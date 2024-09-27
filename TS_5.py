import streamlit as st
import pandas as pd
import os
import warnings
import re
import datetime as dt
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
import duckdb
from PIL import Image
import base64
from io import BytesIO
from streamlit_option_menu import option_menu

warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")
hide_streamlit_style = """
        <style>
        /* Hide header */
        header {visibility: hidden;}
        
        /* Hide footer */
        footer {visibility: hidden;}
        </style>
    """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# change folder
#url = "https://raw.githubusercontent.com/Rugger85/Reck_TS/main/users_db.xlsx"
users = pd.read_excel("users_db.xlsx")
# change folder
clients = pd.read_excel("clients.xlsx", sheet_name='Client', dtype=str)
# change folder
work_area = pd.read_excel("clients.xlsx", sheet_name='Work_Area', dtype=str)
# change folder
TOA = pd.read_excel("clients.xlsx", sheet_name='Type_of_assignment', dtype=str)

def authenticate(username_or_email, password):
    for index, row in users.iterrows():
        if (username_or_email == row['Username'] or username_or_email == row['email']) and password == row['Pwd']:
            return True
    return False

def login():
    page_bg_css = '''
        <style>
        .stApp {
            background-color: #2eafa2;
            color: white;  /* Set default text color to white */
        }
        .stTextInput > label, .stSelectbox > label, .stError {
            color: white;  /* Set text color of labels and error messages to white */
        }
        .stTitle {
            color: white;  /* Set text color of the title to white */
            font-family: 'Arial', sans-serif;  /* Set font type */
        }
        .stButton > button {
            color: inherit;  /* Inherit color from the parent element (background color) */
            background-color: #1e8e8d;  /* Set a different background color for buttons if needed */
        }
        /* Style for logo */
        .logo-container {
            text-align: center;
            margin-top: 5px;
        }
        .logo-container img {
            width: 200px;  /* Adjust the width of the logo */
        }
        /* Style for footer text */
        .footer-text {
            position: absolute;
            bottom: -150px;  /* Adjust bottom positioning */
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-family: 'Bell MT', serif;
            font-size: 1.2em;  /* Adjust font size */
        }
        </style>
    '''
    def image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    
    st.markdown(page_bg_css, unsafe_allow_html=True)
    # change folder
    logo_path = "Final_logo_ver_1_white-01.png" 
    image = Image.open(logo_path)   
    st.markdown(f'''
        <div class="logo-container">
            <img src="data:image/png;base64,{image_to_base64(image)}" alt="Logo">
        </div>
    ''', unsafe_allow_html=True)
    

    st.markdown('<h1 style="color: white; font-family: Bell MT;">Welcome to Timesheet</h1>', unsafe_allow_html=True)

    choice = st.selectbox("Login/Signup", ['Login', 'Sign Up'])

    if choice == 'Login':
        username_or_email = st.text_input('Username or Email address')
        password = st.text_input('Password', type='password')
        
        if '@' in username_or_email:
            
            user_record = users[users['email'] == username_or_email]
        else:
            
            user_record = users[users['Username'] == username_or_email]
        
        
        if not user_record.empty:
            username_or_email = user_record['Username'].item()
            designation = user_record['Designation'].item()
            emp_no = user_record['Employee No'].item()
            emp_no = str(emp_no)
            emp_no = emp_no.strip(".0")
            
            if st.button('Login'):
                if authenticate(username_or_email, password):
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = username_or_email
                    st.session_state['designation'] = designation
                    st.session_state['emp_no'] = emp_no
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        else:
            st.error("User not found")

    else:
        # change folder
        df = pd.read_excel("users_db.xlsx")
        fullname = st.text_input("Full Name")
        email = st.text_input("Email address")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        email_pattern = r'^[A-Za-z].*@thereckoner\.co\.uk$'
        title = st.selectbox("Designation", ["Trainee", "Semi-Senior Audit Associate", "Senior Audit Associate", "Assistant Manager", "Manager",
                                             "HR Executive", "HR Coordinator", "HR Manager", "IT Adminstrator"])
        manager = st.selectbox("Manager", ["Ibrar", "Zeeshan", "Zaynab", "Danial", "Jawad", "Khan"])
        joining = st.date_input('Select Date')
        global new_emp_no
        if title == "Manager":
            df_2 = df[df["Designation"] == "Manager"]
        
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 1001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)

        if title == "Assistant Manager":
            df_2 = df[df["Designation"] == "Assistant Manager"]
        
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 2001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)

        if title == "Senior Audit Associate":
            df_2 = df[df["Designation"] == "Senior Audit Associate"]
            
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 3001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)

        if title == "Semi-Senior Audit Associate":
            df_2 = df[df["Designation"] == "Semi-Senior Audit Associate"]
        
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 4001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)
        
        if title == "Trainee":
            df_2 = df[df["Designation"] == "Trainee"]
        
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 5001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)
        if title in ["HR Executive", "HR Coordinator", "IT Adminstrator", "HR Manager"]:
            df_2 = df[df["Designation"].isin(["HR Executive", "HR Coordinator", "IT Adminstrator", "HR Manager"])]
        
            max_emp_no = df_2["Employee No"].max()
            if pd.isna(max_emp_no):
                new_emp_no = 6001
            else:
                
                new_emp_no = int(max_emp_no + 1)
            
            st.markdown(f"""
                <h1 style='color:white; font-size:30px;'>
                    Employee No: {new_emp_no}
                </h1>
            """, unsafe_allow_html=True)
        
        if re.match(email_pattern,email):
            if st.button("Register"):
                if users[users['email'] == email].empty and users[users['Username'] == username].empty:
                    new_entry = {"Username": username, "email": email, "Pwd": password, "Designation": title, "Manager": manager, "Joining Date": joining, "Employee No": new_emp_no, "Full Name": fullname}
                    users.loc[len(users)] = new_entry
                    # change folder
                    users.to_excel("users_db.xlsx", index=False)
                    st.success("Registration Successful")
                else:
                    st.error("User already exists!")
        else:
            st.error("Invalid email address")
    st.markdown('<div class="footer-text">East side, Plaza, Fazal-e-haq road, Blue Area, Islamabad</div>', unsafe_allow_html=True)

