import streamlit as st, mysql.connector as mysql
import streamlit_authenticator as stauth
import reset, account_control, home, account_details, developers_info, contacts
from streamlit_option_menu import option_menu
import appInfo, app, pandas as pd, filterDF
from sqlalchemy import create_engine
def auth():
    placeholder = st.empty()
    with placeholder.container():
        st.title("PTTRS Authentication")
        st.markdown("#")
        formOption = st.selectbox(
        "Login/Register/Reset",
        ('Login', 'Register', 'Reset Password'))
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
    cursor.execute("SELECT mail FROM usr_info")
    emails_ = cursor.fetchall()
    emails = [x[0] for x in emails_]
    cursor.execute("SELECT uniqueusr FROM usr_info")
    usernames_ = cursor.fetchall()
    usernames = [x[0] for x in usernames_]
    cursor.execute("SELECT hashed_password FROM usr_info")
    passwords_ = cursor.fetchall()
    passwords = [x[0] for x in passwords_]
    if formOption == "Login":
        credentials = {'usernames': {}}
        for index in range(len(emails)):
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
        Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
        email, authentication_status, username = Authenticator.login(':green[Login]\nNew users are requsted to register first!', 'main')
        # info, info1 = st.columns(1)
        if username:
            if username in usernames:
                if authentication_status:
                    # let User see app
                    placeholder.empty()
                    st.sidebar.subheader(f'Welcome {username}')
                    st.sidebar.markdown("######")
                    with st.sidebar:
                        selected = option_menu(
                            menu_title = "PTTRS",
                            options = ["Home", "Use PTTRS", "Patient Database", "Account Details", "App Info", "Developers Info", "Contact"],
                            icons= ['house', "arrow-bar-right", "database", "person-square", "info-circle-fill", "info-square-fill", "send"]
                        )
                    if selected == "Home":
                        home.app()
                    if selected == "Account Details":
                        account_details.account_details(username)
                    if selected == "Developers Info":
                        developers_info.developers()
                    if selected == "Contact":
                        contacts.contacts(username)
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
                        cursor.execute(f"SELECT regas FROM usr_info WHERE uniqueusr = '{username}'")
                        getRegAs = cursor.fetchall()[0][0]
                        # st.write(getRegAs)
                        if getRegAs == "Doctor":
                            app.doctorWala(username)
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
                        cursor.execute(f"SELECT regas FROM usr_info WHERE uniqueusr = '{username}'")
                        getRegAs = cursor.fetchall()[0][0]
                        # st.write(getRegAs)
                        if getRegAs == "Doctor":
                            try:
                                st.header(":green[Your Patients Database]")
                                st.write("###### **The Database is Sorted by Date, Patient ID, and Visit No. in Descending, Descending, and Descending Order Respectively.**")
                                st.markdown("#####")
                                engine = create_engine('mysql://u164935248_trial_pttrs:Trial_pttrs1@89.117.157.103/u164935248_trial_pttrs')
                                pdf_ = pd.read_sql(f"SELECT * FROM `patient_data` WHERE uniqueusr = '{username}' ORDER BY date_time DESC, patient_id DESC, visit_no DESC", con=engine)
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
                            except: st.info("At this moment you don't have any patient in the database.")
                        else:
                            st.header(":red[You don't have any access to patient database.]")
                            st.markdown("#####")
                            st.info("Patient database is only for doctors to access their patient details. Other than any doctors it's usage is strictly restricted.")
                    Authenticator.logout('Log Out', 'sidebar')                                       
                elif not authentication_status:
                    # with info:
                    st.error('Incorrect Password or username!')
                else:
                    # with info:
                    st.warning('Please feed in your credentials')
            else:
                # with info:
                st.warning('Username does not exist, Please register first!')
    elif formOption == "Reset Password":
        reset.reset()
    # elif formOption == "Find Username":
    #     reset.findUserName()
    else:
        account_control.register()
