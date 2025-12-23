import streamlit as st, re, streamlit_authenticator as sauth, mysql.connector as mysql
def reset():
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
    with st.form(key="reset"):
        st.subheader(':green[Reset Password]')
        email_id = st.text_input("Username:red[*]")
        password = st.text_input("New Password:red[*]", type="password", help="Password must be atleast 8 characters long and must contain alphabet(s), number(s), special character(s)")
        confirm_password = st.text_input("Confirm Password:red[*]", type="password")
        if st.form_submit_button("Reset Password"):
            if len(email_id) == 0:
                st.warning("Please provide your email ID!")
            elif len(password) == 0:
                st.warning("Please provide a password!")
            elif has_alphabet_numeric_special(password) == False:
                st.warning("Password must contain alphabet(s), number(s), special character(s). Please recheck your password!")
            elif len(password) < 8:
                st.warning("Password must be atleast 8 characters long. Please recheck your password!")
            elif password != confirm_password:
                st.warning("Password & Confirm Password Does Not Matched!")
            else:
                cursor.execute(f"SELECT uniqueusr FROM `usr_info` WHERE uniqueusr = '{email_id}'")
                uniqueUserVerify = cursor.fetchall()
                if len(uniqueUserVerify) == 0: st.error("Invalid Unique User ID!")
                else: 
                    cursor.execute(f"UPDATE `usr_info` SET password='{password}', hashed_password='{sauth.Hasher([password]).generate()[0]}' WHERE uniqueusr = '{email_id}'")
                    st.balloons()
                    st.success("Password reset successfully!")
        connect2.close()

# def findUserName():
#     st.write("#")
#     st.write("#####")
#     config = {
#     'user': 'u164935248_trial_pttrs',
#     'password': 'Trial_pttrs1',
#     'host': '89.117.157.103',
#     'use_pure': True,
#     'raise_on_warnings': True,
# }
#     connect2= mysql.connect(**config)
#     cursor = connect2.cursor()
#     mail = st.text_input("Your mail")
#     if st.button("Get Unique User ID"):
#         cursor.execute(f"USE u164935248_trial_pttrs")
#         cursor.execute(f"SELECT uniqueusr FROM usr_info WHERE `mail` = '{mail}'")
#         try: 
#             getuniqueusr = cursor.fetchall()
#             if len(getuniqueusr) == 0:
#                 st.warning("No Unique User ID found with the given mail ID. Please register first, if you are a new user!")
#             else:
#                 st.write(getuniqueusr)
#         except: 
#             st.warning("No Unique User ID found with the given mail ID. Please register first, if you are a new user!")
