import streamlit as st, mysql.connector as mysql, re, streamlit_authenticator as sauth

def contacts(username):
    col1, col2 = st.columns([1, 2])
    with col1: st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script><h2>Contact us</h2><p><b style="font-weight: 500;">Dr. Sintu Kumar Samanta</b> (Principle Investigator)<br>Assistant Professor<br>Department of Applied Sciences<br>Indian Institute of Information Technology Allahabad <br>Devghat, Jhalwa, Prayagraj, Uttar Pradesh 211015, India<br>Email: <a href="mailto:samantasintu@iiita.ac.in" style="text-decoration: none;">samantasintu@iiita.ac.in</a></p><p><b style="font-weight: 500;">Ananya Anurag Anand</b> (Principle Developer)                     <br>Email: <a href="rss2022501@iiita.ac.in" style="text-decoration: none;">rss2022501@iiita.ac.in</a></p><br><h5>For any technical issues</h5><p><b style="font-weight: 500;">Rajat Kumar Mondal</b> (Principle Developer)                     <br>Email: <a href="mailto:mbi2022013@iiita.ac.in" style="text-decoration: none;">mbi2022013@iiita.ac.in</a></p></div>', unsafe_allow_html=True)
    
    with col2:
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
        st.markdown("#")
        with st.form(key="contact"):
            st.subheader(':green[Contact form]')
            st.write("You can contact by filling out this form")
            subject = st.text_input("Subject:red[*]")
            messege = st.text_area("Your Query:red[*]", height=20)
            # salutation = st.selectbox("Salutation", ("Your Salutation", "Dr.", "Mr.", "Ms.", "Miss"))
            # colName = st.columns(3)
            # with colName[0]: first_name = st.text_input("First Name:red[*]") 
            # with colName[1]: middle_name = st.text_input("Middle Name")
            # with colName[2]: last_name = st.text_input("Last Name:red[*]")
            # gender = st.selectbox("Gender:red[*]", ("Select a Gender", "Male", "Female", "Others"))
            # colUniqueInfo = st.columns(2)
            # with colUniqueInfo[0]: email_id = st.text_input("Email Id:red[*]")
            # with colUniqueInfo[1]: unique_user_id = st.text_input("Unique User ID:red[*]")
            # colInfoPass = st.columns(2)
            # with colInfoPass[0] : password = st.text_input("Password:red[*]", type="password", help="Password must be atleast 8 characters long and must contain alphabet(s), number(s), special character(s)")
            # with colInfoPass[1]: confirm_password = st.text_input("Confirm Password:red[*]", type="password")
            # affiliation = st.text_input("Affiliation:red[*]")
            # affiliation_type = st.selectbox("Affiliation Type:red[*]", ("Select an Affiliation Type", "Hospital", "Personal Chember", "Research Institute", "University", "College"))
            # registered_as = st.selectbox("Registered As:red[*]", ("Select an Account Registration Type", "Doctor", "Scientist", "Researcher", "PhD Scholar", "Student"))
            if st.form_submit_button("Send Query"):
                # pass
                if len(subject) == 0: st.warning("Please Write a Subject!")
                elif len(messege) == 0: st.warning("Please Type Your Query!")
                else:
                    cursor.execute(f"SELECT * FROM `usr_info` WHERE uniqueusr='{username}'")
                    # st.write(f"SELECT * FROM `usr_info` WHERE uniqueusr={username}")
                    data = cursor.fetchall()
                    # st.write(data)
                    name = f"{data[0][1]} {data[0][2]} {data[0][3]} {data[0][4]}"
                    gender = data[0][5]
                    country = f"{data[0][16]}, {data[0][17]}, {data[0][18]}, {data[0][6]}, {data[0][19]}"
                    email = data[0][7]
                    uniqueUser = data[0][8]
                    mbCode = data[0][9].split("(")
                    mobile = f"{mbCode[0]}{data[0][10]}"
                    affiliation = data[0][13]
                    afftype = data[0][14]
                    regAs = data[0][15]
                    short_name = data[0][20]
                    liscence = data[0][21]
                    speciality = data[0][22]
                    # st.write(name)
                    # st.write(f"INSER INTO usr_query (name, gender, country, mail, uniqueusr, mobile, affiliation, afftype, regas, subject, messege) VALUES ('{name}', '{gender}', '{country}', '{email}', '{uniqueUser}', '{mobile}', '{affiliation}', '{afftype}', '{regAs}', '{subject}', '{messege}')")

                    cursor.execute(f"INSERT INTO usr_query (name, gender, full_address, mail, uniqueusr, mobile, affiliation, afftype, regas, short_name, liscence, speciality, subject, messege) VALUES ('{name}', '{gender}', '{country}', '{email}', '{uniqueUser}', '{mobile}', '{affiliation}', '{afftype}', '{regAs}', '{short_name}', '{liscence}', '{speciality}', '{subject}', '{messege}')")
                    st.success("Your query submitted successfully. Team PTTRS will contact you ASAP!")
            #     if salutation == "Your Salutation":
            #         st.warning("Salutation is not selcted. Please select your salutation properly")
            #     elif len(first_name) == 0:
            #         st.warning("Please provide your first name!")
            #     elif len(last_name) == 0:
            #         st.warning("Please provide your last name!")
            #     elif gender == "Select a Gender":
            #         st.warning("Gender is not selcted. Please select a gender!")
            #     elif len(email_id) == 0:
            #         st.warning("Please provide your email ID!")
            #     elif '@' not in email_id:
            #         st.warning("Invalid email ID. Please provide email ID correctly!")
            #     elif len(unique_user_id) == 0:
            #         st.warning("Please provide an unique user ID!")
            #     elif len(password) == 0:
            #         st.warning("Please provide a password!")
            #     elif has_alphabet_numeric_special(password) == False:
            #         st.warning("Password must contain alphabet(s), number(s), special character(s). Please recheck your password!")
            #     elif len(password) < 8:
            #         st.warning("Password must be atleast 8 characters long. Please recheck your password!")
            #     elif len(affiliation) == 0:
            #         st.warning("Please provide your affiliation!")
            #     elif len(affiliation_type) == "Select an Affiliation Type":
            #         st.warning("Please select your affiliation type!")
            #     elif registered_as == "Select an Account Registration Type":
            #         st.warning("Please select an account registration type!")
            #     elif password != confirm_password:
            #         st.warning("Password & Confirm Password is Not Matched!")
            #     else:
            #         cursor.execute(f"SELECT uniqueusr FROM `usr_info` WHERE uniqueusr = '{unique_user_id}'")
            #         if len(cursor.fetchall()) == 0:
            #             cursor.execute(f'''INSERT INTO usr_info (salutation, first_name, middle_name, last_name, gender, mail, uniqueusr, password, hashed_password, affiliation, afftype, regas) VALUES ("{salutation}", "{first_name}", "{middle_name}", "{last_name}", "{gender}", "{email_id}", "{unique_user_id}", "{password}", "{sauth.Hasher([password]).generate()[0]}", "{affiliation}", "{affiliation_type}", "{registered_as}")''')
            #             st.balloons()
            #             st.success("Account created successfully! Now you can login to PTTRS by your 'email ID/unique user name' and password")
            #             st.warning("###### Please note down your 'Unique User ID' for future purposes. Once a 'Unique User ID' is generated in our record it can't be modified!")
            #         else:
            #             st.warning("The 'Unique User ID' is already taken. Please try with another unique user ID!")
            # connect2.close()
    st.markdown('<div class="align-middle" style="width: 100%; margin-top: 2%;"><iframe style="border: 1px solid gray; border-radius:5px; padding: 0.6%" width="100%" height="460px auto" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3603.226373171629!2d81.76872441473931!3d25.430694283788142!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x399acda4892cc187%3A0xb07e2e87ab51e82a!2sIndian%20Institute%20of%20Information%20Technology%2C%20Allahabad!5e0!3m2!1sen!2sin!4v1672264848943!5m2!1sen!2sin"></iframe>     </div>', unsafe_allow_html=True)