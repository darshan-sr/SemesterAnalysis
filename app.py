import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


st.set_page_config(page_title='Student progress Analysis',
page_icon='/Users/darshangowda/Documents/StudentAnalytics.py/RVlogo.png', 
initial_sidebar_state="expanded")


st.empty()
st.sidebar.image("/Users/darshangowda/Documents/StudentAnalytics.py/logo.png", width=300)
st.sidebar.title("MENU")


hide_st_style = """
            <style>
            
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def student_analysis():
    st.markdown("<div style='text-align:center;'><h1>Student Marks Analysis 📈</h1></div>", unsafe_allow_html=True,)
    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        if branch_choice == "CSE":
            xls = pd.ExcelFile('/Users/darshangowda/Documents/StudentAnalytics.py/2021.CSE.StudentMarksSheet.xlsx')
            plot_analysis(xls) 

        if branch_choice == "ISE":
            xls = pd.ExcelFile('/Users/darshangowda/Documents/StudentAnalytics.py/2021.ISE-6.xlsx')
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
        sorted_data = sorted_data[['USN','NAME','TOTAL','GRADE','PERCENTAGE']].tail(12)
        fig = px.bar(sorted_data, x='PERCENTAGE', y='NAME',color='PERCENTAGE',color_continuous_scale=['#90EE90', 'green','#006400'])
        st.plotly_chart(fig)
        st.empty().text_align = 'center'

        sorted = data.sort_values(by='PERCENTAGE',ascending=False)
        sorted = sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']].head(10)
        st.write(sorted[['USN','NAME','TOTAL','GRADE','PERCENTAGE']])



    elif type_choice == "Subject Wise Analysis":
        st.write("Subject Wise Analysis")


    elif type_choice == "Student wise Analysis":
        st.write("Student")
        student_name = st.selectbox("Select a student:", data["NAME"].unique())
        student_data = data[data["NAME"] == student_name]
        st.write("Student-wise Analytics for:", student_name)


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
            st.error("Incorrect username or password")


def how_to_use():
    st.markdown("<div style='text-align:center;'><h1>Guide to use the Website</h1></div>", unsafe_allow_html=True,)
    video_iframe = '<iframe width="700" height="405" src="https://youtu.be/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
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





