import streamlit as st, mysql.connector as mysql
def account_details(username):
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
    cursor.execute(f"SELECT * FROM `usr_info` WHERE uniqueusr='{username}'")
    # st.write(f"SELECT * FROM `usr_info` WHERE uniqueusr={username}")
    data = cursor.fetchall()
    # st.write(data)
    if data[0][15] == "Doctor":
        with st.form(key="Acc_det"):
            mbCode = data[0][9].split("(")
            st.markdown("#### :green[Account Details]")
            st.markdown("#####")
            st.markdown(f"**Unique User Name:** {data[0][8]}")
            st.markdown(f"**Name:** {data[0][1]} {data[0][2]} {data[0][3]} {data[0][4]}")
            st.markdown(f"**Gender:** {data[0][5]}")
            st.markdown(f"**Full Address:** {data[0][16]}, {data[0][17]}, {data[0][18]}, {data[0][6]}, {data[0][19]}")
            st.markdown(f"**Email ID:** {data[0][7]}")
            st.markdown(f"**Mobile No.:** {mbCode[0]}{data[0][10]}")
            st.markdown(f"**Affiliation:** {data[0][13]}")
            st.markdown(f"**Affiliation Type:** {data[0][14]}")
            st.markdown(f"**Registered As:** {data[0][15]}")
            st.markdown(f"**Short Name:** {data[0][20]}")
            st.markdown(f"**Liscence No.:** {data[0][21]}")
            st.markdown(f"**Speciality:** {data[0][22]}")
            st.markdown("#####")
            st.form_submit_button("Got it")
    else:
        with st.form(key="Acc_det "):
            mbCode = data[0][9].split("(")
            st.markdown("#### :green[Account Details]")
            st.markdown("#####")
            st.markdown(f"**Unique User Name:** {data[0][8]}")
            st.markdown(f"**Name:** {data[0][1]} {data[0][2]} {data[0][3]} {data[0][4]}")
            st.markdown(f"**Gender:** {data[0][5]}")
            st.markdown(f"**Full Address:** {data[0][16]}, {data[0][17]}, {data[0][18]}, {data[0][6]}, {data[0][19]}")
            st.markdown(f"**Email ID:** {data[0][7]}")
            st.markdown(f"**Mobile No.:** {mbCode[0]}{data[0][10]}")
            st.markdown(f"**Affiliation:** {data[0][13]}")
            st.markdown(f"**Affiliation Type:** {data[0][14]}")
            st.markdown(f"**Registered As:** {data[0][15]}")
            st.markdown("#####")
            st.form_submit_button("Got it")
