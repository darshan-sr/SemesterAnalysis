import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu
import base64 
import os

import streamlit_authenticator as stauth
import database as db
from glob import glob
from termcolor import colored

from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore import Client



st.set_page_config(page_title='Student progress Analysis',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded")


with open('style1.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("sidebarlogo.jpg")

page_bg_img = f"""


<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: topleft;
background-repeat: no-repeat;
background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.sidebar.title("")
st.sidebar.title("")




def student_analysis():
    st.markdown("<div style='text-align:center;'><h1>STUDENT MARKS ANALYSIS 📈</h1></div>", unsafe_allow_html=True,)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
 
   
    

    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        if branch_choice == "CSE":
            try:
                xls = pd.ExcelFile('/Users/darshangowda/Documents/SavedXLSX/2021.CSE.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except:
                st.write("Data not found")
            

        if branch_choice == "ISE":
            xls = pd.ExcelFile('2021.ISE-6.xlsx')
            plot_analysis(xls)
            


        if branch_choice == "ECE":
            try:
                xls = pd.ExcelFile('/Users/darshangowda/Documents/SavedXLSX/2021/ECE/2021.ECE.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except:
                st.write("Data not found")

        if branch_choice == "ME":
            try:
                xls = pd.ExcelFile('/Users/darshangowda/Documents/SavedXLSX/2021/ME/2021.ME.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except FileNotFoundError:
                st.write("Data not found")


def plot_analysis(xls):
    sheet_name = st.selectbox("Select the semester", xls.sheet_names)
    data = pd.read_excel(xls, sheet_name=sheet_name)
    
    
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
        st.dataframe(data)
        
        
        
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


        if Subject_Choice == Subject2:

            st.write("Analysis for the subject:",Subject2)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject2_Marks = data.columns[9]
            data = data.sort_values(by=Subject2_Marks,ascending=True)
            fig = px.histogram(data, x=Subject2_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject2_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject2_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject2_Results = data.columns[10]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject2_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject2_Results])])
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
            data[data.columns[9]] = pd.to_numeric(data[data.columns[9]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[9]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[9]] >= 80) & (data[data.columns[9]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[9]] >= 70) & (data[data.columns[9]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[9]] >= 60) & (data[data.columns[9]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[9]] >= 55) & (data[data.columns[9]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[9]] >= 50) & (data[data.columns[9]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[9]] >= 40) & (data[data.columns[9]] < 50)), 'GRADE'] = 'P'

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
            data[data.columns[7]] = pd.to_numeric(data[data.columns[7]], errors='coerce')
            data[data.columns[8]] = pd.to_numeric(data[data.columns[8]], errors='coerce')

            column7_data = data[data.columns[7]].sum()
            column8_data = data[data.columns[8]].sum()
            labels = [data.columns[7], data.columns[8]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column7_data, column8_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[9],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[9]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[9], y=data.columns[2],color=data.columns[9],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[9],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[9],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[9],'GRADE','PERCENTAGE']])


        if Subject_Choice == Subject3:

            st.write("Analysis for the subject:",Subject3)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject3_Marks = data.columns[13]
            data = data.sort_values(by=Subject3_Marks,ascending=True)
            fig = px.histogram(data, x=Subject3_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject3_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject3_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject3_Results = data.columns[14]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject3_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject3_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("This below bar graph shows the students who have failed in the subject and their total marks")
            failed_data = data.loc[data[data.columns[14]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[13]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
            data[data.columns[13]] = pd.to_numeric(data[data.columns[9]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[13]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[13]] >= 80) & (data[data.columns[13]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[13]] >= 70) & (data[data.columns[13]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[13]] >= 60) & (data[data.columns[13]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[13]] >= 55) & (data[data.columns[13]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[13]] >= 50) & (data[data.columns[13]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[13]] >= 40) & (data[data.columns[13]] < 50)), 'GRADE'] = 'P'

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
            data[data.columns[12]] = pd.to_numeric(data[data.columns[12]], errors='coerce')
            data[data.columns[13]] = pd.to_numeric(data[data.columns[13]], errors='coerce')

            column13_data = data[data.columns[12]].sum()
            column14_data = data[data.columns[13]].sum()
            labels = [data.columns[12], data.columns[13]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column13_data, column14_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[13],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[13]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[13], y=data.columns[2],color=data.columns[13],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[13],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[13],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[13],'GRADE','PERCENTAGE']])


        if Subject_Choice == Subject4:

            st.write("Analysis for the subject:",Subject4)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject4_Marks = data.columns[17]
            data = data.sort_values(by=Subject4_Marks,ascending=True)
            fig = px.histogram(data, x=Subject4_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject4_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject4_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject4_Results = data.columns[18]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject4_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject4_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("This below bar graph shows the students who have failed in the subject and their total marks")
            failed_data = data.loc[data[data.columns[18]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[17]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
            data[data.columns[17]] = pd.to_numeric(data[data.columns[9]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[17]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[17]] >= 80) & (data[data.columns[17]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[17]] >= 70) & (data[data.columns[17]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[17]] >= 60) & (data[data.columns[17]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[17]] >= 55) & (data[data.columns[17]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[17]] >= 50) & (data[data.columns[17]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[17]] >= 40) & (data[data.columns[17]] < 50)), 'GRADE'] = 'P'

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
            data[data.columns[15]] = pd.to_numeric(data[data.columns[12]], errors='coerce')
            data[data.columns[16]] = pd.to_numeric(data[data.columns[13]], errors='coerce')

            column13_data = data[data.columns[15]].sum()
            column14_data = data[data.columns[16]].sum()
            labels = [data.columns[15], data.columns[16]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column13_data, column14_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[17],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[17]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[17], y=data.columns[2],color=data.columns[17],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[17],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[17],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[17],'GRADE','PERCENTAGE']])


        if Subject_Choice == Subject5:

            st.write("Analysis for the subject:",Subject5)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject5_Marks = data.columns[21]
            data = data.sort_values(by=Subject5_Marks,ascending=True)
            fig = px.histogram(data, x=Subject5_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject5_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject5_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject5_Results = data.columns[22]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject5_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject5_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("This below bar graph shows the students who have failed in the subject and their total marks")
            failed_data = data.loc[data[data.columns[22]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[21]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
            data[data.columns[21]] = pd.to_numeric(data[data.columns[21]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[21]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[21]] >= 80) & (data[data.columns[21]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[21]] >= 70) & (data[data.columns[21]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[21]] >= 60) & (data[data.columns[21]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[21]] >= 55) & (data[data.columns[21]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[21]] >= 50) & (data[data.columns[21]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[21]] >= 40) & (data[data.columns[21]] < 50)), 'GRADE'] = 'P'

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
            data[data.columns[19]] = pd.to_numeric(data[data.columns[19]], errors='coerce')
            data[data.columns[20]] = pd.to_numeric(data[data.columns[20]], errors='coerce')

            column19_data = data[data.columns[19]].sum()
            column20_data = data[data.columns[20]].sum()
            labels = [data.columns[19], data.columns[16]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column19_data, column20_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[21],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[21]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[21], y=data.columns[2],color=data.columns[21],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[21],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[21],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[21],'GRADE','PERCENTAGE']])
            

        if Subject_Choice == Subject6:

            st.write("Analysis for the subject:",Subject6)
            st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)

            # Histogram of Marks

            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
            st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            Subject6_Marks = data.columns[25]
            data = data.sort_values(by=Subject6_Marks,ascending=True)
            fig = px.histogram(data, x=Subject6_Marks)
            fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
            st.plotly_chart(fig)


            Student_Name = data.columns[2]
            data = data.sort_values(by=Subject6_Marks,ascending=True)
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
            st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
            fig = px.bar(data, x=Student_Name, y=Subject6_Marks)
            fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
            st.plotly_chart(fig)


            # Create a list of valid grades
            valid_grades = ['P', 'F', 'X','A']
            Subject6_Results = data.columns[26]
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
            st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
            # Filter the data to only include rows where Subject1_Results is in the valid_grades list
            data_to_plot = data[data[Subject6_Results].isin(valid_grades)]
            # Create the pie chart using the filtered data
            fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject6_Results])])
            fig.update_layout( width=700, height=700)
            st.plotly_chart(fig)


            # Analysis of Student Having Backlog in the Subject
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("This below bar graph shows the students who have failed in the subject and their total marks")
            failed_data = data.loc[data[data.columns[26]].isin(['F', 'X', 'A','NE'])]
            student_name = failed_data[data.columns[2]]
            student_marks = failed_data[data.columns[25]]
            fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
            fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
            st.plotly_chart(fig)


            # Grade Analysis
            # Create a new column 'GRADE' based on the conditions provided
            st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
            st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
            data[data.columns[25]] = pd.to_numeric(data[data.columns[25]], errors='coerce')
            data['GRADE'] = 'F'
            data.loc[(data[data.columns[25]] >= 90), 'GRADE'] = 'O'
            data.loc[((data[data.columns[25]] >= 80) & (data[data.columns[25]] < 90)), 'GRADE'] = 'A+'
            data.loc[((data[data.columns[25]] >= 70) & (data[data.columns[25]] < 80)), 'GRADE'] = 'A'
            data.loc[((data[data.columns[25]] >= 60) & (data[data.columns[25]] < 70)), 'GRADE'] = 'B+'
            data.loc[((data[data.columns[25]] >= 55) & (data[data.columns[25]] < 60)), 'GRADE'] = 'B'
            data.loc[((data[data.columns[25]] >= 50) & (data[data.columns[25]] < 55)), 'GRADE'] = 'C'
            data.loc[((data[data.columns[25]] >= 40) & (data[data.columns[25]] < 50)), 'GRADE'] = 'P'

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
            data[data.columns[23]] = pd.to_numeric(data[data.columns[23]], errors='coerce')
            data[data.columns[24]] = pd.to_numeric(data[data.columns[24]], errors='coerce')

            column23_data = data[data.columns[23]].sum()
            column24_data = data[data.columns[24]].sum()
            labels = [data.columns[23], data.columns[24]]
            labels[0] = 'CIE'
            labels[1] = 'SEE'
            values = [column23_data, column24_data]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(width=700, height=700)
            st.plotly_chart(fig)


            st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
            st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
            sorted_data = data.sort_values(by=data.columns[25],ascending=True)
            sorted_data = sorted_data[[data.columns[2],data.columns[25]]].tail(12)
            fig = px.bar(sorted_data, x=data.columns[25], y=data.columns[2],color=data.columns[25],color_continuous_scale=['#90EE90', 'green','#006400'])
            fig.update_layout(xaxis_title='Total Marks in the Subject')
            st.plotly_chart(fig)

            st.markdown("<h1></h1></div>", unsafe_allow_html=True)
            st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
            sorted = data.sort_values(by=data.columns[25],ascending=False)
            sorted = sorted[['USN','NAME',data.columns[25],'GRADE','PERCENTAGE']].head(10)
            st.table(sorted[['USN','NAME',data.columns[25],'GRADE','PERCENTAGE']])
    


    elif selected == "Student wise Analysis":


        student_name = st.selectbox("Select a student:", data[data.columns[2]].unique(),index=1)

    
        # Filter the data to get the marks of the selected student
        student_data = data[data[data.columns[2]] == student_name]
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        NAME = student_data[data.columns[2]].values[0]
        st.write("NAME: ",NAME)
        USN = student_data[data.columns[1]].values[0]
        st.write("USN: ",USN)

        with open('style1.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.markdown('### STUDENT DETAILS:')
        col1, col2= st.columns(2)
        col1.metric("Name",NAME)
        col2.metric("USN",USN)


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

        Total= int(student_data[data.columns[39]].values[0])
        Percentage= round(student_data[data.columns[40]].values[0],2)
        Grade= student_data[data.columns[41]].values[0]
        Results=student_data[data.columns[42]].values[0]
        Passed_Subjects=int(student_data[data.columns[43]].values[0])
        Failed_Subjects=int(student_data[data.columns[44]].values[0])
        Absent_Subjects=int(student_data[data.columns[45]].values[0])
        st.markdown('')
        col1, col2,col3= st.columns(3)
        col1.metric("TOTAL:",Total)
        col2.metric("PERCENTAGE:","{:.2f}%".format(Percentage))
        col3.metric("GRADE:",Grade)
    
        col4,col5,col6 = st.columns(3)
        
        def color_text(Results):
            if Results == "PASS":
                return colored(Results, "green")
            elif Results == "FAIL":
                return colored(Results, "red")
        colored_results = color_text(Results)
        col4.metric("RESULTS:", colored_results)
        col5.metric("PASSED SUBJECTS:",Passed_Subjects)
        col6.metric("FAILED SUBJECTS",Failed_Subjects)



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


def USN_analysis():
    student_id = st.text_input("Enter student USN:")
    data = pd.DataFrame()
    path = '/Users/darshangowda/Documents/SavedXLSX/2021/ISE/'
    
    if not os.path.exists(path):
        st.error("Invalid path")
        return

    sheet_names = []
    for file in glob(path + "*.xlsx"):
        xls = pd.ExcelFile(file)
        sheet_names.extend(xls.sheet_names)
    sheet_names = list(set(sheet_names))
    selected_sheet = st.selectbox("Select a sheet", sheet_names)

    for file in glob(path + "*.xlsx"):
        try:
            xls = pd.ExcelFile(file)
            data = pd.concat([data, pd.read_excel(xls, sheet_name=selected_sheet)])
        except Exception as e:
            st.error("Error reading file: " + file)
            st.exception(e)
            return
            
    if student_id not in data['USN'].values:
        st.warning("USN not found.")
    else:
    
        student_data = data.loc[data['USN'] == student_id]
        NAME = student_data[data.columns[2]].values[0]
        
        USN = student_data[data.columns[1]].values[0]
        with open('style1.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)        


        st.markdown('### STUDENT DETAILS:')
        col1, col2= st.columns(2)
        col1.metric("Name",NAME)
        col2.metric("USN",USN)

        
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



        Total= int(student_data[data.columns[39]].values[0])
        Percentage= round(student_data[data.columns[40]].values[0],2)
        Grade= student_data[data.columns[41]].values[0]
        Results=student_data[data.columns[42]].values[0]
        Passed_Subjects=int(student_data[data.columns[43]].values[0])
        Failed_Subjects=int(student_data[data.columns[44]].values[0])
        Absent_Subjects=int(student_data[data.columns[45]].values[0])
        st.markdown('')
        col1, col2,col3= st.columns(3)
        col1.metric("TOTAL:",Total)
        col2.metric("PERCENTAGE:","{:.2f}%".format(Percentage))
        col3.metric("GRADE:",Grade)
        
        col4,col5,col6 = st.columns(3)
        col4.metric("RESULTS:",Results)
        col5.metric("PASSED SUBJECTS:",Passed_Subjects)
        col6.metric("FAILED SUBJECTS",Failed_Subjects)
        

        
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

    




def department_login():
    st.title("DEPARTMENT LOGIN")
    users = db.fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "sales_dashboard", "abcdef", cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login("LOGIN", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        st.success("Logged in successfully")
        authenticator.logout("Logout", "sidebar")

        if username == "ISE":
            batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
            if batch_choice == "2021 Batch":
                uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                if uploaded_file:
                    with open("/Users/darshangowda/Documents/SavedXLSX/2021/ISE/2021.ISE.StudentMarksSheet.xlsx", "wb") as f:
                        f.write(uploaded_file.read())
                    st.success("File saved in desired folder.")





def how_to_use():
    st.markdown("<div style='text-align:center;'><h1>GUIDE TO USE THE WEBSITE 👨🏻‍💻</h1></div>", unsafe_allow_html=True,)
    video_iframe = '<iframe width="700" height="405" src="https://youtube.com/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    st.write(video_iframe, unsafe_allow_html=True)


def Submit_Feedback():
    
    st.header(":mailbox: Submit a Feedback!")
    st.title("")
    st.write("We are collecting feedback for our Student Marks Analysis app which is used by college lectures and students. Your input on what can be improved and if there are any bugs will greatly assist in the continued development of the app. Your suggestions for new features would also be appreciated. Please fill out the contact form to share your thoughts and feedback. Your contributions will help make the app an even more useful tool for the college community")
    st.title("")

    @st.experimental_singleton
    def get_db():
        db = firestore.Client.from_service_account_json("key.json")
        return db


    def post_message(db: Client, input_name, input_mail, input_message):
        payload = {
            "name": input_name,
            "mail": input_mail,
            "message": input_message,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        }
        doc_ref = db.collection("").document()
    
        doc_ref.set(payload)
        return


    def main():

        db = get_db()

        with st.form(key="form"):
            input_name = st.text_input("Your Name: ",placeholder="Name")
            input_mail = st.text_input("Your college Mail ID: ",placeholder="example.rvitm@rvei.edu.in")
            input_message = st.text_area("Your Feedback: ",placeholder="Your Feedback Here")
    
            if st.form_submit_button("Submit"):
                post_message(db, input_name, input_mail, input_message)
                st.success("Your Feedback was Submitted!")
            


    if __name__ == "__main__":
       
        main()


def about():

    st.title("About")

st.sidebar.title("")
st.sidebar.title("")

with st.sidebar:
    
        
    with open('/Users/darshangowda/StreamlitApp/style1.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 
    selected = option_menu(
            menu_title= "MAIN MENU",
            options= ["Class Analysis","Student Analysis","Department Login","How to use","Progress Report Generation","Submit Feedback","About"],
            icons= ["person-workspace","person","briefcase","box-arrow-in-right","file-earmark-break","envelope-plus","code"],
            menu_icon="list",
            default_index=0,
            orientation="horizantal",
        )
if selected == "Class Analysis":
    student_analysis()
if selected == "Student Analysis":
    USN_analysis()
if selected == "Department Login":
    department_login()
if selected == "How to use":
    how_to_use()  
if selected == "Progress Report Generation":
    st.markdown("<div style='text-align:center;'><h1>UNDER DEVELOPMENT   🚧</h1></div>", unsafe_allow_html=True,)
if selected == "Submit Feedback":
    Submit_Feedback()
if selected == "About":
    about()

