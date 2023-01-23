import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


st.set_page_config(page_title='Student progress Analysis',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded")


st.empty()
st.sidebar.image("logo.png", width=300)
st.sidebar.title("MENU")


hide_st_style = """
            <style>
            
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def student_analysis():
    st.markdown("<div style='text-align:center;'><h1>Student Marks Analysis 📈</h1></div>", unsafe_allow_html=True,)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        if branch_choice == "CSE":
            st.write("No Data")
            

        if branch_choice == "ISE":
            xls = pd.ExcelFile('2021.ISE-6.xlsx')
            plot_analysis(xls)

def plot_analysis(xls):
    sheet_name = st.selectbox("Select the semester", xls.sheet_names)
    data = pd.read_excel(xls, sheet_name=sheet_name)
    st.dataframe(data)
    type_choice = st.selectbox("Select the type of analytics you need", ["Semester Analysis", "Subject Wise Analysis","Student wise Analysis"])
    if type_choice == "Semester Analysis":
        st.markdown("<div style='text-align:center;'><h3>          </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>GRADE ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        
        # Plot a Pie Chart For Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. Pie Chart of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Pie Chart denotes the Percentage of students with respective to their Grades")
        st.write("FCD - First class Distinction, FC - First class, SC - Second Class, FAIL - Failure")
    
        # Create a list of valid grades
        valid_grades = ['FCD', 'FC', 'SC', 'FAIL', 'NE']
        column2 = data.columns[41]
        # Filter the data to only include rows where column2 is in the valid_grades list
        data_to_plot = data[data[column2].isin(valid_grades)]
        # Create the pie chart using the filtered data
        fig = go.Figure(data=[go.Pie( labels=data_to_plot[column2])])
        fig.update_layout(title=column2, width=700, height=700)
        st.plotly_chart(fig)


        # Plot Histogram for Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>2. Histogram of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Histogram denotes the Number of students with respective to their Grades.")
        st.write("FCD - First class Distinction, FC - First class, SC - Second Class, FAIL - Failure")

        column2 = data.columns[41]
        fig = px.histogram(data, x=column2)
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students')
        st.plotly_chart(fig)


        # Baclog Subjects Analysis

        st.markdown("<div style='text-align:center;'><h3>BACKLOG SUBJECTS ANALYSIS 📈</h3></div>", unsafe_allow_html=True)


        #No of students having backlog in each subject
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. No. of Students having Backlogs in Each Subject</h5></div>", unsafe_allow_html=True)
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
        st.markdown("<h5>2. Bar Chart between NAME and FAIL</h5></div>", unsafe_allow_html=True)
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
        fig = px.histogram(data, x=data.iloc[:, 40])
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students')
        st.plotly_chart(fig)


        #Topper Analysis

        st.markdown("<div style='text-align:center;'><h3>TOPPER LIST 📈</h3></div>", unsafe_allow_html=True)
        sorted_data = data.sort_values(by='PERCENTAGE',ascending=True)
        sorted_data = sorted_data[['NAME','PERCENTAGE']].tail(12)
        fig = px.bar(sorted_data, x='PERCENTAGE', y='NAME',color='PERCENTAGE',color_continuous_scale=['#90EE90', 'green','#006400'])
        st.plotly_chart(fig)
        st.empty().text_align = 'center'

        st.markdown("<div><h4>    1. Top 10 Toppers List      </h4></div>", unsafe_allow_html=True)
        

        sorted = data.sort_values(by='PERCENTAGE',ascending=False)
        sorted = sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']].head(10)
        st.write(sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']])



    elif type_choice == "Subject Wise Analysis":
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

            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            Subject1_Marks = data.columns[5]
            data = data.sort_values(by=Subject1_Marks,ascending=True)
            fig = px.histogram(data, x=Subject1_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject1_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. ScatterPlot Between NAME and Total</h5></div>", unsafe_allow_html=True)
            fig = px.bar(data, x=Student_Name, y=Subject1_Marks)
            fig.update_layout(width=600, height=600)
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject1_Results = data.columns[6]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject1_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject1_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            failed_data = data.loc[data[data.columns[6]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[5]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(title="Failed Students Total Marks", xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
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
            fig.update_layout(title='Grades of Students', xaxis_title='GRADE', yaxis_title='Number of Students')
            st.plotly_chart(fig)

            grades_count = data['GRADE'].value_counts() 

            fig = go.Figure(data=[go.Pie(labels=grades_count.index, values=grades_count.values)])
            fig.update_layout(title="Grades Percentage",width=700, height=700)
            st.plotly_chart(fig)


            data[data.columns[3]] = pd.to_numeric(data[data.columns[3]], errors='coerce')
            data[data.columns[4]] = pd.to_numeric(data[data.columns[4]], errors='coerce')

            column3_data = data[data.columns[3]].sum()
            column4_data = data[data.columns[4]].sum()
            labels = [data.columns[3], data.columns[4]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column3_data, column4_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(title="CIE vs SEE Marks",width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<div style='text-align:center;'><h3>SUBJECT TOPPER LIST 📈</h3></div>", unsafe_allow_html=True)
            sorted_data = data.sort_values(by=data.columns[5],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[5]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[5], y=data.columns[2],color=data.columns[5],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            sorted = data.sort_values(by='PERCENTAGE',ascending=False)
            sorted = sorted[['USN','NAME',data.columns[5],'GRADE','PERCENTAGE']].head(10)
            st.write(sorted[['USN','NAME',data.columns[5],'GRADE','PERCENTAGE']])
            


    elif type_choice == "Student wise Analysis":



        student_name = st.selectbox("Select a student:", data[data.columns[2]].unique())

        # Filter the data to get the marks of the selected student
        student_data = data[data[data.columns[2]] == student_name]

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
            
            # Create a bar chart of the extracted marks
            fig = px.bar(x=[subject1_name, subject2_name,subject3_name,subject4_name,subject5_name,subject6_name,subject7_name,subject8_name,subject9_name],
             y=[subject1_marks, subject2_marks,subject3_marks,subject4_marks,subject5_marks,subject6_marks,subject7_marks,subject8_marks,subject9_marks])
            st.plotly_chart(fig)



def check_credentials(username, password):
    if username == "darshangowda" and password == "Darshan@123":
        return True
    else:
        return False

def department_login():
    st.markdown("<div style='text-align:center;'><h1>Department Login</h1></div>", unsafe_allow_html=True,)
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        if check_credentials(username, password):
            st.success("Logged in Successfully!")
            update_excel()
        else:
            st.error("Incorrect username or password",icon="☠️")


def how_to_use():
    st.markdown("<div style='text-align:center;'><h1>Guide to use the Website</h1></div>", unsafe_allow_html=True,)
    video_iframe = '<iframe width="700" height="405" src="https://youtube.com/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    st.write(video_iframe, unsafe_allow_html=True)


def update_excel():
    st.write("Update your excel Sheet here")

app_mode = st.sidebar.selectbox("Choose what you want 👇",["Student Analysis", "Department Login", "How to use"])
if app_mode == "Student Analysis":
    student_analysis()
elif app_mode == "Department Login":
    department_login()
elif app_mode == "How to use":
    how_to_use()





