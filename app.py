import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Student progress Analysis',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



st.empty()
st.sidebar.image("logo.png", width=300)






def student_analysis():
    st.markdown("<div style='text-align:center;'><h1>Student Marks Analysis 📈</h1></div>", unsafe_allow_html=True,)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        if branch_choice == "CSE":
            st.write("No data Found")
            

        if branch_choice == "ISE":
            xls = pd.ExcelFile('2021.ISE-6.xlsx')
            plot_analysis(xls)

def plot_analysis(xls):
    sheet_name = st.selectbox("Select the semester", xls.sheet_names)
    data = pd.read_excel(xls, sheet_name=sheet_name)
    st.dataframe(data)
    
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h3>   SELECT THE TYPE OF ANALYSIS YOU NEED     </h3></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h4>          </h4></div>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Semester Analysis","Subject Wise Analysis","Student wise Analysis"],
        icons=["person-workspace","stack","person"],
        orientation="horizontal",
        
    )
    
    
    if selected == "Semester Analysis":
        st.markdown("<div style='text-align:center;'><h3>          </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>GRADE ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        
        # Plot a Pie Chart For Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. Pie Chart of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Pie Chart represents the distribution of students according to their grades. The different segments of the chart denote the percentage of students who have achieved a specific grade. The grades are categorized as FCD (First Class Distinction), FC (First Class), SC (Second Class), and FAIL (Failure).")
        
    
        # Create a list of valid grades
        valid_grades = ['FCD', 'FC', 'SC', 'FAIL', 'NE']
        column2 = data.columns[41]
        # Filter the data to only include rows where column2 is in the valid_grades list
        data_to_plot = data[data[column2].isin(valid_grades)]
        # Create the pie chart using the filtered data
        fig = go.Figure(data=[go.Pie( labels=data_to_plot[column2])])
        fig.update_layout( width=700, height=700)
        st.plotly_chart(fig)


        # Plot Histogram for Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>2. Histogram of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Histogram illustrates the distribution of students across different grade ranges, with FCD representing First class Distinction, FC representing First class, SC representing Second Class, and FAIL representing failure.")
        

        column2 = data.columns[41]
        fig = px.histogram(data, x=column2)
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students')
        st.plotly_chart(fig)


        # Baclog Subjects Analysis

        st.markdown("<div style='text-align:center;'><h3>BACKLOG SUBJECTS ANALYSIS 📈</h3></div>", unsafe_allow_html=True)


        #No of students having backlog in each subject
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. No. of Students having Backlogs in Each Subject</h5></div>", unsafe_allow_html=True)
        st.write("The Below Bar Chart represents the number of students who have failed in a particular subject")
        column1 = data.columns[6]
        column2 = data.columns[10]
        column3 = data.columns[14]
        column4 = data.columns[18]
        column5 = data.columns[22]
        column6 = data.columns[26]
        column7 = data.columns[30]
        column8 = data.columns[33]
        column9 = data.columns[37]
        subject_columns = [column1,column2,column3,column4,column5,column6,column7,column8,column9]
        subject_failures = data[subject_columns].eq('F').sum()
        subject_failures.index = [data.iloc[0,3],data.iloc[0, 7] ,data.at[0, data.columns[11]],data.at[0, data.columns[15]], data.at[0, data.columns[19]], data.at[0, data.columns[23]],data.at[0, data.columns[27]], data.at[0, data.columns[30]], data.at[0, data.columns[34]]]
        subject_failures = subject_failures.rename("Number of Failures")
        subject_failures.sort_values(ascending=True, inplace=True)
        fig = px.bar(subject_failures.reset_index(), y='index', x='Number of Failures')
        fig.update_layout(width=700, height=600,yaxis_title='Subject')
        st.plotly_chart(fig)
        


        # Bar Chart between NAME and FAIL

        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>2. Bar Chart between Students and Number of Backlogs </h5></div>", unsafe_allow_html=True)
        st.write("The bar chart illustrates the number of subjects in which students have failed (backlogs) and their corresponding names. It provides a clear visual representation of the students who have failed and the number of subjects they have failed in, allowing for easy identification of students who may require additional support or resources.")
        x_data = data.iloc[:, 2]
        y_data = data.iloc[:, 44]
        # Create a boolean mask to filter y_data where it is not equal to 0
        mask = y_data != 0
        filtered_x_data = x_data[mask]
        filtered_y_data = y_data[mask]
        fig = go.Figure(data=[go.Bar(x=filtered_x_data, y=filtered_y_data)])
        fig.update_layout(width=700, height=600,yaxis_title='No. of Backlog Subjects')
        st.plotly_chart(fig)


        # Percentage Analysis

        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>PERCENTAGE ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. Percentage Histogram</h5></div>", unsafe_allow_html=True)
        st.write("The histogram presents the distribution of percentage marks obtained by students in a semester. It clearly shows the range of marks scored by the students and the frequency at which each mark range occurs, providing a comprehensive understanding of the students' performance in the semester.")
        fig = px.histogram(data, x=data.iloc[:, 40])
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students',xaxis_title="Percentage")
        st.plotly_chart(fig)


        #Topper Analysis

        st.markdown("<div style='text-align:center;'><h3>SEMESTER TOPPER ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)

        st.markdown("<h5>Top 10 Performers in the Semester </h5></div>", unsafe_allow_html=True)
        st.write("The below bar chart showcases the top 10 highest-scoring students in the Semester, displaying their names and marks for easy comparison and analysis.")
        sorted_data = data.sort_values(by='PERCENTAGE',ascending=True)
        sorted_data = sorted_data[['NAME','PERCENTAGE']].tail(12)
        fig = px.bar(sorted_data, x='PERCENTAGE', y='NAME',color='PERCENTAGE',color_continuous_scale=['#90EE90', 'green','#006400'])
        fig.update_layout(width=600, height=500,xaxis_title='Percentage')
        st.plotly_chart(fig)
        st.empty().text_align = 'center'

        st.write("The below table displays the top 10 students who have performed exceptionally well in the Semester.")
        

        sorted = data.sort_values(by='PERCENTAGE',ascending=False)
        sorted = sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']].head(10)
        st._legacy_table(sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']])



    elif selected == "Subject Wise Analysis":
        st.write("Subject Wise Analysis")
        Subject1 = data.iloc[0, 3]
        Subject2 = data.iloc[0, 7]
        Subject3 = data.iloc[0, 11]
        Subject4 = data.iloc[0, 15]
        Subject5 = data.iloc[0, 19]
        Subject6 = data.iloc[0, 23]
        Subject7 = data.iloc[0, 27]
        Subject8 = data.iloc[0, 31]
        Subject9 = data.iloc[0, 35]
        Subject_Choice = st.selectbox("Select the Subject:", [Subject1, Subject2, Subject3, Subject4, Subject5, Subject6, Subject7, Subject8, Subject9])

        if Subject_Choice == Subject1:

            st.write("Analysis for the subject:",Subject1)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject1_Marks = data.columns[5]
            data = data.sort_values(by=Subject1_Marks,ascending=True)
            fig = px.histogram(data, x=Subject1_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject1_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject1_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject1_Results = data.columns[6]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject1_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject1_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("This below bar graph shows the students who have failed in the subject and their total marks")
            failed_data = data.loc[data[data.columns[6]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[5]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
            data[data.columns[5]] = pd.to_numeric(data[data.columns[5]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[5]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[5]] >= 80) & (data[data.columns[5]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[5]] >= 70) & (data[data.columns[5]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[5]] >= 60) & (data[data.columns[5]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[5]] >= 55) & (data[data.columns[5]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[5]] >= 50) & (data[data.columns[5]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[5]] >= 40) & (data[data.columns[5]] < 50)), 'GRADE'] = 'P'

            # Create the bar chart
            grade_counts = data['GRADE'].value_counts()
            fig = go.Figure(data=[go.Bar(x=grade_counts.index, y=grade_counts.values)])
            fig.update_layout( xaxis_title='GRADE', yaxis_title='Number of Students')
            st.plotly_chart(fig)

            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>6. Grade Distribution - Pie Chart</h5></div>", unsafe_allow_html=True)
            st.write("The Pie chart below illustrates the grade distribution of the subject in a clear and concise way, providing a visual representation of the number of students who achieved a specific grade, making it easy to understand and compare with the bar chart representation.")

            grades_count = data['GRADE'].value_counts() 

            fig = go.Figure(data=[go.Pie(labels=grades_count.index, values=grades_count.values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)

            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>7. Internal vs External Test Performance Comparison</h5></div>", unsafe_allow_html=True)
            st.write("The Below pie chart illustrates the comparison of the performance of the whole class in the subject, in terms of their internal test marks versus their external test marks, providing a clear visual representation of the performance of the class in both aspects.")
            data[data.columns[3]] = pd.to_numeric(data[data.columns[3]], errors='coerce')
            data[data.columns[4]] = pd.to_numeric(data[data.columns[4]], errors='coerce')

            column3_data = data[data.columns[3]].sum()
            column4_data = data[data.columns[4]].sum()
            labels = [data.columns[3], data.columns[4]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column3_data, column4_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[5],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[5]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[5], y=data.columns[2],color=data.columns[5],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[5],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[5],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[5],'GRADE','PERCENTAGE']])
            


    elif selected == "Student wise Analysis":


        student_name = st.selectbox("Select a student:", data[data.columns[2]].unique(),index=1)


        # Filter the data to get the marks of the selected student
        student_data = data[data[data.columns[2]] == student_name]
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.write("NAME: ",student_name)
        USN = student_data[data.columns[1]].values[0]
        st.write("USN: ",USN)



        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>MARKS CARD FOR THE SEMESTER </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        st.write("The below table presents a comprehensive view of the student's marks sheet for the specific semester, including the percentage, total marks, and grade obtained by the student ")
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        
        subjects = []
        for i in range(3, 36, 4):
            student_data[data.columns[i+2]] = pd.to_numeric(student_data[data.columns[i+2]], errors='coerce')

            subject = {}
            subject["Name"] = data.iloc[0, i]
            subject["CIE Marks"] = student_data[data.columns[i]].values[0]
            subject["SEE Marks"] = student_data[data.columns[i+1]].values[0]
            subject["Total"] = student_data[data.columns[i+2]].values[0]
            subject["Results"] = student_data[data.columns[i+3]].values[0]

                #Assign the grades and grade points based on the total marks
            subject["Grade"] = "F"
            subject["Grade Points"] = 0
            if subject["Total"] >= 90:
                subject["Grade"] = "O"
                subject["Grade Points"] = 10
            elif subject["Total"] >= 80:
                subject["Grade"] = "A+"
                subject["Grade Points"] = 9
            elif subject["Total"] >= 70:
                subject["Grade"] = "A"
                subject["Grade Points"] = 8
            elif subject["Total"] >= 60:
                subject["Grade"] = "B+"
                subject["Grade Points"] = 7
            elif subject["Total"] >= 55:
                subject["Grade"] = "B"
                subject["Grade Points"] = 6
            elif subject["Total"] >= 50:
                subject["Grade"] = "C"
                subject["Grade Points"] = 5
            elif subject["Total"] >= 40:
                subject["Grade"] = "P"
                subject["Grade Points"] = 4
            subjects.append(subject)
        
        st._legacy_table(pd.DataFrame(subjects))

        

        student_table = pd.DataFrame({
            
            'Total': [student_data[data.columns[39]].values[0]],
            'Percentage': [student_data[data.columns[40]].values[0]],
            'Grade': [student_data[data.columns[41]].values[0]],
            'Results': [student_data[data.columns[42]].values[0]],
            'Passed Subjects': [student_data[data.columns[43]].values[0]],
            'Failed Subjects': [student_data[data.columns[44]].values[0]],
            'Absent Subjects': [student_data[data.columns[45]].values[0]],
        })
        
        st._legacy_table(student_table)



        if student_data.empty:
            st.error("No data found for selected student.")
        else:
            # Extract the marks of the student in the 5th and 9th columns
            subject1_marks = student_data[data.columns[5]].values[0]
            subject2_marks = student_data[data.columns[9]].values[0]
            subject3_marks = student_data[data.columns[13]].values[0]
            subject4_marks = student_data[data.columns[17]].values[0]
            subject5_marks = student_data[data.columns[21]].values[0]
            subject6_marks = student_data[data.columns[25]].values[0]
            subject7_marks = student_data[data.columns[29]].values[0]
            subject8_marks = student_data[data.columns[33]].values[0]
            subject9_marks = student_data[data.columns[37]].values[0]

            subject1_name = data.iloc[0,3]
            subject2_name = data.iloc[0,7]
            subject3_name = data.iloc[0,11]
            subject4_name = data.iloc[0,15]
            subject5_name = data.iloc[0,19]
            subject6_name = data.iloc[0,23]
            subject7_name = data.iloc[0,27]
            subject8_name = data.iloc[0,31]
            subject9_name = data.iloc[0,35]

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h3>BAR CHART OF MARKS IN EVERY SUBJECT </h3></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.write("The below bar chart provides a visual representation of the student's performance in each subject of the semester, highlighting the marks obtained by the student in each subject and allowing for a quick and easy comparison of the student's performance across all subjects.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            
            # Create a bar chart of the extracted marks
            fig = px.bar(x=[subject1_name, subject2_name,subject3_name,subject4_name,subject5_name,subject6_name,subject7_name,subject8_name,subject9_name],
             y=[subject1_marks, subject2_marks,subject3_marks,subject4_marks,subject5_marks,subject6_marks,subject7_marks,subject8_marks,subject9_marks])
            fig.update_layout(xaxis_title='Subject',yaxis_title='Total Marks',width=700, height=600)
            st.plotly_chart(fig)



def check_credentials(username, password):
    if username == "darshangowda" and password == "Darshan@123":
        return True
    else:
        return False

def department_login():
    st.markdown("<div style='text-align:center;'><h1>DEPARTMENT LOGIN</h1></div>", unsafe_allow_html=True,)
  
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        if check_credentials(username, password):
            st.success("Logged in Successfully!")
            uploaded_file = st.file_uploader("Choose a file", type="xlsx")
            if uploaded_file:
                with open("/Users/darshangowda/Documents/SavedXLSX/2021.ISE.StudentMarksSheet.xlsx", "wb") as f:
                    f.write(uploaded_file.read())
                st.success("File saved in desired folder.")

        else:
            st.sidebar.error("Incorrect username or password",icon="☠️")


def how_to_use():
    st.markdown("<div style='text-align:center;'><h1>Guide to use the Website</h1></div>", unsafe_allow_html=True,)
    video_iframe = '<iframe width="700" height="405" src="https://youtube.com/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    st.write(video_iframe, unsafe_allow_html=True)



st.sidebar.title("")
st.sidebar.title("")
with st.sidebar:
    
    selected = option_menu(
            menu_title= "Main Menu",
            options= ["Student Analysis","Department Login","How to use"],
            icons= ["person-workspace","briefcase","box-arrow-in-right"],
            menu_icon="house",
            default_index=0,
            orientation="horizantal",
        )
if selected == "Student Analysis":
    student_analysis()
if selected == "Department Login":
    department_login()
if selected == "How to use":
    how_to_use()  