def authenticated_page():
    
    #st.set_page_config(layout="wide")
    sidebar_bg_color = """
    <style>
    [data-testid="stSidebar"] {
        background-color: #2eafa2;  /* Replace with your custom color */
    }
    </style>
    """
    
    sidebar_css = """
    <style>
    [data-testid="stSidebar"] {
        position: relative; /* Ensure the sidebar is positioned relative for absolute children */
        background-color: #1f1f1f; /* Example background color */
        background-image: url('https://your-image-url.com/background.jpg'); /* Example background image */
        background-size: cover; /* Ensure the image covers the entire sidebar */
    }
    .sidebar-logo {
        position: relative;
        bottom: 0px; /* Distance from the bottom */
        left: 50%;
        transform: translateX(-50%); /* Center the logo horizontally */
        width: 20px; /* Adjust the width as needed */
        height: auto; /* Maintain the aspect ratio */
    }
    </style>
    """
    # change folder
    logo_path = "Final_logo_ver_1_white-01.png"  
    image = Image.open(logo_path)   
    
    
    st.markdown(sidebar_css, unsafe_allow_html=True)
    st.sidebar.image(image, use_column_width=False, width=300)
    
    st.markdown(sidebar_bg_color, unsafe_allow_html=True)
    st.sidebar.title(f"Welcome, {st.session_state.get('user', 'User')}")
    empno = st.session_state['emp_no']
    empno = str(empno)
    empno = empno.strip(".0")
    st.sidebar.header(f"Emp No: {empno}")
    user = st.session_state.get('user', 'User')
    if 'user' in st.session_state:
        user = st.session_state['user']
        # change folder
        file_path = f"{user}.xlsx"
        if os.path.exists(file_path):
            table = pd.read_excel(file_path)
            
        else:
            st.write("No data found for the user")
    #designation = ['Designation']
    if st.session_state['designation'] =="Manager" or st.session_state['designation'] =="Assistant Manager":
        
        menu_choice = st.sidebar.selectbox("Menu", ["Existing data","Single entry", "Multiple entries", "Sync", "Upload", "Report", "Team Report", "Edit entry", "Logout"])
    
        if menu_choice == "Existing data":
            if os.path.exists(file_path):
                table = pd.read_excel(file_path)
                #table = pd.DataFrame(data)
                table['Hours'] = table['Hours'].round(2)
                table['Hours'] = table['Hours'].map('{:.2f}'.format)
                table['Date'] = pd.to_datetime(table['Date'])
                table['Date'] = pd.to_datetime(table['Date']).dt.strftime('%m/%d/%Y')
                table['From'] = pd.to_datetime(table["From"]).dt.strftime('%H:%M')
                table['To'] = pd.to_datetime(table["To"]).dt.strftime('%H:%M')
                table['Emp No'] = table['Emp No'].astype(str)
                c1, c2 = st.columns(2)
                with c1:
                    st.write("Existing Data:")
                with c2:
                    if st.button("Download Complete file"):
                        # change folder
                        #file_path_2 = f"C:\\Users\\PC 1\\Downloads\\{user}.xlsx"
                        #table.to_excel(file_path_2, index=False)
                        if st.download_button("Download Complete file", file_name=f"{user}.xlsx"):
                            st.success('Data downloaded successfully!')
                        else:
                            st.error("Download Fail")

                selected_df = st.selectbox("Select data to view", options=["Last 10 entries", "Last 50 entries", "Complete entries"])
                if selected_df == "Last 10 entries":
                    st.table(table.tail(10))
                elif selected_df == "Last 50 entries":
                    st.table(table.tail(50))
                else:
                    st.table(table)
            else:
                st.write("")
                #st.write(designation.item)
        
        
        if menu_choice == "Single entry":
            st.header("Single Entry")
            
            col2 = st.container()

            date = st.date_input('Select Date')

            client_name = st.selectbox("Client Name", options=clients['ClientName'])

            Charg_none = st.selectbox('Entity',options=['Reckoner','BKL'])

            type = st.selectbox('Type', options=["Chargeable", "None-Charg"])

            a1, a2 = st.columns(2)
            with a1:
                input_from = st.text_input("From", value=st.session_state.get('input_from', ''))
            with a2:
                if st.button('From'):
                    current_time_from = datetime.now().strftime('%H:%M')
                    st.session_state['input_from'] = current_time_from
            b1, b2 = st.columns(2)
            with b1:
                input_to = st.text_input("To", value=st.session_state.get('input_to', ''))
            with b2:
                if st.button('To'):
                    current_time_to = datetime.now().strftime('%H:%M')
                    st.session_state['input_to'] = current_time_to
            if input_from and input_to:
                try:
                    
                    time_from = datetime.strptime(input_from, '%H:%M')
                    time_to = datetime.strptime(input_to, '%H:%M')

                    time_difference = round((time_to - time_from).total_seconds() / 3600,2)

                    if time_difference < 0:
                        time_difference += 24

                    st.metric(label="Total Hours", value=time_difference)
                except ValueError:
                    st.write("Please enter valid time values in HH:MM format.")
            else:
                st.text_input("Hours")

            toa = st.selectbox("Type of assignment", options=TOA['Type of assignment'])

            workarea = st.selectbox("Work Area", options=work_area['Work Area'])

            workdone = st.text_area("Work done")
            
            st.container()
            if 'table' not in st.session_state:
                st.session_state['table'] = pd.DataFrame(columns=[
                    "Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"
                ])

            st.container()
            
            if st.button("Save"):

                new_entry = pd.DataFrame({
                            "Name": [user],
                            "Entity": [Charg_none],
                            "Type": [type],
                            "Date": [date],
                            "From": [input_from],
                            "To": [input_to],
                            "Hours": [time_difference],
                            "Client Name": [client_name],
                            "Type of assignment": [toa],
                            "Work Area": [workarea],
                            "Work done": [workdone],
                            "Emp No": [empno]
                        })

                columns = ["Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"]
                new_entry = new_entry[columns]
                
                if os.path.exists(file_path):
                    existing_data = pd.read_excel(file_path)
                    existing_data.reset_index(drop=True, inplace=True)
                    updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
                else:
                    updated_data = new_entry

                updated_data.to_excel(file_path, index=False)
                st.success('Data saved successfully!')
            
            if st.button("Refresh"):
                if os.path.exists(file_path):

                    refreshed_data = pd.read_excel(file_path)
                    st.table(refreshed_data.tail(5))
                else:
                    st.write("No file exists")


        elif menu_choice == "Multiple entries":
            
            def process_entries(entries_text):
                entries = entries_text.splitlines()
                entries = [entry for entry in entries if entry.strip()]
                data = []

                for entry in entries:

                    s_replaced = re.sub(r'[\t]+', ',', entry)
                    s_replaced = re.sub(r'(?<=\S) {2,}(?=\S)', ',', s_replaced)

                    parts = s_replaced.split(',', 11)
                    hour_pattern = r'^\d{1,2}\.\d{1,2}$'

                    if re.match(hour_pattern, str(parts[4])):
                        parts = parts[:4] + ['00:00', '00:00'] + parts[4:]
                        #st.write((parts[9]))
                        client_and_work_done = parts[11].split(',', 1)
                        parts = parts[:11] + client_and_work_done

                    elif len(parts) == 10:
                        client_and_work_done = parts[11].split(',', 1)
                        st.write(client_and_work_done)
                        parts = parts[:11] + client_and_work_done

                    while len(parts) < 12:
                        parts.append('')

                    data.append(parts)

                columns = ["Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"]
                df = pd.DataFrame(data, columns=columns)
                return df

            st.header("Multiple Entries")
            Entire_entry = st.text_area("Paste full entry")

            if st.button("Process it"):
                df = process_entries(Entire_entry)
                st.write(df)

                st.session_state['processed_df'] = df

            if 'processed_df' in st.session_state:
                df = st.session_state['processed_df']
                
                if st.button("Save"):
                    # change folder
                    file_path = f"{user}.xlsx"  
                    
                    if os.path.exists(file_path):
                        existing_data = pd.read_excel(file_path)
                        updated_data = pd.concat([existing_data, df], ignore_index=True)
                    else:
                        updated_data = df

                    updated_data.to_excel(file_path, index=False)
                    st.success('Data saved successfully!')

        elif menu_choice == "Sync":
            try:
                new_file = st.text_input("Enter the path to original file")
                # change folder
                file_path = f"{user}.xlsx"  
                new_file = new_file.strip().strip('"').strip("'")
                df_1 = pd.read_excel(file_path)
                df_2 = pd.read_excel(new_file)
                new_entries = df_2[~df_2.index.isin(df_1.index)]
                df_1_updated = pd.concat([df_1, new_entries], ignore_index=False)
                st.write(f"Number of entries before sync: {len(df_1)}")
                st.write(f"Number of new entries added: {len(new_entries)}")
                st.write(f"Number of entries after sync: {len(df_1_updated)}")
                if st.button("Sync"):
                    df_1_updated.to_excel(file_path, index=False)
                    st.write("Sync Successful")
            except:
                st.write("Please enter the path to the original file")
            

            

        elif menu_choice == "Upload":
            st.header("Upload")
            uploaded_file = st.file_uploader("Choose a file", type=["xlsx"])

            # change folder
            file_path = f"{user}.xlsx"    

            if uploaded_file is not None:
                if os.path.exists(file_path):
                    os.remove(file_path)  
                    st.info(f"Existing file {file_path} deleted.")
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"File saved as {file_path}")


        elif menu_choice == "Report":
            page_bg_css = '''
            <style>
            .stApp {
                background-color: black;
                color: white;  /* Set default text color to white */
            }
            </style>
            '''

            st.markdown(page_bg_css, unsafe_allow_html=True)
            plotly_layout = {
                'paper_bgcolor': 'black',  
                'plot_bgcolor': 'black',   
                'font': {
                    'color': 'white'       
                }
            }
            # change folder
            file_path = f"D:\\Timesheets\\app\\{user}.xlsx"  
            dataset = pd.read_excel(file_path)


            dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')

            dataset = dataset.dropna(subset=['Date'])

            current_month = datetime.now().month
            current_year = datetime.now().year

            dataset['Year_Month'] = dataset['Date'].dt.to_period('M')  

            available_months = dataset['Year_Month'].unique()

            default_month = pd.Period(f'{current_year}-{current_month:02d}', freq='M')
            if default_month not in available_months:
                default_month = available_months.max()  

            st.markdown("<p style='color: white; font-family: Bell MT;'>Select Month</p>", unsafe_allow_html=True)

            selected_month = st.selectbox(
                'Select Month',  
                options=available_months,
                index=list(available_months).index(default_month),
                label_visibility='collapsed'  
            )

            dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce').dt.strftime('%m/%d/%Y')
            filtered_data = dataset[dataset['Year_Month'] == selected_month]

            grouped_data = filtered_data.groupby('Entity')['Hours'].sum().reset_index()
            grouped_toa = filtered_data.groupby('Type of assignment')['Hours'].sum().reset_index()
            grouped_clients = filtered_data.groupby(['Client Name', 'Entity', 'Type of assignment'])['Hours'].sum().reset_index()
            grouped_clients_2 = filtered_data.groupby(['Client Name', 'Entity', 'Type'])['Hours'].sum().reset_index()
            charg_hours_entity = filtered_data.groupby(['Entity', 'Type'])['Hours'].sum().reset_index()

            st.markdown(
                "<h1 style='color: white; font-family: Bell MT;'>Monthly Performance Report</h1>", 
                unsafe_allow_html=True
            )
            
            
            z1, z2, z3 = st.columns(3)
            with z1:
                if grouped_data.shape[0] > 1:  # Check if there are at least 2 rows
                    entity_2 = round(grouped_data.iloc[1, 1], 2)
                else:
                    entity_2 = 0  # Or set a default value or handle accordingly
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=entity_2,
                    title={'text': "Reckoner Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                    gauge={
                        'axis': {'range': [0, 180], 'tickcolor': 'white'},
                        'bar': {'color': "#2eafa2", 'thickness': 0.9},
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.85}
                    }
                ))
                fig.update_layout(plotly_layout)  
                st.plotly_chart(fig, use_container_width=True)

            with z2:
                entity_1 = round(grouped_data.iloc[0, 1], 2)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=entity_1,
                    title={'text': "BKL Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                    gauge={
                        'axis': {'range': [0, 180], 'tickcolor': 'white'},
                        'bar': {'color': "#2eafa2", 'thickness': 0.9},
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                    }
                ))
                fig.update_layout(plotly_layout)  
                st.plotly_chart(fig, use_container_width=True)

                with z3:
                    dataset['Date'] = pd.to_datetime(dataset['Date'], format='%m/%d/%Y')
                    working_dataset = dataset[dataset['Date'].dt.month == selected_month.month]
                    days = len(working_dataset[working_dataset['Entity'].notnull()]['Date'].dt.date.unique())
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=days,
                        title={'text': "Working Days", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                        gauge={
                            'axis': {'range': [0, 31], 'tickcolor': 'white'},
                            'bar': {'color': "#2eafa2", 'thickness': 0.9},
                            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                        }
                    ))
                    
                    fig.update_layout(plotly_layout)  
                    st.plotly_chart(fig, use_container_width=True)

            v1, v2 = st.columns(2)
            with v1:
                
                no_clients = len(grouped_clients['Client Name'].unique())
                
                st.markdown(
                    f"""
                    <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                        <h2 style="font-size: 2.0em; text-align: center; font-family: 'Bell MT';">
                            <span style="color: white;">Clients: </span> 
                            <span style="color: #2eafa2;">{no_clients}</span>
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with v2:
                
                no_tasks = len(grouped_clients['Type of assignment'].unique())
                
                st.markdown(
                    f"""
                    <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                        <h2 style="font-size: 2.0em; text-align: center;font-family: 'Bell MT';">
                            <span style="color: white;">Type of assignments: </span> 
                            <span style="color: #2eafa2;">{no_tasks}</span>
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.container()
            #x1, x2 = st.columns([2,1])
            #with x1:
                #st.header("Client hours")
            def style_table(df):
                return df.style.format(
                    {'Hours': '{:.2f}'}  # Ensure Hours is displayed with 2 decimal places
                ).set_properties(
                    **{
                        'background-color': 'black',
                        'color': 'white',
                        'border-color': 'white',
                        'width': '100%'
                    }
                )
            charg_hours_entity['Hours'] = charg_hours_entity['Hours'].round(2)
            styled_table_1 = style_table(charg_hours_entity)
            st.write(styled_table_1.to_html(), unsafe_allow_html=True)
            st.write("-------------------------------------------")
            grouped_clients_2['Hours'] = grouped_clients_2['Hours'].round(2)
            styled_table = style_table(grouped_clients_2)

            st.write(styled_table.to_html(), unsafe_allow_html=True)

            
                #st.write(grouped_clients)
            #with x2:
            plotly_layout_1 = {
            'paper_bgcolor': 'black',  
            'plot_bgcolor': 'black',   
            'font': {
                'color': 'white'       
            },
            'xaxis': {
                'tickfont': {'color': 'white'}, 
                'title': {'font': {'color': 'white'}},  
                'gridcolor': 'gray'     
            },
            'yaxis': {
                'tickfont': {'color': 'white'},  
                'title': {'font': {'color': 'white'}},  
                'gridcolor': 'gray'     
            },
            'title': {
                'font': {'color': 'white'}  
            },
            'legend': {
                'font': {'color': 'white'},  
                'bgcolor': 'black'           
            }
        }
            fig = px.bar(
                    working_dataset,
                    x="Date",
                    y="Hours",
                    color="Entity",
                    title="Hours by Clients",
                )
            fig.update_xaxes(
                tickmode='linear',  # Ensure linear spacing between ticks
                dtick='D',          # Set tick interval to one day
            )
            fig.update_layout(plotly_layout_1)
            st.plotly_chart(fig, use_container_width=True)
            
            st.container()
            altair_theme = {
                'config': {
                    'background': 'black',
                    'title': {'color': 'white'},
                    'axis': {
                        'labelColor': 'white',
                        'titleColor': 'white',
                        'gridColor': 'gray'
                    },
                    'legend': {'labelColor': 'white', 'titleColor': 'white'}
                }
            }

            alt.themes.register('custom_theme', lambda: altair_theme)
            alt.themes.enable('custom_theme')
            filtered = working_dataset.groupby(['Client Name', 'Date'], as_index=False)['Hours'].sum()


            scatter_plot = alt.Chart(filtered).mark_circle().encode(
                x=alt.X('yearmonthdate(Date):T', title='Date'),
                y='Hours:Q',
                color=alt.Color('Client Name:N', legend=None),
                size='Hours:Q',
                tooltip=['Client Name:N', 'Date:T', 'Hours:Q']
            ).properties(
                title='Daily Hours Charged per Client'
            )

            st.altair_chart(scatter_plot, use_container_width=True)

            st.container()
            filtereddf = working_dataset.groupby(['Entity', 'Date'], as_index=False)['Hours'].sum()
            line_chart = alt.Chart(filtereddf).mark_line().encode(
                x=alt.X('yearmonthdate(Date):T', title='Date'),
                y='Hours:Q',
                color='Entity:N'
            ).properties(
                title='Daily Hours Charged per Entity'
            )
            points = line_chart.mark_point().encode(
                x=alt.X('yearmonthdate(Date):T', title='Date'),
                y='Hours:Q',
                color='Entity:N'
            )
            chart_with_points = line_chart + points
            st.altair_chart(chart_with_points, use_container_width=True)

        elif menu_choice == "Team Report":
                page_bg_css = '''
                <style>
                .stApp {
                    background-color: black;
                    color: white;  /* Set default text color to white */
                }
                </style>
                '''

                st.markdown(page_bg_css, unsafe_allow_html=True)
                plotly_layout = {
                    'paper_bgcolor': 'black',  
                    'plot_bgcolor': 'black',   
                    'font': {
                        'color': 'white'       
                    }
                }
                filtered_users = users[users['Manager']==st.session_state['user']]
                st.markdown("<p style='color: white; font-family: Bell MT;'>Select Team Member</p>", unsafe_allow_html=True)
                selected_name = st.selectbox(
                    'Select Team Member',  
                    options=filtered_users['Full Name'],
                    
                    label_visibility='collapsed'  
                )
                try:
                    user_1 = filtered_users[filtered_users['Full Name'] == selected_name]
                    s_1 = user_1['Username'].item()
                except:
                    st.write("")
                try:
                    # change folder
                    file_path = f"{s_1}.xlsx"  
                    
                    dataset = pd.read_excel(file_path)
                    dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')

                    dataset = dataset.dropna(subset=['Date'])

                    current_month = datetime.now().month
                    current_year = datetime.now().year

                    dataset['Year_Month'] = dataset['Date'].dt.to_period('M')  

                    available_months = dataset['Year_Month'].unique()

                    default_month = pd.Period(f'{current_year}-{current_month:02d}', freq='M')
                    if default_month not in available_months:
                        default_month = available_months.max()  

                    st.markdown("<p style='color: white; font-family: Bell MT;'>Select Month</p>", unsafe_allow_html=True)

                    selected_month = st.selectbox(
                        'Select Month',  
                        options=available_months,
                        index=list(available_months).index(default_month),
                        label_visibility='collapsed'  
                    )

                    dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce').dt.strftime('%m/%d/%Y')
                    filtered_data = dataset[dataset['Year_Month'] == selected_month]

                    grouped_data = filtered_data.groupby('Entity')['Hours'].sum().reset_index()
                    grouped_toa = filtered_data.groupby('Type of assignment')['Hours'].sum().reset_index()
                    grouped_clients = filtered_data.groupby(['Client Name', 'Entity', 'Type of assignment'])['Hours'].sum().reset_index()
                    grouped_clients_2 = filtered_data.groupby(['Client Name', 'Entity', 'Type'])['Hours'].sum().reset_index()
                    charg_hours_entity = filtered_data.groupby(['Entity', 'Type'])['Hours'].sum().reset_index()
                    
                    st.markdown(
                        "<h1 style='color: white; font-family: Bell MT;'>Monthly Performance Report</h1>", 
                        unsafe_allow_html=True
                    )
            
            
                    z1, z2, z3 = st.columns(3)
                    with z1:
                        if grouped_data.shape[0] > 1:  # Check if there are at least 2 rows
                            entity_2 = round(grouped_data.iloc[1, 1], 2)
                        else:
                            entity_2 = 0  # Or set a default value or handle accordingly
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=entity_2,
                            title={'text': "Reckoner Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                            gauge={
                                'axis': {'range': [0, 180], 'tickcolor': 'white'},
                                'bar': {'color': "#2eafa2", 'thickness': 0.9},
                                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.85}
                            }
                        ))
                        fig.update_layout(plotly_layout)  
                        st.plotly_chart(fig, use_container_width=True)

                    with z2:
                        entity_1 = round(grouped_data.iloc[0, 1], 2)
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=entity_1,
                            title={'text': "BKL Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                            gauge={
                                'axis': {'range': [0, 180], 'tickcolor': 'white'},
                                'bar': {'color': "#2eafa2", 'thickness': 0.9},
                                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                            }
                        ))
                        fig.update_layout(plotly_layout)  
                        st.plotly_chart(fig, use_container_width=True)

                        with z3:
                            dataset['Date'] = pd.to_datetime(dataset['Date'], format='%m/%d/%Y')
                            working_dataset = dataset[dataset['Date'].dt.month == selected_month.month]
                            days = len(working_dataset[working_dataset['Entity'].notnull()]['Date'].dt.date.unique())
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=days,
                                title={'text': "Working Days", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                                gauge={
                                    'axis': {'range': [0, 31], 'tickcolor': 'white'},
                                    'bar': {'color': "#2eafa2", 'thickness': 0.9},
                                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                                }
                            ))
                            
                            fig.update_layout(plotly_layout)  
                            st.plotly_chart(fig, use_container_width=True)

                    v1, v2 = st.columns(2)
                    with v1:
                        
                        no_clients = len(grouped_clients['Client Name'].unique())
                        
                        st.markdown(
                            f"""
                            <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                                <h2 style="font-size: 2.0em; text-align: center; font-family: 'Bell MT';">
                                    <span style="color: white;">Clients: </span> 
                                    <span style="color: #2eafa2;">{no_clients}</span>
                                </h2>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                    with v2:
                        
                        no_tasks = len(grouped_clients['Type of assignment'].unique())
                        
                        st.markdown(
                            f"""
                            <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                                <h2 style="font-size: 2.0em; text-align: center;font-family: 'Bell MT';">
                                    <span style="color: white;">Type of assignments: </span> 
                                    <span style="color: #2eafa2;">{no_tasks}</span>
                                </h2>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.container()
                    #x1, x2 = st.columns([2,1])
                    #with x1:
                        #st.header("Client hours")
                    def style_table(df):
                        return df.style.format(
                            {'Hours': '{:.2f}'}  # Ensure Hours is displayed with 2 decimal places
                        ).set_properties(
                            **{
                                'background-color': 'black',
                                'color': 'white',
                                'border-color': 'white',
                                'width': '100%'
                            }
                        )
                    charg_hours_entity['Hours'] = charg_hours_entity['Hours'].round(2)
                    styled_table_1 = style_table(charg_hours_entity)
                    st.write(styled_table_1.to_html(), unsafe_allow_html=True)
                    st.write("-------------------------------------------")
                    grouped_clients_2['Hours'] = grouped_clients_2['Hours'].round(2)
                    styled_table = style_table(grouped_clients_2)

                    st.write(styled_table.to_html(), unsafe_allow_html=True)

                    
                        #st.write(grouped_clients)
                    #with x2:
                    plotly_layout_1 = {
                    'paper_bgcolor': 'black',  
                    'plot_bgcolor': 'black',   
                    'font': {
                        'color': 'white'       
                    },
                    'xaxis': {
                        'tickfont': {'color': 'white'}, 
                        'title': {'font': {'color': 'white'}},  
                        'gridcolor': 'gray'     
                    },
                    'yaxis': {
                        'tickfont': {'color': 'white'},  
                        'title': {'font': {'color': 'white'}},  
                        'gridcolor': 'gray'     
                    },
                    'title': {
                        'font': {'color': 'white'}  
                    },
                    'legend': {
                        'font': {'color': 'white'},  
                        'bgcolor': 'black'           
                    }
                }
                    fig = px.bar(
                            working_dataset,
                            x="Date",
                            y="Hours",
                            color="Entity",
                            title="Hours by Clients",
                        )
                    fig.update_xaxes(
                        tickmode='linear',  # Ensure linear spacing between ticks
                        dtick='D',          # Set tick interval to one day
                    )
                    fig.update_layout(plotly_layout_1)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.container()
                    altair_theme = {
                        'config': {
                            'background': 'black',
                            'title': {'color': 'white'},
                            'axis': {
                                'labelColor': 'white',
                                'titleColor': 'white',
                                'gridColor': 'gray'
                            },
                            'legend': {'labelColor': 'white', 'titleColor': 'white'}
                        }
                    }

                    alt.themes.register('custom_theme', lambda: altair_theme)
                    alt.themes.enable('custom_theme')
                    filtered = working_dataset.groupby(['Client Name', 'Date'], as_index=False)['Hours'].sum()


                    scatter_plot = alt.Chart(filtered).mark_circle().encode(
                        x=alt.X('yearmonthdate(Date):T', title='Date'),
                        y='Hours:Q',
                        color=alt.Color('Client Name:N', legend=None),
                        size='Hours:Q',
                        tooltip=['Client Name:N', 'Date:T', 'Hours:Q']
                    ).properties(
                        title='Daily Hours Charged per Client'
                    )

                    st.altair_chart(scatter_plot, use_container_width=True)

                    st.container()
                    filtereddf = working_dataset.groupby(['Entity', 'Date'], as_index=False)['Hours'].sum()
                    line_chart = alt.Chart(filtereddf).mark_line().encode(
                        x=alt.X('yearmonthdate(Date):T', title='Date'),
                        y='Hours:Q',
                        color='Entity:N'
                    ).properties(
                        title='Daily Hours Charged per Entity'
                    )
                    points = line_chart.mark_point().encode(
                        x=alt.X('yearmonthdate(Date):T', title='Date'),
                        y='Hours:Q',
                        color='Entity:N'
                    )
                    chart_with_points = line_chart + points
                    st.altair_chart(chart_with_points, use_container_width=True)
                except:
                    st.success("No Team member found")


                

        elif menu_choice == "Edit entry":
            st.header("Edit Entry")
            # change folder
            file_path = f"{user}.xlsx"    
            entities = ['BKL', 'Reckoner']

            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                df['Date'] = pd.to_datetime(df['Date'])  

                selected_date = st.date_input("Select Date", key="selected_date")

                filtered_df = df[df['Date'] == pd.to_datetime(selected_date)]
                
                if not filtered_df.empty:
                    st.write(f"Entries for {selected_date}:")
                    st.write(filtered_df.reset_index(drop=True))  

                    index_to_edit = st.number_input("Enter index number to edit", min_value=0, max_value=len(filtered_df)-1, key="index_to_edit")

                    if st.button("Edit"):
                        st.session_state.entry_to_edit = filtered_df.iloc[index_to_edit]
                    
                    if "entry_to_edit" in st.session_state:
                        entry_to_edit = st.session_state.entry_to_edit

                        edited_name = st.text_input("Name", entry_to_edit['Name'])

                        edited_entity = st.selectbox("Entity", options=entities, index=entities.index(entry_to_edit['Entity']))
                        
                        edited_date = st.date_input("Date", value=entry_to_edit['Date'])
                        edited_from = st.text_input("From", entry_to_edit['From'])
                        edited_to = st.text_input("To", entry_to_edit['To'])
                        edited_hours = st.text_input("Hours", entry_to_edit['Hours'])

                        edited_client_name = st.selectbox("Client Name", options=clients['ClientName'], index=clients['ClientName'].tolist().index(entry_to_edit['Client Name']))
                        
                        edited_assignment_type = st.selectbox("Type of Assignment", options=TOA['Type of assignment'], index=TOA['Type of assignment'].tolist().index(entry_to_edit['Type of assignment']))
                        edited_work_area = st.selectbox("Work Area", options=work_area['Work Area'], index=work_area['Work Area'].tolist().index(entry_to_edit['Work Area']))
                        edited_work_done = st.text_area("Work done", entry_to_edit['Work done'])

                        if st.button("Save Changes"):

                            df.loc[filtered_df.index[index_to_edit], 'Name'] = edited_name
                            df.loc[filtered_df.index[index_to_edit], 'Entity'] = edited_entity
                            df.loc[filtered_df.index[index_to_edit], 'Date'] = pd.to_datetime(edited_date)
                            df.loc[filtered_df.index[index_to_edit], 'From'] = edited_from
                            df.loc[filtered_df.index[index_to_edit], 'To'] = edited_to
                            df.loc[filtered_df.index[index_to_edit], 'Hours'] = edited_hours
                            df.loc[filtered_df.index[index_to_edit], 'Client Name'] = edited_client_name
                            df.loc[filtered_df.index[index_to_edit], 'Type of assignment'] = edited_assignment_type
                            df.loc[filtered_df.index[index_to_edit], 'Work Area'] = edited_work_area
                            df.loc[filtered_df.index[index_to_edit], 'Work done'] = edited_work_done

                            df.to_excel(file_path, index=False)
                            st.success("Entry updated successfully!")
                            del st.session_state.entry_to_edit  

                else:
                    st.error("Data file not found.")
        elif menu_choice == "Logout":
                st.session_state['authenticated'] = False
                st.session_state['user'] = None
                st.rerun()
    
    #elif st.session_state['designation'] =="IT Adminstrator":
        #menu_choice = st.sidebar.selectbox("Menu", ["Existing data","Single entry", "Sync", "Report", "Edit entry", "Update Client's list", "Amend Users", "Logout"])

    elif st.session_state['designation'] !="Manager" or st.session_state['designation'] !="Assistant Manager":
        menu_choice = st.sidebar.selectbox("Menu", ["Existing data","Single entry", "Multiple entries", "Report", "Edit entry", "Logout"])
    
        if menu_choice == "Existing data":
            if os.path.exists(file_path):
                table = pd.read_excel(file_path)
                #table = pd.DataFrame(data)
                table['Hours'] = table['Hours'].round(2)
                table['Hours'] = table['Hours'].map('{:.2f}'.format)
                table['Date'] = pd.to_datetime(table['Date'])
                table['Date'] = pd.to_datetime(table['Date']).dt.strftime('%m/%d/%Y')
                table['From'] = pd.to_datetime(table["From"]).dt.strftime('%H:%M')
                table['To'] = pd.to_datetime(table["To"]).dt.strftime('%H:%M')
                table['Emp No'] = table['Emp No'].astype(str)
                c1, c2 = st.columns(2)
                with c1:
                    st.write("Existing Data:")
                with c2:
                    if st.button("Download Complete file"):
                        # change folder
                        #file_path_2 = f"C:\\Users\\PC 1\\Downloads\\{user}.xlsx"
                        #table.to_excel(file_path_2, index=False)
                        if st.download_button("Download Complete file", file_name="f{user}.xlsx"):
                                              st.success("Download Successful")
                        else:
                                              
                                              st.error('Download Fail!')

                selected_df = st.selectbox("Select data to view", options=["Last 10 entries", "Last 50 entries", "Complete entries"])
                if selected_df == "Last 10 entries":
                    st.table(table.tail(10))
                elif selected_df == "Last 50 entries":
                    st.table(table.tail(50))
                else:
                    st.table(table)
            else:
                st.write("")
                #st.write(designation.item)
        
        
        if menu_choice == "Single entry":
            st.header("Single Entry")
            
            col2 = st.container()

            date = st.date_input('Select Date')

            client_name = st.selectbox("Client Name", options=clients['ClientName'])

            Charg_none = st.selectbox('Entity',options=['Reckoner','BKL'])

            type = st.selectbox('Type', options=["Chargeable", "None-Charg"])

            a1, a2 = st.columns(2)
            with a1:
                input_from = st.text_input("From", value=st.session_state.get('input_from', ''))
            with a2:
                if st.button('From'):
                    current_time_from = datetime.now().strftime('%H:%M')
                    st.session_state['input_from'] = current_time_from
            b1, b2 = st.columns(2)
            with b1:
                input_to = st.text_input("To", value=st.session_state.get('input_to', ''))
            with b2:
                if st.button('To'):
                    current_time_to = datetime.now().strftime('%H:%M')
                    st.session_state['input_to'] = current_time_to
            if input_from and input_to:
                try:
                    
                    time_from = datetime.strptime(input_from, '%H:%M')
                    time_to = datetime.strptime(input_to, '%H:%M')

                    time_difference = round((time_to - time_from).total_seconds() / 3600,2)

                    if time_difference < 0:
                        time_difference += 24

                    st.metric(label="Total Hours", value=time_difference)
                except ValueError:
                    st.write("Please enter valid time values in HH:MM format.")
            else:
                st.text_input("Hours")

            toa = st.selectbox("Type of assignment", options=TOA['Type of assignment'])

            workarea = st.selectbox("Work Area", options=work_area['Work Area'])

            workdone = st.text_area("Work done")
            
            st.container()
            if 'table' not in st.session_state:
                st.session_state['table'] = pd.DataFrame(columns=[
                    "Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"
                ])

            st.container()
            
            if st.button("Save"):

                new_entry = pd.DataFrame({
                            "Name": [user],
                            "Entity": [Charg_none],
                            "Type": [type],
                            "Date": [date],
                            "From": [input_from],
                            "To": [input_to],
                            "Hours": [time_difference],
                            "Client Name": [client_name],
                            "Type of assignment": [toa],
                            "Work Area": [workarea],
                            "Work done": [workdone],
                            "Emp No": [empno]
                        })

                columns = ["Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"]
                new_entry = new_entry[columns]
                
                if os.path.exists(file_path):
                    existing_data = pd.read_excel(file_path)
                    existing_data.reset_index(drop=True, inplace=True)
                    updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
                else:
                    updated_data = new_entry

                updated_data.to_excel(file_path, index=False)
                st.success('Data saved successfully!')
            
            if st.button("Refresh"):
                if os.path.exists(file_path):

                    refreshed_data = pd.read_excel(file_path)
                    st.table(refreshed_data.tail(5))
                else:
                    st.write("No file exists")


        elif menu_choice == "Multiple entries":
            
            def process_entries(entries_text):
                entries = entries_text.splitlines()
                entries = [entry for entry in entries if entry.strip()]
                data = []

                for entry in entries:

                    s_replaced = re.sub(r'[\t]+', ',', entry)
                    s_replaced = re.sub(r'(?<=\S) {2,}(?=\S)', ',', s_replaced)

                    parts = s_replaced.split(',', 11)
                    hour_pattern = r'^\d{1,2}\.\d{1,2}$'

                    if re.match(hour_pattern, str(parts[4])):
                        parts = parts[:4] + ['00:00', '00:00'] + parts[4:]
                        #st.write((parts[9]))
                        client_and_work_done = parts[11].split(',', 1)
                        parts = parts[:11] + client_and_work_done

                    elif len(parts) == 10:
                        client_and_work_done = parts[11].split(',', 1)
                        st.write(client_and_work_done)
                        parts = parts[:11] + client_and_work_done

                    while len(parts) < 12:
                        parts.append('')

                    data.append(parts)

                columns = ["Name", "Entity", "Type", "Date", "From", "To", "Hours", "Client Name", "Type of assignment", "Work Area", "Work done", "Emp No"]
                df = pd.DataFrame(data, columns=columns)
                return df

            st.header("Multiple Entries")
            Entire_entry = st.text_area("Paste full entry")

            if st.button("Process it"):
                df = process_entries(Entire_entry)
                st.write(df)

                st.session_state['processed_df'] = df

            if 'processed_df' in st.session_state:
                df = st.session_state['processed_df']
                
                if st.button("Save"):
                    # change folder
                    file_path = f"{user}.xlsx"  
                    
                    if os.path.exists(file_path):
                        existing_data = pd.read_excel(file_path)
                        updated_data = pd.concat([existing_data, df], ignore_index=True)
                    else:
                        updated_data = df

                    updated_data.to_excel(file_path, index=False)
                    st.success('Data saved successfully!')

        elif menu_choice == "Report":
            try:
                page_bg_css = '''
                <style>
                .stApp {
                    background-color: black;
                    color: white;  /* Set default text color to white */
                }
                </style>
                '''

                st.markdown(page_bg_css, unsafe_allow_html=True)
                plotly_layout = {
                    'paper_bgcolor': 'black',  
                    'plot_bgcolor': 'black',   
                    'font': {
                        'color': 'white'       
                    }
                }
                # change folder
                file_path = f"{user}.xlsx" 
                dataset = pd.read_excel(file_path)


                dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')

                dataset = dataset.dropna(subset=['Date'])

                current_month = datetime.now().month
                current_year = datetime.now().year

                dataset['Year_Month'] = dataset['Date'].dt.to_period('M')  

                available_months = dataset['Year_Month'].unique()

                default_month = pd.Period(f'{current_year}-{current_month:02d}', freq='M')
                if default_month not in available_months:
                    default_month = available_months.max()  

                st.markdown("<p style='color: white; font-family: Bell MT;'>Select Month</p>", unsafe_allow_html=True)

                selected_month = st.selectbox(
                    'Select Month',  
                    options=available_months,
                    index=list(available_months).index(default_month),
                    label_visibility='collapsed'  
                )

                dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce').dt.strftime('%m/%d/%Y')
                filtered_data = dataset[dataset['Year_Month'] == selected_month]

                grouped_data = filtered_data.groupby('Entity')['Hours'].sum().reset_index()
                grouped_toa = filtered_data.groupby('Type of assignment')['Hours'].sum().reset_index()
                grouped_clients = filtered_data.groupby(['Client Name', 'Entity', 'Type of assignment'])['Hours'].sum().reset_index()
                grouped_clients_2 = filtered_data.groupby(['Client Name', 'Entity'])['Hours'].sum().reset_index()

                st.markdown(
                    "<h1 style='color: white; font-family: Bell MT;'>Monthly Performance Report</h1>", 
                    unsafe_allow_html=True
                )
                
                
                z1, z2, z3 = st.columns(3)
                with z1:
                    if grouped_data.shape[0] > 1:  # Check if there are at least 2 rows
                        entity_2 = round(grouped_data.iloc[1, 1], 2)
                    else:
                        entity_2 = 0  # Or set a default value or handle accordingly
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=entity_2,
                        title={'text': "Reckoner Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                        gauge={
                            'axis': {'range': [0, 180], 'tickcolor': 'white'},
                            'bar': {'color': "#2eafa2", 'thickness': 0.9},
                            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.85}
                        }
                    ))
                    fig.update_layout(plotly_layout)  
                    st.plotly_chart(fig, use_container_width=True)

                with z2:
                    entity_1 = round(grouped_data.iloc[0, 1], 2)
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=entity_1,
                        title={'text': "BKL Hours", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                        gauge={
                            'axis': {'range': [0, 180], 'tickcolor': 'white'},
                            'bar': {'color': "#2eafa2", 'thickness': 0.9},
                            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                        }
                    ))
                    fig.update_layout(plotly_layout)  
                    st.plotly_chart(fig, use_container_width=True)

                    with z3:
                        dataset['Date'] = pd.to_datetime(dataset['Date'], format='%m/%d/%Y')
                        working_dataset = dataset[dataset['Date'].dt.month == selected_month.month]
                        days = len(working_dataset[working_dataset['Entity'].notnull()]['Date'].dt.date.unique())
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=days,
                            title={'text': "Working Days", 'font': {'size': 32, 'color': 'white','family': 'Bell MT'}},
                            gauge={
                                'axis': {'range': [0, 31], 'tickcolor': 'white'},
                                'bar': {'color': "#2eafa2", 'thickness': 0.9},
                                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75}
                            }
                        ))
                        
                        fig.update_layout(plotly_layout)  
                        st.plotly_chart(fig, use_container_width=True)

                v1, v2 = st.columns(2)
                with v1:
                    
                    no_clients = len(grouped_clients['Client Name'].unique())
                    
                    st.markdown(
                        f"""
                        <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                            <h2 style="font-size: 2.0em; text-align: center; font-family: 'Bell MT';">
                                <span style="color: white;">Clients: </span> 
                                <span style="color: #2eafa2;">{no_clients}</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                with v2:
                    
                    no_tasks = len(grouped_clients['Type of assignment'].unique())
                    
                    st.markdown(
                        f"""
                        <div style="border: 0.5px solid #02d4d4; padding: 10px; border-radius: 5px;">
                            <h2 style="font-size: 2.0em; text-align: center;font-family: 'Bell MT';">
                                <span style="color: white;">Type of assignments: </span> 
                                <span style="color: #2eafa2;">{no_tasks}</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.container()
                #x1, x2 = st.columns([2,1])
                #with x1:
                    #st.header("Client hours")
                def style_table(df):
                    return df.style.format(
                        {'Hours': '{:.2f}'}  # Ensure Hours is displayed with 2 decimal places
                    ).set_properties(
                        **{
                            'background-color': 'black',
                            'color': 'white',
                            'border-color': 'white',
                            'width': '100%'
                        }
                    )

                grouped_clients_2['Hours'] = grouped_clients_2['Hours'].round(2)
                styled_table = style_table(grouped_clients_2)

                st.write(styled_table.to_html(), unsafe_allow_html=True)
                    #st.write(grouped_clients)
                #with x2:
                plotly_layout_1 = {
                'paper_bgcolor': 'black',  
                'plot_bgcolor': 'black',   
                'font': {
                    'color': 'white'       
                },
                'xaxis': {
                    'tickfont': {'color': 'white'}, 
                    'title': {'font': {'color': 'white'}},  
                    'gridcolor': 'gray'     
                },
                'yaxis': {
                    'tickfont': {'color': 'white'},  
                    'title': {'font': {'color': 'white'}},  
                    'gridcolor': 'gray'     
                },
                'title': {
                    'font': {'color': 'white'}  
                },
                'legend': {
                    'font': {'color': 'white'},  
                    'bgcolor': 'black'           
                }
            }
                fig = px.bar(
                        working_dataset,
                        x="Date",
                        y="Hours",
                        color="Entity",
                        title="Hours by Clients",
                    )
                fig.update_xaxes(
                    tickmode='linear',  # Ensure linear spacing between ticks
                    dtick='D',          # Set tick interval to one day
                )
                fig.update_layout(plotly_layout_1)
                st.plotly_chart(fig, use_container_width=True)
                
                st.container()
                altair_theme = {
                    'config': {
                        'background': 'black',
                        'title': {'color': 'white'},
                        'axis': {
                            'labelColor': 'white',
                            'titleColor': 'white',
                            'gridColor': 'gray'
                        },
                        'legend': {'labelColor': 'white', 'titleColor': 'white'}
                    }
                }

                alt.themes.register('custom_theme', lambda: altair_theme)
                alt.themes.enable('custom_theme')
                filtered = working_dataset.groupby(['Client Name', 'Date'], as_index=False)['Hours'].sum()


                scatter_plot = alt.Chart(filtered).mark_circle().encode(
                    x=alt.X('yearmonthdate(Date):T', title='Date'),
                    y='Hours:Q',
                    color=alt.Color('Client Name:N', legend=None),
                    size='Hours:Q',
                    tooltip=['Client Name:N', 'Date:T', 'Hours:Q']
                ).properties(
                    title='Daily Hours Charged per Client'
                )

                st.altair_chart(scatter_plot, use_container_width=True)

                st.container()
                filtereddf = working_dataset.groupby(['Entity', 'Date'], as_index=False)['Hours'].sum()
                line_chart = alt.Chart(filtereddf).mark_line().encode(
                    x=alt.X('yearmonthdate(Date):T', title='Date'),
                    y='Hours:Q',
                    color='Entity:N'
                ).properties(
                    title='Daily Hours Charged per Entity'
                )
                points = line_chart.mark_point().encode(
                    x=alt.X('yearmonthdate(Date):T', title='Date'),
                    y='Hours:Q',
                    color='Entity:N'
                )
                chart_with_points = line_chart + points
                st.altair_chart(chart_with_points, use_container_width=True)
            except:
                st.write("")

        elif menu_choice == "Edit entry":
            st.header("Edit Entry")
            # change folder
            file_path = f"{user}.xlsx"   
            entities = ['BKL', 'Reckoner']

            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                df['Date'] = pd.to_datetime(df['Date'])  

                selected_date = st.date_input("Select Date", key="selected_date")

                filtered_df = df[df['Date'] == pd.to_datetime(selected_date)]
                
                if not filtered_df.empty:
                    st.write(f"Entries for {selected_date}:")
                    st.write(filtered_df.reset_index(drop=True))  

                    index_to_edit = st.number_input("Enter index number to edit", min_value=0, max_value=len(filtered_df)-1, key="index_to_edit")

                    if st.button("Edit"):
                        st.session_state.entry_to_edit = filtered_df.iloc[index_to_edit]
                    
                    if "entry_to_edit" in st.session_state:
                        entry_to_edit = st.session_state.entry_to_edit

                        edited_name = st.text_input("Name", entry_to_edit['Name'])

                        edited_entity = st.selectbox("Entity", options=entities, index=entities.index(entry_to_edit['Entity']))
                        
                        edited_date = st.date_input("Date", value=entry_to_edit['Date'])
                        edited_from = st.text_input("From", entry_to_edit['From'])
                        edited_to = st.text_input("To", entry_to_edit['To'])
                        edited_hours = st.text_input("Hours", entry_to_edit['Hours'])

                        edited_client_name = st.selectbox("Client Name", options=clients['ClientName'], index=clients['ClientName'].tolist().index(entry_to_edit['Client Name']))
                        
                        edited_assignment_type = st.selectbox("Type of Assignment", options=TOA['Type of assignment'], index=TOA['Type of assignment'].tolist().index(entry_to_edit['Type of assignment']))
                        edited_work_area = st.selectbox("Work Area", options=work_area['Work Area'], index=work_area['Work Area'].tolist().index(entry_to_edit['Work Area']))
                        edited_work_done = st.text_area("Work done", entry_to_edit['Work done'])

                        if st.button("Save Changes"):

                            df.loc[filtered_df.index[index_to_edit], 'Name'] = edited_name
                            df.loc[filtered_df.index[index_to_edit], 'Entity'] = edited_entity
                            df.loc[filtered_df.index[index_to_edit], 'Date'] = pd.to_datetime(edited_date)
                            df.loc[filtered_df.index[index_to_edit], 'From'] = edited_from
                            df.loc[filtered_df.index[index_to_edit], 'To'] = edited_to
                            df.loc[filtered_df.index[index_to_edit], 'Hours'] = edited_hours
                            df.loc[filtered_df.index[index_to_edit], 'Client Name'] = edited_client_name
                            df.loc[filtered_df.index[index_to_edit], 'Type of assignment'] = edited_assignment_type
                            df.loc[filtered_df.index[index_to_edit], 'Work Area'] = edited_work_area
                            df.loc[filtered_df.index[index_to_edit], 'Work done'] = edited_work_done

                            df.to_excel(file_path, index=False)
                            st.success("Entry updated successfully!")
                            del st.session_state.entry_to_edit  
        elif menu_choice == "Logout":
                st.session_state['authenticated'] = False
                st.session_state['user'] = None
                st.rerun()
    else:
        st.error("Data file not found.")

            

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        authenticated_page()
    else:
        login()

if __name__ == "__main__":
    main()
