import streamlit as st, re, streamlit_authenticator as sauth, mysql.connector as mysql
import pycountry
import phonenumbers

def get_country_phone_codes():
    country_phone_codes = []
    for country in pycountry.countries:
        try:
            country_code = phonenumbers.country_code_for_region(country.alpha_2)
            country_phone_codes.append((country.name, f"+{country_code}"))
        except phonenumbers.NumberFormatException:
            pass
    country_phone_codes.sort(key=lambda x: x[0])
    return country_phone_codes

def register():
    all_country_phone_codes = get_country_phone_codes()
    countryCodes = [f"{phone_code} ({country})" for country, phone_code in all_country_phone_codes]
    countriesAll = [f"{country}" for country, phone_code in all_country_phone_codes]           
    st.write("#")
    st.write("#####")
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
    def has_alphabet_numeric_special(input_string): return bool(re.match("^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).+$", input_string))
    with st.form(key="register"):
        st.subheader(':green[Register]')
        nameCols = st.columns([1,2,2,2,1])
        with nameCols[0]: salutation = st.selectbox("Salutation", ("Your Salutation", "Dr.", "Mr.", "Ms.", "Miss"))
        with nameCols[1]: first_name = st.text_input("First Name:red[*]") 
        with nameCols[2]: middle_name = st.text_input("Middle Name")
        with nameCols[3]: last_name = st.text_input("Last Name:red[*]")
        with nameCols[4]: gender = st.selectbox("Gender:red[*]", ("Select a Gender", "Male", "Female", "Others"))
        addressCols = st.columns([2,1,1,1,1])
        with addressCols[0]: address = st.text_input("Address:red[*]")
        with addressCols[1]: pin = st.text_input("PIN:red[*]")
        with addressCols[2]: state = st.text_input("State:red[*]")
        with addressCols[3]: country = st.selectbox("Country:red[*]", ["Select Your Country"]+countriesAll)
        with addressCols[4]: continent = st.selectbox("Continent:red[*]", ["Select Your Continent"]+['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Australia', 'South America'])
        colUniqueInfo = st.columns(2)
        with colUniqueInfo[0]: email_id = st.text_input("Email ID:red[*]")
        with colUniqueInfo[1]: unique_user_id = st.text_input("Unique User Name:red[*]")
        phoneCols = st.columns([1,2])
        with phoneCols[0]: countryCode = st.selectbox("Country code:red[*]", ["Select a Country Code"]+countryCodes)
        with phoneCols[1]: phoneNumber = st.text_input("Mobile No.:red[*]")
        colInfoPass = st.columns(2)
        with colInfoPass[0] : password = st.text_input("Password:red[*]", type="password", help="Password must be atleast 8 characters long and must contain alphabet(s), number(s), special character(s)")
        with colInfoPass[1]: confirm_password = st.text_input("Confirm Password:red[*]", type="password")
        affiliation = st.text_input("Affiliation:red[*]")
        affiliation_type = st.selectbox("Affiliation Type:red[*]", ("Select an Affiliation Type", "Hospital", "Personal Chember", "Research Institute", "University", "College"))
        registered_as = st.selectbox("Registered As:red[*]", ("Select an Account Registration Type", "Doctor", "Scientist", "Researcher", "PhD Scholar", "Student"))
        # st.write(first_name+middle_name+last_name)
        shortName, lisence, speciality = "", "", ""
        if registered_as == "Doctor":
            if len(first_name+middle_name+last_name) > 25:
                shortName = st.text_input("Write a short name within 25 characters:red[*] (since the length of your full name is greater that 25 characters, you need to again write your name in the following box within 25 characters. This will be display as your name in the generated PDF report.)")
            lisence = st.text_input("Liscence No.:red[*] (Since you are register yourself as doctor, you have to put your liscence no.)")            
            speciality = st.text_input("Speciality:red[*] (Since you are going to register yourself as doctor, you have to put your specilisation)")
        if st.form_submit_button("Create Account"):
            if salutation == "Your Salutation":
                st.warning("Salutation is not selcted. Please select your salutation properly")
            elif len(first_name) == 0:
                st.warning("Please provide your first name!")
            elif len(last_name) == 0:
                st.warning("Please provide your last name!")
            elif gender == "Select a Gender":
                st.warning("Gender is not selcted. Please select a gender!")
            elif len(address) == 0:
                st.warning("No address is provided. It is a reqired field!")
            elif len(pin) == 0:
                st.warning("No PIN Code is provided. It is a reqired field!")
            elif pin.isnumeric() == False:
                st.warning("PIN Code Must Be in Digits Only!")
            elif len(state) == 0:
                st.warning("No state is provided. It is a reqired field!")
            elif country == "Select Your Country":
                st.warning("Please Select Your Country!")
            elif country == "Select Your Continent":
                st.warning("Please Select Your Continent!")
            elif len(email_id) == 0:
                st.warning("Please provide your email ID!")
            elif '@' not in email_id:
                st.warning("Invalid email ID. Please provide email ID correctly!")
            elif countryCode == "Select a Country Code":
                st.warning("Please Select A Country Code")
            elif len(phoneNumber) < 10:
                st.warning("Mobile No. Must Be atleast 10 Digit Long!")
            elif phoneNumber.isnumeric() == False:
                st.warning("Mobile No. Must Be in Digits Only!")
            elif len(unique_user_id) == 0:
                st.warning("Please provide an Unique User Name!")
            elif len(password) == 0:
                st.warning("Please provide a password!")
            elif has_alphabet_numeric_special(password) == False:
                st.warning("Password must contain alphabet(s), number(s), special character(s). Please recheck your password!")
            elif len(password) < 8:
                st.warning("Password must be atleast 8 characters long. Please recheck your password!")
            elif password != confirm_password:
                st.warning("Password & Confirm Password is Not Matched!")
            elif len(affiliation) == 0:
                st.warning("Please provide your affiliation!")
            elif affiliation_type == "Select an Affiliation Type":
                st.warning("Please select your affiliation type!")
            elif registered_as == "Select an Account Registration Type":
                st.warning("Please select an account registration type!")
            elif registered_as == "Doctor":
                if len(shortName) == 0 and len(first_name+middle_name+last_name) > 25: st.warning("Please write your short name. This is a required field!")
                elif len(shortName) > 25: st.warning("Your short name length is still long than 25 characters!")
                elif len(lisence) == 0: st.warning("Liscence No. is not provided. It is required field.")
                elif len(speciality) == 0: st.warning("Specialisation(s) is/are not provided. It is required field.")
                else:
                    cursor.execute(f"SELECT uniqueusr FROM `usr_info` WHERE uniqueusr = '{unique_user_id}'")
                    uniqueUsers, uniqueMail = [], []
                    try:
                        uniqueUsers = cursor.fetchall()
                    except: pass
                    cursor.execute(f"SELECT mail FROM `usr_info` WHERE mail = '{email_id}'")
                    try:
                        uniqueMail = cursor.fetchall()
                    except: pass
                    if len(uniqueMail) > 0:
                        st.warning("An account is already found with the provided email ID. We can't proceed with this one!")
                    elif len(uniqueUsers) > 0:
                        st.warning("The 'Unique User Name' is already taken. Please try with another Unique User Name!")
                    else:
                        cursor.execute(f'''INSERT INTO usr_info (salutation, first_name, middle_name, last_name, gender, country, mail, uniqueusr, country_code, mobile, password, hashed_password, affiliation, afftype, regas, address, pin, state, continent, short_name, liscence_no, speciality) VALUES ("{salutation}", "{first_name}", "{middle_name}", "{last_name}", "{gender}", "{country}", "{email_id}", "{unique_user_id}", "{countryCode}", "{phoneNumber}", "{password}", "{sauth.Hasher([password]).generate()[0]}", "{affiliation}", "{affiliation_type}", "{registered_as}", "{address}", "{pin}", "{state}", "{continent}", "{shortName}", "{lisence}", "{speciality}")''')
                        st.balloons()
                        st.success("Account created successfully! Now you can login to PTTRS by your 'email ID/unique user name' and password")
                        st.warning("###### Please note down your 'Unique User Name' for future purposes. Once a 'Unique User Name' is generated in our record, it can't be modified!")
            else:
                cursor.execute(f"SELECT uniqueusr FROM `usr_info` WHERE uniqueusr = '{unique_user_id}'")
                uniqueUsers, uniqueMail = [], []
                try:
                    uniqueUsers = cursor.fetchall()
                except: pass
                cursor.execute(f"SELECT mail FROM `usr_info` WHERE mail = '{email_id}'")
                try:
                    uniqueMail = cursor.fetchall()
                except: pass
                if len(uniqueMail) > 0:
                    st.warning("An account is already found with the provided email ID. We can't proceed with this one!")
                elif len(uniqueUsers) > 0:
                    st.warning("The 'Unique User Name' is already taken. Please try with another Unique User Name!")
                else:
                    cursor.execute(f'''INSERT INTO usr_info (salutation, first_name, middle_name, last_name, gender, country, mail, uniqueusr, country_code, mobile, password, hashed_password, affiliation, afftype, regas, address, pin, state, continent, short_name, liscence_no, speciality) VALUES ("{salutation}", "{first_name}", "{middle_name}", "{last_name}", "{gender}", "{country}", "{email_id}", "{unique_user_id}", "{countryCode}", "{phoneNumber}", "{password}", "{sauth.Hasher([password]).generate()[0]}", "{affiliation}", "{affiliation_type}", "{registered_as}", "{address}", "{pin}", "{state}", "{continent}", "{shortName}", "{lisence}", "{speciality}")''')
                    st.balloons()
                    st.success("Account created successfully! Now you can login to PTTRS by your 'email ID/unique user name' and password")
                    st.warning("###### Please note down your 'Unique User Name' for future purposes. Once a 'Unique User Name' is generated in our record, it can't be modified!")
        connect2.close()
