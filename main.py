import streamlit as st, mysql.connector as mysql
import reset, account_control, home, account_details, developers_info, contacts
from streamlit_option_menu import option_menu
import appInfo, app, pandas as pd, filterDF
from sqlalchemy import create_engine
st.set_page_config(page_title='PTTRS', page_icon='🧬', initial_sidebar_state='collapsed', layout="wide")
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if st.session_state.logged_in:
        display_main_page()
    else:
        login()

def login():
    config = {
    'user': 'u164935248_trial_pttrs',
    'password': 'Trial_pttrs1',
    'host': '89.117.157.103',
    'use_pure': True,
    'raise_on_warnings': True,
}
    connect2= mysql.connect(**config)
    cursor = connect2.cursor()
    try:
        cursor.execute("USE `u164935248_trial_pttrs`")
    except:
        print('Not Using u164935248_trial_pttrs')
    placeholder = st.empty()
    with placeholder.container():
        st.title("PTTRS Authentication")
        st.markdown("#")
        formOption = st.selectbox(
        "Login/Register/Reset",
        ('Login', 'Register', 'Reset Password'))
    if formOption == 'Login':
        st.markdown("#")
        with st.form("my_login"):
            st.subheader(':green[Login]')
            st.markdown('New users are requsted to register first!')
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            login__ = st.form_submit_button("Login")
            if login__:
                if len(username) > 0 or len(password) > 0:
                    foundusr, foundpass = '', ''
                    cursor.execute(f"SELECT uniqueusr FROM usr_info WHERE uniqueusr = '{username}' AND password = '{password}'")
                    try: beuser = cursor.fetchall()
                    except: pass
                    if len(beuser) > 0: 
                        foundusr = beuser[0][0]
                        cursor.execute(f"SELECT password FROM usr_info WHERE uniqueusr = '{username}' AND password = '{password}'")
                        try: foundpass = cursor.fetchall()[0][0]
                        except: pass
                    else: pass
                    if foundusr == username and password == foundpass:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Logged in successfully!")
                        st.experimental_rerun() 
                    else:
                        st.error("Invalid username or password. Please try again.")
                else: st.error("No username or password provided!")
    elif formOption == "Register":
        account_control.register()
    else:
        reset.reset()

def display_main_page():
    st.sidebar.subheader(f'Welcome {st.session_state.username}!')
    st.sidebar.markdown("######")
    with st.sidebar:
        selected = option_menu(
            menu_title = "PTTRS",
            options = ["Home", "Use PTTRS", "Patient Database", "Account Details", "App Info", "Developers Info", "Contact"],
            icons= ['house', "arrow-bar-right", "database", "person-square", "info-circle-fill", "info-square-fill", "send"]
        )
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun() 
    if selected == "Home":
        home.app()
    if selected == "Account Details":
        account_details.account_details(st.session_state.username)
    if selected == "Developers Info":
        developers_info.developers()
    if selected == "Contact":
        contacts.contacts(st.session_state.username)
    if selected == "App Info":
        appInfo.app_info()
    if selected == "Use PTTRS":
        config = {
        'user': 'u164935248_trial_pttrs',
        'password': 'Trial_pttrs1',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
        connect2 = mysql.connect(**config)
        cursor = connect2.cursor()
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute(f"SELECT regas FROM usr_info WHERE uniqueusr = '{st.session_state.username}'")
        getRegAs = cursor.fetchall()[0][0]
        if getRegAs == "Doctor":
            app.doctorWala(st.session_state.username)
        else:
            app.other()
    if selected == "Patient Database":
        config = {
        'user': 'u164935248_trial_pttrs',
        'password': 'Trial_pttrs1',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
        connect2 = mysql.connect(**config)
        cursor = connect2.cursor()
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute(f"SELECT regas FROM usr_info WHERE uniqueusr = '{st.session_state.username}'")
        getRegAs = cursor.fetchall()[0][0]
        # st.write(getRegAs)
        if getRegAs == "Doctor":
            st.header(":green[Your Patients Datbase]")
            st.write("###### **The Database is Sorted by Date, Patient ID, and Visit No. in Descending, Ascending, and Ascending Order Respectively.**")
            st.markdown("#####")
            engine = create_engine('mysql://u164935248_trial_pttrs:Trial_pttrs1@89.117.157.103/u164935248_trial_pttrs')
            pdf_ = pd.read_sql(f"SELECT * FROM `patient_data` WHERE uniqueusr = '{st.session_state.username}' ORDER BY date_time DESC, patient_id ASC, visit_no ASC", con=engine)
            pdf__ = pdf_.drop(["tb_key", "uniqueusr"], axis=1)
            colmapping = {
                 'patient_id' : 'Patitnt ID',
                  'visit_no' : 'Visit No.', 
                  'name' : 'Name',
                  'age': 'Age',
                   'gender': 'Gender',
                'blood_group': 'Blood Group',
                 'address': 'Address',
                  'state': 'State',
                   'pin': 'PIN',
                   'country_code': 'Country Code',
                    'country': 'Country',
                     'continent': 'Continent',
                       'contact_no': 'Contact No.',
                        'patient_tb_health': 'Patient TB Health',
                         'infection_age': 'Infection Age',
                          'treatment_status': 'Treatment_status', 
                          'medical_history': 'Medical History', 
                          'dst_done': 'DST Done',
                           'test_name': 'Test Name',
                            'known_amr_strain': 'Known AMR Strain', 
                            'amr_strain_resistant_drug': 'AMR_Strain_Resistant_Drug', 
                            'amc': 'AMCs', 
                            'selected_tb_drug': 'Selected TB Drug(s)', 
                            'selected_amc_drug': 'Selected AMC_Drug(s)',
                            'date_time': 'Date',
                            'next_visit' : 'Next Visit' 
                                                    }
            pdf__ = pdf__.rename(columns=colmapping)
            st.dataframe(filterDF.filter_dataframe(pdf__))    
        else:
            st.header(":red[You don't have any access to patient database.]")
            st.markdown("#####")
            st.info("Patient database is only for doctors to access their patient details. Other than any doctors it's usage is strictly restricted.")

if __name__ == "__main__":
    main()
