import streamlit as st, filterDF, mysql.connector as mc, networkx as nx, community.community_louvain as cl, pandas as pd, numpy as np, math as mt, joblib, os
from pyvis.network import Network
from scipy.sparse import csr_matrix, vstack
from rdkit import Chem
from rdkit.Chem import Crippen
from rdkit.Chem import Descriptors
from sqlalchemy import create_engine
from itertools import combinations
import pycountry, phonenumbers
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
all_country_phone_codes = get_country_phone_codes()
def generate_report(id, visit, name, age, gender, bg, address_, contact, drName, speciality, nextVisit, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, uniqusr):
    pdf = canvas.Canvas(f"tb_report_{uniqusr}_pid_{id}_vno_{visit}.pdf", pagesize=letter)
    pdf.setTitle(f"tb_report_{uniqusr}_pid_{id}_vno_{visit}")
    pdf.setFont("Times-Roman", 12)
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(30, 750, "TB Treatment Report")
    date_ = datetime.now().strftime('%d/%m/%Y %H:%M:%S').split(" ")[0]
    pdf.drawString(495, 750, f"Date: {date_}")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(38, 730, "PATIENT INFORMATION")
    pdf.drawString(43, 715, f"ID: {id}")
    pdf.drawString(43, 700, f"Visit: {visit}")
    pdf.drawString(43, 685, f"Name: {name}")
    pdf.drawString(43, 670, f"Age: {age}")
    pdf.drawString(43, 655, f"Gender: {gender}")
    pdf.drawString(43, 640, f"Blood Group: {bg}")
    pdf.drawString(43, 625, f"Full Address: {address_}")
    pdf.drawString(43, 610, f"Contact No.: {contact}")
    pdf.line(12, 602, 300, 602)
    pdf.drawString(320, 730, "DOCTOR INFORMATION")
    pdf.drawString(325, 715, f"Name: {drName}")
    pdf.drawString(325, 700, f"Specialty: {speciality}")
    pdf.drawString(320, 670, f"NEXT VISIT")
    pdf.drawString(325, 655, f"{nextVisit}")
    pdf.line(300, 602, 600, 602)
    pdf.drawString(38, 585, "TB INFORMATION OF PATIENT")
    pdf.drawString(43, 570, f"Patient health condition regarding TB: {tb_health}")
    pdf.drawString(43, 555, f"Infection age: {infection_age}")
    pdf.drawString(43, 540, f"Treatment: {treatment}")
    pdf.line(12, 532, 600, 532)
    pdf.drawString(38, 517, "AMR (ANTIMICROBIAL RESISTANCE) REPORT AND STRAIN")
    pdf.drawString(43, 502, f"Test name(s): {testNames}")
    pdf.drawString(43, 487, f"AMR strain name: {amrStrain}")
    pdf.drawString(43, 472, f"Resistant drug(s): {resistantDrugs}")
    pdf.line(12, 464, 600, 464)
    pdf.drawString(38, 449, f"AMC DETAILS: {amcDetails}")
    pdf.line(12, 441, 600, 441)
    pdf.drawString(38, 426, "PRESCRIBED MEDICINE(S)")
    pdf.drawString(43, 411, f"For TB: {tbDrug}")
    pdf.drawString(43, 396, f"For AMC: {amcDrug}")
    pdf.line(12, 388, 600, 388)
    pdf.drawString(38, 373, "SPECIAL COMMENT(S) BY DOCTOR")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(20, 20, f"Report generated at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} by B&BL, IIIT A")
    pdf.drawString(20, 8, f"Powered by PTTRS@BBLSERVER")
    pdf.save()
def doctorWala(userID):
    countryCodes = [f"{phone_code} ({country})" for country, phone_code in all_country_phone_codes]
    # st.set_page_config(layout="wide", page_title="PTTRS (Trial Version)", page_icon="🧬")
    st.title("Personalized Tuberculosis Treatment Recommender System (PTTRS)")
    # st.markdown("##### A Precision-Medicine Based Application for Recommending Personalized Treatment to Tuberculosis Patients")
    # st.markdown("####")
    config = {
        'user': 'u164935248_trial_pttrs',
        'password': 'Trial_pttrs1',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
    connect2 = mc.connect(**config)
    cursor = connect2.cursor()
    # userID = 'rajat'
    engine = create_engine('mysql://u164935248_pttrs_drs:pttrS1_drs@89.117.157.103/u164935248_pttrs_drs')
    backend, check_patient_conformation, go_backend = [], [""], []
    st.write("----")
    st.write("##### ***Patient Details (:red[*] are compulsory)***")
    patientType = st.radio("Patient category", ["New Patient", "Re-visit"], horizontal=True, help="Please DO NOT use auto-suggestion while fill the form.")
    varifydata = 0
    newVisitID_ = ''
    id_ = ''
    if patientType == "New Patient":
        backend.append(userID)
        cursor.execute('USE u164935248_trial_pttrs')
        cursor.execute(f"SELECT patient_id from patient_data WHERE uniqueusr = '{userID}' ORDER BY patient_id DESC")
        foundPatientID = cursor.fetchall()
        # st.write(foundPatientID[0][0])
        newPatientID = 0
        if len(foundPatientID) > 0:
            newPatientID = int(foundPatientID[0][0])+1
        id_ = newPatientID
        newVisitID = 1
        newVisitID_ = newVisitID
        backend.append(newPatientID)
        backend.append(newVisitID)
        st.write("Note: Patient ID & visit number will assign automatically by the system!")
        st.write(f"ID Assigned: {newPatientID}; Visit No. Assigned: {newVisitID}")
        patient_data = st.columns([2,1,1,1,2])
        with patient_data[0]:
            patientName = st.text_input("Full name:red[*]", help="Name must be within 25 characters.")
            if len(patientName) <= 25 : 
                check_patient_conformation.append(patientName)
                varifydata+=1
            else: st.warning("Name must be within 25 characters!")
        with patient_data[1]:
            patientAge = st.selectbox("Age:red[*]", [""]+list(range(0,120)))
            check_patient_conformation.append(patientAge)
        with patient_data[2]:
            patientGender = st.selectbox("Geneder:red[*]", ["",'Female','Male','Others'])
            check_patient_conformation.append(patientGender)
        with patient_data[3]:
            patientBloodGroup = st.selectbox("Blood Group:red[*]", ["", 'A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-', 'Bombay'])
            check_patient_conformation.append(patientBloodGroup)
        with patient_data[4]:
            patientTBHealth = st.selectbox("Patient health condition regardig TB:red[*]", ["", "Normal", "Moderate", "Better than moderate", "Worst", "Unable to survive"])
            check_patient_conformation.append(patientTBHealth)
        patient_data3 = st.columns([1,1,2,1,2])
        with patient_data3[0]:
            patientCurrentInfectionState = st.selectbox("Infection age:red[*]", ["", "Newly infected", "Few days old", "Few weeks old", "1 month old", "Few months old", "1 year old", "Few years old"])
            check_patient_conformation.append(patientCurrentInfectionState)
        with patient_data3[1]:
            patientTreatment = st.selectbox("Treatment:red[*]", ["", "Initiate", "Going on"])
            check_patient_conformation.append(patientTreatment)
        with patient_data3[2]:
            patientCountryCode = st.selectbox("Country Code:red[*]", [""]+countryCodes)
            check_patient_conformation.append(patientCountryCode)
        with patient_data3[3]:
            patientPhone = st.text_input("Contact no.:red[*]", help="Phone no. must be digits. At only first position '+' sign is allowed for country code.")
            if len(patientPhone) > 0:
                if len(patientPhone) < 10:
                    st.warning("Contact no. must be atleast 10 digits long.")
                elif patientPhone.isnumeric() == False:
                    st.warning("Contact no. must be in digits only!")
                else:
                    check_patient_conformation.append(patientPhone)
                    varifydata+=1
        with patient_data3[4]:
            patientPhone = st.text_input("Address:red[*]", help="Address must be within 50 characters.")
            if len(patientPhone) <= 50:
                check_patient_conformation.append(patientPhone)
                varifydata+=1
            else: st.warning("Address must be within 50 characters!")
        patient_data2 = st.columns(4)
        with patient_data2[0]:
            patientContinent = st.selectbox("Continent:red[*]", [""]+["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])
            check_patient_conformation.append(patientContinent)
        with patient_data2[1]:
            patientCountry = st.selectbox("Country:red[*]", [""]+[country.name for country in pycountry.countries])
            check_patient_conformation.append(patientCountry)
        with patient_data2[2]:
            patientState = st.text_input("State:red[*]")
            check_patient_conformation.append(patientState)
        with patient_data2[3]:
            patientPINCode = st.text_input("PIN Code:red[*]", help="PIN code must be in digits only.")
            if len(patientPINCode) > 0:
                try:
                    varifyPIN = int(patientPINCode)
                    check_patient_conformation.append(patientPINCode)
                    varifydata+=1
                except:
                    st.warning("PIN Code must be in digits only!")
        go_backend = backend+check_patient_conformation
        # st.write(go_backend)
        patientMedicalHistory = st.text_area("Midical history/condition (if any)")
        go_backend.append(patientMedicalHistory)
        st.write("----")
    getvisitno = ''
    if patientType == "Re-visit":
        st.write("Note: Visit number will assign automatically by the system!")
        patientID = st.text_input("Unique patient ID")
        id_ = patientID
        if st.checkbox("Get patient details"):
            if len(str(patientID)) > 0:
                cursor.execute('USE u164935248_trial_pttrs')
                cursor.execute(f"SELECT `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `infection_age`, `treatment_status`, `contact_no`, `address`, `continent`, `country`, `state`, `pin`, `medical_history`, `date_time`, `country_code` FROM patient_data WHERE uniqueusr = '{userID}' AND patient_id = '{patientID}' ORDER BY visit_no DESC LIMIT 1")
                userDet = cursor.fetchall()
                if len(userDet) > 0:
                    st.write(f"Patient ID: {userDet[0][0]}")
                    backend.append(str(userDet[0][0]))
                    cursor.execute(f"SELECT MAX(visit_no) FROM patient_data WHERE uniqueusr = '{userID}' AND patient_id = {patientID}")
                    visit_no = cursor.fetchall()[0][0]
                    backend.append(str(visit_no+1))
                    st.write(f"Total visited: {visit_no} Times")
                    # spDate = str(userDet[0][-1]).split(" ")[0].split("-")
                    # st.write(f"Last visited: {spDate[2]}/{spDate[1]}/{spDate[0]}")
                    st.write(f"Last visited: {userDet[0][-2]}")
                    st.write(f"New Visit No. Assigned: {str(visit_no+1)}")
                    newVisitID_ = visit_no+1
                    getvisitno = visit_no+1
                    # st.text(f"Name: {userDet[0][2]}    Age: {userDet[0][3]}")
                    patient_data = st.columns([2,1,1,1,2])
                    with patient_data[0]:
                        patientName = st.text_input("Full name ", value=userDet[0][2], disabled=True)
                        if len(patientName) <= 25 : 
                            check_patient_conformation.append(patientName)
                            varifydata+=1
                        else: st.warning("Name must be within 25 characters!")
                    with patient_data[1]:
                        patientAge = st.text_input("Age ", value=userDet[0][3], disabled=True)
                        check_patient_conformation.append(patientAge)
                    with patient_data[2]:
                        patientGender = st.text_input("Geneder ", value=userDet[0][4], disabled=True)
                        check_patient_conformation.append(patientGender)
                    with patient_data[3]:
                        patientBloodGroup = st.text_input("Blood Group ", value=userDet[0][5], disabled=True)
                        check_patient_conformation.append(patientBloodGroup)
                    with patient_data[4]:
                        patientTBHealth = st.selectbox("Patient health condition regardig TB:red[*]", ["", "Same as previous visit", "Improving", "Normal", "Moderate", "Better than moderate", "Worst", "Unable to survive"])
                        check_patient_conformation.append(patientTBHealth)
                    patient_data3 = st.columns([1,1,2,1,2])
                    with patient_data3[0]:
                        patientCurrentInfectionState = st.text_input("Infection age ", value=userDet[0][6], disabled=True)
                        check_patient_conformation.append(patientCurrentInfectionState)
                    with patient_data3[1]:
                        patientTreatment = st.selectbox("Treatment:red[*] ", ["", "Going on", "Most probably will stop soon", "Stop"])
                        check_patient_conformation.append(patientTreatment)
                    with patient_data3[2]:
                        patientCountryCode = st.text_input("Country Code", value=userDet[0][-1], disabled=True)
                        check_patient_conformation.append(patientCountryCode)
                    with patient_data3[3]:
                        patientPhone = st.text_input("Contact no.", value=userDet[0][8], disabled=True)
                        if len(patientPhone) > 0:
                            if len(patientPhone) < 10:
                                st.warning("Contact no. must be atleast 10 digits long.")
                            elif patientPhone.isnumeric() == False:
                                st.warning("Contact no. must be in digits only!")
                            else:
                                check_patient_conformation.append(patientPhone)
                                varifydata+=1
                    with patient_data3[4]:
                        patientPhone = st.text_input("Address ", value=userDet[0][9], disabled=True)
                        if len(patientPhone) <= 50:
                            check_patient_conformation.append(patientPhone)
                            varifydata+=1
                        else: st.warning("Address must be within 50 characters!")
                    patient_data2 = st.columns(4)
                    with patient_data2[0]:
                        patientContinent = st.text_input("Continent ", value=userDet[0][10], disabled=True)
                        check_patient_conformation.append(patientContinent)
                    with patient_data2[1]:
                        patientCountry = st.text_input("Country ", value=userDet[0][11], disabled=True)
                        check_patient_conformation.append(patientCountry)
                    with patient_data2[2]:
                        patientState = st.text_input("State ", value=userDet[0][12], disabled=True)
                        check_patient_conformation.append(patientState)
                    with patient_data2[3]:
                        patientPINCode = st.text_input("PIN Code ", value=userDet[0][13], disabled=True)
                        if len(patientPINCode) > 0:
                            try:
                                varifyPIN = int(patientPINCode)
                                check_patient_conformation.append(patientPINCode)
                                varifydata+=1
                            except:
                                st.warning("PIN Code must be in digits only!")
                    go_backend = backend+check_patient_conformation
                    # st.write(go_backend)
                    patientMedicalHistory = st.text_input("Midical history/condition (if any) ", value=userDet[0][14], disabled=True)
                    go_backend.append(patientMedicalHistory)
                    # st.write(go_backend)
                    go_backend.pop(2)
                    cursor.execute(f"SELECT `patient_id`, `travel_history`, `strain_info`, `dst_done`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `date_time`, `visit_no`, `patient_tb_health`, `next_visit`, `treatment_status` FROM patient_data WHERE uniqueusr = '{userID}' AND patient_id = '{patientID}' ORDER BY visit_no DESC")
                    checkup_history = cursor.fetchall()
                    visitHistory = []
                    try:
                        for histry in checkup_history:
                            locationList = []
                            for travel in histry[1].split("; "):
                                cursor.execute(travel)                        
                                for info in cursor.fetchall():
                                    # st.write(info)
                                    locationList.append(f"{info[0]}-{info[1]}")
                            visitHistory.append({
                                    "pid": histry[0],
                                    "Location Info": "; ".join(locationList)
                                })
                    except:
                        visitHistory.append({
                                    "pid": histry[0],
                                    "Location Info": ""
                                })
                    visitHistory_ = []
                    try:
                        for histry in checkup_history:
                            locationList = []
                            for travel in histry[2].split("; "):
                                cursor.execute(travel)                        
                                for info in cursor.fetchall():
                                    # st.write(info)
                                    locationList.append(f"{info[0]}-{info[1]}")
                            visitHistory_.append({
                                    "pid": histry[0],
                                    "Strain Info": "; ".join(locationList)
                                }) 
                    except:
                        visitHistory_.append({
                                    "pid": histry[0],
                                    "Strain Info": ""
                                })  
                    visitHistory___ = []
                    for histry in checkup_history:
                        # previousDateSplit = str(histry[10]).split(" ")[0].split("-")
                        visitHistory___.append({
                            "pid": histry[0],
                            "DST": histry[3],
                            "DST Name": histry[4],
                            "AMR TB (by DST)": histry[5],
                            "Drug Rest. (by DST)": histry[6],
                            "AMC Info": histry[7],
                            "Given TB Drug": histry[8],
                            "Given AMC Drug": histry[9],
                            # "Date": f"{previousDateSplit[2]}/{previousDateSplit[1]}/{previousDateSplit[0]}",
                            "Date": histry[10],
                            "Visit No.": histry[11],
                            "Health Condition Regarding TB": histry[12],
                            "Next Visit Date": histry[13],
                            "Treatment Status": histry[14]
                        })
                    patientHistoryDF = pd.DataFrame(visitHistory___)
                    patientHistoryDF["Strain Info"] = pd.DataFrame(visitHistory_)["Strain Info"]
                    patientHistoryDF["Location Info"] = pd.DataFrame(visitHistory)["Location Info"]
                    re_order = ["Date", "Visit No.", "Health Condition Regarding TB", "Treatment Status", "Given TB Drug", "AMC Info", "Given AMC Drug", "Location Info", "Strain Info", "DST", "DST Name", "AMR TB (by DST)", "Drug Rest. (by DST)", "Next Visit Date"]
                    patientHistoryDF = patientHistoryDF[re_order]
                    st.markdown(":green[Treatment Details] (Sorted by Visit No. in descending order)")
                    st.dataframe(patientHistoryDF, height=200)
                else: st.warning("You don't have the patient with given patient ID!")
            else:
                st.warning("Unable to proceed without patient ID!")
    col1, col2 = st.columns(2)
    travelHistorySql = []
    with col1:
        st.markdown("----")
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute("SELECT * FROM data_geo_loc")
        option1Data = cursor.fetchall()
        inputDataList1 = []
        for i in option1Data:
            inputDataList1.append(i[0])
        st.write("##### ***Location information***")
        option1 = st.multiselect(
            'Enter geographical location or travel history [optional]', sorted(
                list(set(inputDataList1))), help="This facility helps a user to see the possible strain based on travel history of a patient. Multiple travel location can be choosen."
        )
        locs = []
        locsStrain = []
        if len(option1) == 0:
            cursor.execute(f"SELECT * FROM `data_geo_loc`")
            outData1 = cursor.fetchall()
            for i in outData1:
                locs.append(i[0])
                locsStrain.append(i[1][0].upper()+i[1][1:])        
            df1 = {
                "Geographical Location": locs,
                "TB Strain": locsStrain
            }
            st.caption("Display all TB strain based on geographical location [default] (data sorted by Geographical Location)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
            go_backend.append("")
        else:
            exactVal = 0
            if st.checkbox("Exact location"): exactVal = 1
            # if exa
            for op in option1:
                if exactVal == 0:
                    cursor.execute(f"SELECT * FROM `data_geo_loc` WHERE geoloc LIKE '%{op}%'")
                    outData1 = cursor.fetchall()
                    travelHistorySql.append(f"SELECT * FROM `data_geo_loc` WHERE geoloc LIKE '%{op}%'")
                    for i in outData1:
                        locs.append(i[0])
                        locsStrain.append(i[1][0].upper()+i[1][1:])
                if exactVal == 1:
                    cursor.execute(f"SELECT * FROM `data_geo_loc` WHERE geoloc LIKE '{op}'")
                    outData1 = cursor.fetchall()
                    travelHistorySql.append(f"SELECT * FROM `data_geo_loc` WHERE geoloc LIKE '{op}'")
                    for i in outData1:
                        locs.append(i[0])
                        locsStrain.append(i[1][0].upper()+i[1][1:])
            go_backend.append("; ".join(travelHistorySql))
            df1 = {
                "Geographical Location": locs,
                "TB Strain": locsStrain
            }    
            st.caption("Search result (data sorted by Geographical Location)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
        st.markdown("----")
    # st.write("; ".join(travelHistorySql))
    strainInfoSql = []
    with col2:
        st.markdown("----")
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute("SELECT * FROM data_geo_loc")
        option1Data = cursor.fetchall()
        inputDataList1 = []
        for i in option1Data:
            inputDataList1.append(i[1])
        st.write("##### ***Strain information***")
        option1 = st.multiselect(
            'Enter TB strain(s) [optional]', sorted(
                list(set(inputDataList1))), help="This facility helps a user to see the strain that attack to a patient from which geographical location(s). Multiple strain can be choosen."
        )
        locs = []
        locsStrain = []
        if len(option1) == 0:
            cursor.execute(f"SELECT * FROM `data_geo_loc`")
            outData1 = cursor.fetchall()
            for i in outData1:
                locs.append(i[0])
                locsStrain.append(i[1][0].upper()+i[1][1:])        
            df1 = {
                "TB Strain": locsStrain,
                "Geographical Location": locs            
            }
            st.caption("Display all geographical location based on TB strain [default] (data sorted by TB strain)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
            go_backend.append("")
        else:
            exactVal = 0
            if st.checkbox("Exact strain"): exactVal = 1
            for op in option1:
                if exactVal == 0:
                    cursor.execute(f"SELECT * FROM `data_geo_loc` WHERE strain LIKE '%{op}%'")
                    outData1 = cursor.fetchall()
                    strainInfoSql.append(f"SELECT * FROM `data_geo_loc` WHERE strain LIKE '%{op}%'")
                    for i in outData1:
                        locs.append(i[0])
                        locsStrain.append(i[1][0].upper()+i[1][1:])
                if exactVal == 1:
                    cursor.execute(f"SELECT * FROM `data_geo_loc` WHERE strain LIKE '{op}'")
                    outData1 = cursor.fetchall()
                    strainInfoSql.append(f"SELECT * FROM `data_geo_loc` WHERE strain LIKE '{op}'")
                    for i in outData1:
                        locs.append(i[0])
                        locsStrain.append(i[1][0].upper()+i[1][1:])
            go_backend.append("; ".join(strainInfoSql))
            df1 = {
                "Geographical Location": locs,
                "TB Strain": locsStrain
            }    
            st.caption("Search result (data sorted by Geographical Location)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
        st.markdown("----")
    # st.write("; ".join(strainInfoSql))
    st.markdown("####")
    opt4 = []
    amrdrugs = []
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("----")
        st.write("##### ***AMR (Antimicrobial Resistance) report and strain***")
        option3 = st.selectbox("Have you done drug susceptibility testing (DST) or any other test for AMR detection??", ["", "Yes", "No"])
        if option3 == "": 
            go_backend+=["","","",""]
            # st.write(go_backend)
        if option3 == "Yes":
            go_backend.append(option3)
            screening_test = st.text_input("Test name(s):red[*]", help="In case of multiple test, please write test names in a comma space separated manner (e.g., test x, test y).")
            go_backend.append(screening_test)
            check_patient_conformation.append(screening_test)
            amr_strain = st.text_input("AMR strain name:red[*]", help="In case of multiple strain, please write strain names in a comma space separated manner (e.g., strain x, strain y). If AMR strain name unknown, just write NA in that case.")
            go_backend.append(amr_strain)
            check_patient_conformation.append(amr_strain)
            # st.write(check_patient_conformation)
            cursor.execute("SELECT `Drug for TB` FROM `data_anti-tb_drugs_sideeffects`")
            amrdata = cursor.fetchall()
            for i in amrdata:
                amrdrugs.append(i[0][0].upper()+i[0][1:])
            option4 = st.multiselect("Resistant drug(s) [if known]", amrdrugs, help="Selected tb-resistant drgus will automatically subtracted from suggestive TB drug list.") 
            go_backend.append(", ".join(option4))
            opt4+=option4
        if option3 == "No":
            go_backend.append(option3)
            go_backend+=["", "", ""]
            # st.write(go_backend)
            cursor.execute("SELECT `Drug for TB` FROM `data_anti-tb_drugs_sideeffects`")
            amrdata = cursor.fetchall()
            for i in amrdata:
                amrdrugs.append(i[0][0].upper()+i[0][1:])
            st.warning("We can't proceed without a lab diagnosis for this section. Please move forward to the next section!")
        st.markdown("----")
    if option3 == "Yes" or option3 == "No":
        with col4:
            st.markdown("----")
            st.write("##### ***AMC (Associated Medical Condition) details***")
            cursor.execute("SELECT `disease` FROM `data_amc_drugs`")
            amcDiseaseData = cursor.fetchall()
            disease = []
            for i in amcDiseaseData:
                disease.append(i[0][0].upper()+i[0][1:].replace("iv/aids", "IV/AIDS"))
            option5 = st.multiselect("Select an associative disease with TB", sorted(disease), help="Well known cross reactive drug(s) based on selected AMC will automatically subtracted from suggestive TB drug list. For 'Diabetes', Rifampin, and Isoniazid; For 'HIV/AIDS', Rifampin, Bedaquiline, and Delamanid; For 'Rheumatoid arthritis', Isoniazid, and Pyrazinamide will subtracted.")
            # if len(option5) == 0: go_backend.append("")
            if len(option5) > 0: go_backend.append(", ".join(option5))
            # st.write(go_backend)
            disearDrugDict = {
                "Diabetes" : ["Rifampin", "Isoniazid"],
                "HIV/AIDS" : ["Rifampin", "Bedaquiline", "Delamanid"],
                "Thyroid": "",
                "Asthma": "",
                "Rheumatoid arthritis" : ["Isoniazid", "Pyrazinamide"]
            }
            notpresdrug = []
            for x in option5:
                notpresdrug+=disearDrugDict[x]
            notpresdrug+=opt4
            st.markdown("----")
    config = {
        'user': 'u164935248_pttrs_drs',
        'password': 'pttrS1_drs',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
    connect2 = mc.connect(**config)
    cursor = connect2.cursor()
    cursor.execute("USE u164935248_pttrs_drs")
    try: cursor.execute(f"TRUNCATE TABLE `filtered_tb_drugs_{userID}`")
    except: pass
    try: pd.DataFrame(sorted(list(set(amrdrugs).difference(set(notpresdrug))))).to_sql(f'filtered_tb_drugs_{userID}', con=engine, index=False, if_exists='replace')
    except: pass
    config = {
        'user': 'u164935248_trial_pttrs',
        'password': 'Trial_pttrs1',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
    connect2 = mc.connect(**config)
    cursor = connect2.cursor()
    cursor.execute("USE u164935248_trial_pttrs")
    totSD__ = []
    filtered_tb_drugs = []
    try: filtered_tb_drugs = list(pd.read_sql(f'SELECT * FROM `filtered_tb_drugs_{userID}`', con=engine)['0'])
    except: pass
    totalSelectedDrugs = []
    if len(filtered_tb_drugs) > 1:    
        df = pd.read_csv("se.csv")
        def checkbox_container(data):
            st.write("##### ***Suggested Drugs for TB***")
            cols = st.columns(10)
            if cols[-1].button('Select All'):
                for i in data:
                    st.session_state['dynamic_checkbox_' + i] = True
                st.experimental_rerun()
            if cols[-2].button('UnSelect All'):
                for i in data:
                    st.session_state['dynamic_checkbox_' + i] = False
                st.experimental_rerun()
            makeColumn = mt.ceil(len(filtered_tb_drugs)/10)
            cols2 = st.columns(makeColumn)
            dataCount = 1
            colCnt = 0
            for i in data:
                if dataCount % 10 ==0:colCnt+=1
                with cols2[colCnt]:
                    st.checkbox(i, key='dynamic_checkbox_' + i)
                dataCount+=1

        def get_selected_checkboxes():
            return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]
        st.markdown("####")
        st.markdown("----")
        checkbox_container(filtered_tb_drugs)
        # st.write('You selected:')
        selectedTBDrug = [x for x in get_selected_checkboxes() if x[0] != '_']
        if len(selectedTBDrug) > 0:
            st.markdown("####") 
            st.write(f"###### Selected TB drug(s) [{len(selectedTBDrug)}]: {', '.join(selectedTBDrug)}")
            go_backend.append(', '.join(selectedTBDrug))
        else: go_backend.append("")
        st.markdown("----")
        def amc_checkbox_container(data_, amcD):
            st.write(f"###### ***{amcD}***")
            for i_ in data_:
                st.checkbox(i_, key='dynamic_checkbox__' + i_)
        def amc_get_selected_checkboxes():
            return [i_.replace('dynamic_checkbox__','') for i_ in st.session_state.keys() if i_.startswith('dynamic_checkbox__') and st.session_state[i_]]
        totalSelectedDrugs = []
        if len(option5) > 0:
            st.markdown("####")
            st.markdown("----")
            st.write("##### ***Available Drugs for AMCs***")
            amcList = ["Diabetes", "HIV/AIDS", "Thyroid", "Asthma", "Rheumatoid arthritis"]
            # filteredAMC = []
            cols3 = st.columns(5)
            cols3Indx = 0
            col6 = st.columns(10)
            selAMCData = []
            for amcDisease in option5:
                # filteredAMC.append(amcDisease)
                if amcDisease in amcList:
                    with cols3[cols3Indx]:
                        # st.write(amcDisease)
                        amc_checkbox_container(sorted(list(set(df[df['disease'] == amcDisease]['drug']))), amcDisease)
                        selAMCData += list(set(df[df['disease'] == amcDisease]['drug']))
                cols3Indx+=1
            selectedAMCDrug = amc_get_selected_checkboxes()
            if len(selectedAMCDrug) > 0:
                st.write(f"###### Selected AMC drug(s) [{len([myx for myx in selectedAMCDrug if myx in selAMCData])}]: {', '.join([myx for myx in selectedAMCDrug if myx in selAMCData])}")
                go_backend.append(', '.join([myx for myx in selectedAMCDrug if myx in selAMCData]))
            if len(selectedAMCDrug) == 0: go_backend.append("")
            st.markdown("----")
            totalSelectedDrugs = selectedTBDrug+selectedAMCDrug
        if len(option5) == 0:
            totalSelectedDrugs = selectedTBDrug
            go_backend.append("")
        # st.write(len(totalSelectedDrugs))
        st.markdown("####")
        st.markdown("----")
        selDF = []
        st.write(f"##### ***Mono Drug Side Effect Visualizer***")
        if len(totalSelectedDrugs) == 0:st.warning("Select at least 1 drug (TB/AMC) to visualize mono drug side effect network")
        if len(totalSelectedDrugs) > 0:
            if st.checkbox("Enable Visualizer & Side Effect Informations"):
                mseDF = []
                for selectedDrug in totalSelectedDrugs:
                    mseDF.append(df[df['drug']==selectedDrug])
                if len(mseDF) > 0:
                    selectedDrugDF = pd.concat(mseDF, ignore_index=True)
                    # st.write(selectedDrugDF)
                    selDF = selectedDrugDF
                    selectedDrugDF = selectedDrugDF.drop(['disease'], axis=1)
                    selectedDrugDF['val'] = 1
                    selectedDrugDF = selectedDrugDF.groupby(["drug", "se"], sort=False, as_index=False).sum()
                    G = nx.from_pandas_edgelist(selectedDrugDF,
                                               source="drug",
                                                target="se",
                                                edge_attr="val",
                                                create_using=nx.Graph()
                                               )
                    net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                    node_degree = dict(G.degree)
                    nx.set_node_attributes(G, node_degree, 'size')
                    partition = cl.best_partition(G)
                    nx.set_node_attributes(G, partition, 'group')
                    net.from_nx(G)
                    net.save_graph("mdse.html")
                    with open("mdse.html",'r') as f: 
                        html_data = f.read()
                    agree = st.checkbox('Enable Network Filters & Selection Menu')
                    if agree:
                        net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                        node_degree = dict(G.degree)
                        nx.set_node_attributes(G, node_degree, 'size')
                        partition = cl.best_partition(G)
                        nx.set_node_attributes(G, partition, 'group')
                        net.from_nx(G)
                        net.save_graph("mdse.html")
                        with open("mdse.html",'r') as f: 
                            html_data = f.read()
                    st.components.v1.html(html_data,height=800)
            st.markdown("----")
            st.markdown("####")
            mdInfoCols = st.columns([2,1])
            ddata = []
            mymseDF = []
            for selectedDrug in totalSelectedDrugs:
                mymseDF.append(df[df['drug']==selectedDrug])
                ddata.append({
                    "Disease": list(set(df[df['drug']==selectedDrug]['disease']))[0],
                    "Drug": selectedDrug,
                    "Total SE": len(df[df['drug']==selectedDrug])
                }) 
            peptide_Drug = ['Dulaglutide', 'Omalizumab', 'Mepolizumab', 'Reslizumab', 'Benralizumab', 'Etanercept', 'Adalimumab']
            filteredDrug, peptideDrug = [], []
            # st.write(totalSelectedDrugs)
            for myDrug in totalSelectedDrugs:
                if myDrug not in peptide_Drug: filteredDrug.append(myDrug)
                else: peptideDrug.append(myDrug)
            totalSelectedDrugs = filteredDrug
            # st.write(totalSelectedDrugs)
            # st.write(peptideDrug)       
            with mdInfoCols[0]:
                st.markdown("----")
                st.write(f"##### ***Mono Drug Side Effects***")
                pd.concat(mymseDF).to_sql(f'mse_data_{userID}', con=engine, index=False, if_exists='replace')
                st.dataframe(filterDF.filter_dataframe(pd.read_sql(f'SELECT * FROM `mse_data_{userID}`', con=engine).rename(columns={"disease":"Disease", "drug": "Drug", "se":"Side Effects"})), width=1000000, height=250)
                st.markdown("----")
            with mdInfoCols[1]:
                st.markdown("----")
                st.write(f"##### ***Drug Info***")
                st.dataframe(filterDF.filter_dataframe2(pd.DataFrame(ddata), ), width=1000000, height=250)
                st.markdown("----")
            # st.write(totalSelectedDrugs)
            allDrugNameStrucSMILES = {}
            allDrugNameStrucInchi = {}
            for drugName, Struc_ in zip(pd.read_csv("all_drugs_name_cid_struc_smiles.csv")['drug'], pd.read_csv("all_drugs_name_cid_struc_smiles.csv")['struc']):
                allDrugNameStrucSMILES.update({drugName : Struc_})
            for drugName, Struc_ in zip(pd.read_csv("all_drugs_name_cid_struc_inchi.csv")['drug'], pd.read_csv("all_drugs_name_cid_struc_inchi.csv")['struc']):
                allDrugNameStrucInchi.update({drugName : Struc_})
            # st.write(allDrugNameStrucSMILES)
            smiles, inchi = [], []
            for drg_ in totalSelectedDrugs:
                smiles.append(allDrugNameStrucSMILES[drg_])
            for drg__ in totalSelectedDrugs:
                inchi.append(allDrugNameStrucInchi[drg__])
            # st.write(smiles, inchi)
            unique_combinations = []
            for r in range(1, len(totalSelectedDrugs) + 1):
                unique_combinations.extend(combinations(totalSelectedDrugs, r))
            ucCount = 0
            for uComb in unique_combinations:
                if len(uComb) == 2: ucCount+=1
            predSe = []
            ddCombination = set()
            # allow_display = 0
            if len(totalSelectedDrugs) >= 2:
                if st.button("Predict Drug-Drug Side Effect"):
                    # allow_display += 1
                    myPeptideDrug = ", ".join(peptideDrug)
                    if len(peptideDrug) > 0: st.write('<span style="color: tomato;">'+f"**Important Note: For {myPeptideDrug} drug(s), no discrete structure found on PubChem. Hence, those drug(s) are not considered for making the drug pair(s).**"+'</span>', unsafe_allow_html=True)
                    myC_ = 1
                    with st.spinner('Your query submitted successfully. Please wait...'):
                        for sm_, in_ in zip(range(len(smiles)-1), range(len(inchi)-1)):
                            for sm__, in__ in zip(range(sm_+1,len(smiles)), range(in_+1,len(inchi))):
                                # st.write(f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}")
                                ddCombination.add(f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}")                    
                                os.chdir(rf'{os.getcwd()}')
                                def calculate_descriptors(smiles):
                                    mol = Chem.MolFromSmiles(smiles)
                                    if mol is None:
                                        return "Invalid SMILES"
                                    descriptor_values = [descriptor(mol) for name, descriptor in Descriptors._descList]
                                    logp = Crippen.MolLogP(mol)
                                    des_ = descriptor_values + [logp]
                                    return [0 if np.isnan(x) else x for x in des_]
                                def inchi_calculate_descriptors(smiles):
                                    mol = Chem.MolFromInchi(smiles)
                                    if mol is None:
                                        return "Invalid SMILES"
                                    descriptor_values = [descriptor(mol) for name, descriptor in Descriptors._descList]
                                    logp = Crippen.MolLogP(mol)
                                    des_ = descriptor_values + [logp]
                                    return [0 if np.isnan(x) else x for x in des_]
                                d1_d2_descriptor_names = ["d1_d2_abs_diff_"+desc[0] for desc in Descriptors._descList] + ['d1_d2_abs_diff_LogP']
                                uniqueSideEffects = "".join(open("uniqueSideEffects").readlines()).split("\n")
                                mapppingSE = {}
                                c = 0
                                for sideEffect in uniqueSideEffects:
                                    mapppingSE.update({sideEffect: c})
                                    c+=1
                                try:
                                # st.write(sm_)
                                # st.write(smiles[sm_])
                                # st.write(inchi_calculate_descriptors(smiles[sm_]))
                                # st.write(sm__)
                                # st.write(smiles[sm__])  
                                # st.write(inchi_calculate_descriptors(smiles[sm__]))
                                    s1_s2_abs_diff = np.round(np.abs(np.subtract(np.abs(calculate_descriptors(smiles[sm_])), np.abs(calculate_descriptors(smiles[sm__])))), decimals=6)                            
                                except:         
                                #     st.write(inchi_calculate_descriptors(inchi[in_]))  
                                #     st.write(inchi_calculate_descriptors(inchi[in__]))     
                                    s1_s2_abs_diff = np.round(np.abs(np.subtract(np.abs(inchi_calculate_descriptors(inchi[in_])), np.abs(inchi_calculate_descriptors(inchi[in__])))), decimals=6)            
                                if len(s1_s2_abs_diff) > 0:
                                    col_header = d1_d2_descriptor_names+uniqueSideEffects
                                    x = csr_matrix((0, len(col_header)-1))
                                    c = 0
                                    for lable in range(len(mapppingSE)):
                                        seMat = [0] * len(uniqueSideEffects)
                                        seMat[lable] = 1
                                        merged_array = np.hstack((s1_s2_abs_diff, np.array(seMat[:-1])))
                                        new_row = csr_matrix(merged_array)
                                        x = vstack([x.astype(float), new_row])
                                        c+=1
                                    model = joblib.load('ppmodel.joblib')
                                    model_out = model.predict_proba(x)
                                    mapppingSE = {}
                                    c = 0
                                    for sideEffect in uniqueSideEffects:
                                        mapppingSE.update({c : sideEffect})
                                        c+=1
                                    c = 0
                                    outScore = {}
                                    for i in model_out:
                                        outScore.update({mapppingSE[c]: list(i)[c]})
                                        c+=1
                                    col_header = ["d1_d2_abs_diff_"+desc[0] for desc in Descriptors._descList] + ['d1_d2_abs_diff_LogP']
                                    inpX = csr_matrix((0, len(col_header)))
                                    inpX = vstack([inpX.astype(float), s1_s2_abs_diff])
                                    progress_text = f"Prediction in progress (Drug Combination {myC_}/{ucCount}-> [{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}]). Please wait..."
                                    myC_+=1
                                    my_bar = st.progress(0, text=progress_text)
                                    k = 0
                                    for i, j in zip(range(len(mapppingSE)), outScore.keys()):
                                        os.chdir(rf'{os.getcwd()}'+'/models')
                                        model = joblib.load(f'model_{i}.joblib')
                                        os.chdir(rf'{os.getcwd()}'.replace('/models', ""))
                                        if i%131 == 0:
                                            my_bar.progress(k+9, text=progress_text)
                                            k+=9
                                        try:
                                            specificModelPredict = model.predict(inpX)[0]
                                            if specificModelPredict != -1:
                                                predSe.append({
                                                    "Drug Combination" : f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}",
                                                    "Side Effect with Probability": j+" ["+str(outScore[mapppingSE[i]])+"]" 
                                                })
                                        except:
                                            if outScore[mapppingSE[i]] >= 0.5:
                                                predSe.append({
                                                        "Drug Combination" : f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}",
                                                        "Side Effect with Probability": j+" ["+str(outScore[mapppingSE[i]])+"]" 
                                                    })
                                    my_bar.empty()
                    # st.write(pd.DataFrame(predSe), unsafe_allow_html=True)
                    pd.DataFrame(predSe).to_sql(f'predicted_dd_se_{userID}', con=engine, index=False, if_exists='replace')
                    ddCombSEPredDF = pd.read_sql(f'SELECT * FROM `predicted_dd_se_{userID}`', con=engine)
                    notInSE = 'Infection Upper Respiratory|CMV infection|Brachial plexus injury|Motion sickness|Esophageal spasm|Bladder atony|Nausea|Eating disorder|Pancreatic cancer|Breakthrough bleeding|Thyroid cyst|Leriche syndrome|Eye injury|Candida Infection|EBV infection|Periodontal disease|Cholecystitis acute|Bad breath|Dermatophytosis|Transfusion reaction|Spinal cord injury|Bladder diverticulum|Sunburn|Albuminuria|Ekbom Syndrome|Dandruff|Abuse|Failure to thrive|Infectious mononucleosis|Floaters|Sleep apnea|Trichomoniasis|Bundle branch block right|HIV disease|Renal cancer|Thyroid cancer|Infection|Tremor|Bone marrow transplant|Encephalitis viral|Sick sinus syndrome|Acquired immune deficiency syndrome|Ear infection|Proteinuria|Viral rash NOS|Renal cyst|Acne rosacea|Head injury|Viral pneumonia|Atypical mycobacterial infection|Nasal polyp|Renal agenesis|Bleeding|Peyronies Disease|Anemia aplastic|Diaphragmatic hernia|Faecal incontinence|Bruxism|Animal bite|Pneumocystis carinii infection|Abnormal Laboratory Findings|Faecal impaction|Tinea Capitis|Breast cyst|Sinus headache|Confusion|Carcinoma of Prostate|Tinea cruris|Pyuria|Mitral valve disease NOS|Gallbladder cancer|Balance disorder|Duodenal ulcer perforation|Arthritis bacterial|Anal fistula|Onychomycosis|Mast cell disease|Drowsiness|Coccidioidomycosis|Bulimia|Alcohol consumption|Supernumerary nipple|Breast cancer|Soft tissue infection|Vitamin B 12 deficiency|Cystitis Interstitial|Arthritis infective|Oily Skin|Femoral neck fracture|Bacterial infection|Bacterial endocarditis|Abnormal ECG|Kidney transplant|Difficulty in walking|Salivary gland enlargement|Acute kidney failure|External ear infection|Basal cell carcinoma|Choriocarcinoma|Lyme Disease|Abnormal cervical smear|Lung neoplasm malignant|Hepatitis B|Alcohol abuse|Vitamin D Deficiency|Pneumocystis carinii pneumonia|Tuberculin test positive|Tinea|Rib fracture|Acid reflux|Acne|Post thrombotic syndrome|Night sweat|Mixed connective tissue disease|Ejaculation Premature|Chicken pox|Diarrhea infectious|Xerosis|Decreased lacrimation|Right heart failure|Traumatic arthropathy|ADVERSE DRUG EFFECT|CYSTO|Streptococcal infection|Cystic Fibrosis|Cholecystectomies|Gastroenteritis viral|Parasitic infection intestinal|Cholecystitis chronic|Typhoid|Nightmare|Soft tissue injuries|Chest infection|Polio|Heart attack|Ovarian cancer|Rubella|Ulcer|Abdominal hernia|Skin abrasion|Kidney failure|Fractured pelvis NOS|Adenocarcinoma|Pilonidal cyst|Umbilical hernia|Cryptococcosis|Nocturia|Hepatitis B surface antigen positive|Eyelid diseases|Aseptic necrosis bone|Hepatorenal syndrome|Intervertebral Disc Herniation|Brain neoplasm|Esophageal rupture|Hypercalcinuria|Adrenal carcinoma|Deglutition disorder|Swollen scrotum|Whiplash Injury|Hernia Inguinal|Wrist fracture|Abnormal mammogram|Carcinoid syndrome|Abnormal vision|Heat stroke|Sinus tachycardia|Tension headache|Psychosomatic disease|Viral Pharyngitis|Obesity|Synovial cyst|Dacrocystitis|Drug addiction|Abnormal LFTs|Carcinoma of the colon|Peripheral nerve injury|Tooth Impacted|Bacterial vaginitis|Gonorrhea|Dry skin|Infection Viral|Duodenal ulcer haemorrhage|Cryptorchidism|Rotator cuff syndrome|Fracture nonunion|Tetanus|Pancreatic pseudocyst|Sleep walking|Coma|Bladder cancer|Ovarian Cyst|Arteriosclerotic heart disease|Abnormal movements|Nephrotic syndrome|Phobia|Acidosis|Arthritis rheumatoid|Wound dehiscence|Spinal Compression Fracture|Anthrax|Bundle branch block left|Bone Fracture Spontaneous|Superior vena cava syndrome|Drug withdrawal|Tinea pedis|Nodule Skin|Vitamin B deficiency|Body tinea|Vaginal dysplasia|Dehydration|Caesarean Section|Nasal septal perforation|Black stools|Aspergillosis|Pneumonia Klebsiella|Respiratory failure|Mycobacterium tuberculosis infection|Head ache|Hepatic failure|Acute brain syndrome|Tooth disease|Diphtheria|Arthropathy|Septic abortion|Bone marrow failure|Psychosexual disorder|Dizziness|Endometrial cancer|Anaemia hypochromic|Myoglobinuria|Thyroid neoplasia|Abscess|Bacterial pneumonia|Breast Lump|Septic shock|Conjunctivitis viral|Food poisoning|Cardiac failure|Mycosis fungoides|Hepatitis toxic|Renal mass|Acromegaly|Adenoid hypertrophy|Cutaneous mycosis|Legionella|Fungal disease|Humerus fracture|Salivary Gland Calculus|Flu|Thyroidectomy|Flashing lights|Femur fracture|Skin Striae|Infection Urinary Tract|Uterine infection|Tendon injury|Bulging|Abdominal pain upper|Flashbacks|Hepatitis C antibody positive|Cervical vertebral fracture|Adjustment disorder|Injury of neck|Spinal fracture|Eosinophilic pneumonia acute|Renal colic|Hip fracture|Scar|Hepatitis A|Agitated|Urogenital abnormalities|Polyuria|Bacterial conjunctivitis|Transurethral resection of the prostate|Hernia hiatal|Anal fissure|Incisional hernia|Defaecation urgency|Cryptosporidiosis|Neumonia|Hepatitis C|Urosepsis|Sinus arrest|Pneumonia staphylococcal|Back injury|Cutaneous candidiasis|Thyroid adenoma|Hair disease|Adenomyosis|Sjogrens syndrome|Narcolepsy|Anal pruritus|Heat rash|Eye infection|Hallucination|Cardiac disease|Spider angioma|Esophageal stenosis|Dermoid cyst|Vaginal prolapse|Vaginal discharge|Burns Second Degree|Sexually transmitted diseases|Pelvic infection|Esophageal cancer|Cystic acne|Tinea versicolor|Bone fracture|Abnormal EEG|Sinus bradycardia|Ankle fracture|Meningitis Viral|Gastric Cancer|Night cramps|Carcinoma of the cervix|Brain concussion|Nodule|Feeling unwell|Thyroid disease|Flatulence|Glucosuria'
                    ddCombSEPredDF = ddCombSEPredDF[~ddCombSEPredDF['Side Effect with Probability'].str.contains(notInSE, case=False)]
                    noSideEffect = []
                    totSideEffectDF = []
                    for i_i in ddCombination:
                        if len(ddCombSEPredDF[ddCombSEPredDF['Drug Combination']==i_i]) == 0:
                            noSideEffect.append({
                                "Drug Combination": i_i,
                                "Side Effect with Probability": "No Side Effect [1.0]"
                            })
                        totSideEffectDF.append({
                            "Drug Combination": i_i,
                            "Total No. of Side Effect": len(ddCombSEPredDF[ddCombSEPredDF['Drug Combination']==i_i])
                        })
                    xx = pd.DataFrame(noSideEffect)
                    finalDFDB = pd.concat([ddCombSEPredDF, xx], ignore_index=True)
                    totSideEffectDFDB = pd.DataFrame(totSideEffectDF).sort_index(ascending=False)
                    finalDFDB.to_sql(f'final_dd_se_{userID}', con=engine, index=False, if_exists='replace')
                    totSideEffectDFDB.to_sql(f'tot_side_effect_df_{userID}', con=engine, index=False, if_exists='replace')    
                else: pass
            else:
                if len(peptideDrug) > 0 and len(totalSelectedDrugs) == 1:
                    jpd = ", ".join(peptideDrug)
                    st.warning(f"Atleast 2 non-peptide drugs are require to making the drug pair(s). {jpd} drug(s) can't be consider, since this all are peptide based drugs!")
                if len(totalSelectedDrugs) == 1 and len(peptideDrug) == 0:
                    st.warning(f"Atleast 2 drugs are require to making the drug pair(s).")

    # else:
    #     go_backend.append("")
    filterDict = {
                'Cardiac': ['Cardiac', 'heart', 'pericard', 'carotid', 'arterial', 'atri', 'ventri', 'vascul'],
                'Renal': ['Renal', 'Kidney'],
                'Liver': ['Hepato', 'Hepatic', 'liver'],
                'Cervical': ['Cervical', 'cervix'],
                'Breast': ['Breast'],
                'Respiratory': ['Respiratory', 'pulmonary', 'lung', 'Pneumo'],
                'Brain': ['Brain', 'Cerebral', 'Cerebellar'],
                'Eye': ['Eye', 'Cornea', 'Retin'],
                'Digestive': ['Gastr', 'Intestin', 'Duoden', 'bowel'],
                'Skin': ['Skin', 'derma'],
                'Ortho': ['Bone', 'joint', 'muscle', 'musculoskeletal', 'muscular']
            }
    # st.write(allow_display)
    if len(totalSelectedDrugs) >= 2:
        if st.checkbox("Display result", help="Please enable **after** the prediction"):
            # st.write(totSD__)
            query_finalDF = f'SELECT * FROM `final_dd_se_{userID}`'
            finalDF = pd.read_sql(query_finalDF, con=engine)
            finalDF2 = finalDF.copy()
            query_totSideEffectDF = f'SELECT * FROM `tot_side_effect_df_{userID}`'
            df_from_db_totSideEffectDF = pd.read_sql(query_totSideEffectDF, con=engine)
            if len(finalDF) > 0:
                st.markdown("####")
                st.markdown("----")
                st.markdown("##### ***Drug Drug Side Effect Visualizer***")
                if st.checkbox("Enable Drug Drug Side Effect Visualizer (Not Always Recomended)", help="It is recomended that don't enable this option in case of large number of predicted side effects. It will takes a bit longer to load the network graphics/the browser may unresponsive at that moment."):
                    finalDF_ = finalDF.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                    finalDF_['val'] = 1
                    G = nx.from_pandas_edgelist(finalDF_,
                                               source="Drug Combination",
                                                target="Side Effect with Probability",
                                                edge_attr="val",
                                                create_using=nx.Graph()
                                               )
                    net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                    node_degree = dict(G.degree)
                    nx.set_node_attributes(G, node_degree, 'size')
                    partition = cl.best_partition(G)
                    nx.set_node_attributes(G, partition, 'group')
                    net.from_nx(G)
                    net.save_graph("ddse.html")
                    with open("ddse.html",'r') as f: 
                        html_data = f.read()
                    agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                    if agree_:
                        net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                        node_degree = dict(G.degree)
                        nx.set_node_attributes(G, node_degree, 'size')
                        partition = cl.best_partition(G)
                        nx.set_node_attributes(G, partition, 'group')
                        net.from_nx(G)
                        net.save_graph("ddse.html")
                        with open("ddse.html",'r') as f: 
                            html_data = f.read()
                    st.components.v1.html(html_data,height=800)
                st.markdown("----")
                st.markdown("####")
                ddCols = st.columns([2,1])
                getDF = ""
                with ddCols[0]: 
                    st.markdown("----")
                    st.markdown("##### ***Poly Drug Side Effects [Predicted]***")
                    finalDF[['Side Effect', 'Probability']] = finalDF['Side Effect with Probability'].str.split('[', expand=True)
                    finalDF['Probability'] = finalDF['Probability'].str.rstrip(']')
                    finalDF = finalDF.drop('Side Effect with Probability', axis=1)
                    getDF = finalDF
                    st.dataframe(filterDF.filter_dataframe3(finalDF), width=1000000, height=250)
                    st.markdown("----") 
                with ddCols[1]: 
                    st.markdown("----")
                    st.markdown("##### ***Drug Combination Info***")
                    st.dataframe(filterDF.filter_dataframe4(df_from_db_totSideEffectDF), width=1000000, height=250)
                    st.markdown("----")
                st.markdown("----")
                st.markdown("##### ***Analyze Poly Drug Side Effects [Predicted] More Specifically***")
                if st.checkbox("Enable"):        
                    option_radio = st.radio(
                        "**Select an Option**",
                        ['None','Cardiac', 'Renal', 'Liver', 'Cervical', 'Breast', 'Respiratory', 'Brain', 'Eye', 'Digestive', 'Skin', 'Ortho', 'Other'],
                        # index=None
                        horizontal=True
                    )
                    # st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    if option_radio != 'None':
                        if option_radio != 'Other':
                            filterCols_1 = st.columns([2,1])
                            with filterCols_1[0]:
                                st.markdown('<div style="background-color:Bisque;font-size:50px;text-align:center;"></div>', unsafe_allow_html=True)
                                mydf1 = getDF[getDF['Side Effect'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                st.dataframe(filterDF.filter_dataframe5(mydf1), width=1000000, height=250)
                            with filterCols_1[1]:
                                # st.write(getDF.columns)
                                st.markdown("#####")
                                mydf1 = getDF[getDF['Side Effect'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                comb = mydf1.drop(['Side Effect', 'Probability'], axis=1)
                                # st.write(comb)
                                value_counts_df = comb.value_counts().reset_index()
                                # st.write(comb['Drug Combination'].str.contains("|".join(filterDict['Cardiac']), case=False))
                                value_counts_df.columns = ['Drug Combination', 'Total No. of Side Effect']
                                st.dataframe(filterDF.filter_dataframe6(value_counts_df), width=1000000, height=250)
                            # st.write(finalDF2)
                            st.markdown("###### ***Drug Drug Side Effect Visualizer [SPECIFIC]***")
                            if st.checkbox("Enable (Not Always Recomended)", help="It is recomended that don't enable this option in case of large number of predicted side effects. It will takes a bit longer to load the network graphics/the browser may unresponsive at that moment."):
                                finalDF2_ = finalDF2[finalDF2['Side Effect with Probability'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                finalDF_specific = finalDF2_.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                                finalDF_specific['val'] = 1
                                G = nx.from_pandas_edgelist(finalDF_specific,
                                                           source="Drug Combination",
                                                            target="Side Effect with Probability",
                                                            edge_attr="val",
                                                            create_using=nx.Graph()
                                                           )
                                net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                                node_degree = dict(G.degree)
                                nx.set_node_attributes(G, node_degree, 'size')
                                partition = cl.best_partition(G)
                                nx.set_node_attributes(G, partition, 'group')
                                net.from_nx(G)
                                net.save_graph("ddse.html")
                                with open("ddse.html",'r') as f: 
                                    html_data = f.read()
                                agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                                if agree_:
                                    net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                                    node_degree = dict(G.degree)
                                    nx.set_node_attributes(G, node_degree, 'size')
                                    partition = cl.best_partition(G)
                                    nx.set_node_attributes(G, partition, 'group')
                                    net.from_nx(G)
                                    net.save_graph("ddse_specific.html")
                                    with open("ddse_specific.html",'r') as f: 
                                        html_data = f.read()
                                st.components.v1.html(html_data,height=800)
                        else:
                            # allKW = list(filterDict.values())
                            # st.warning("|".join(list(chain(*allKW))))
                            allKW = "Cardiac|heart|pericard|carotid|arterial|atri|ventri|vascul|Renal|Kidney|Hepato|Hepatic|liver|Cervical|cervix|Breast|Respiratory|pulmonary|lung|Pneumo|Brain|Cerebral|Cerebellar|Eye|Cornea|Retin|Gastr|Intestin|Duoden|bowel|Skin|derma|Bone|joint|muscle|musculoskeletal|muscular"
                            filterCols_1 = st.columns([2,1])
                            with filterCols_1[0]:
                                mydf1 = getDF[~getDF['Side Effect'].str.contains(allKW, case=False)]
                                st.dataframe(filterDF.filter_dataframe5(mydf1), width=1000000, height=250)
                            with filterCols_1[1]:
                                # st.write(getDF.columns)
                                mydf1 = getDF[~getDF['Side Effect'].str.contains(allKW, case=False)]
                                comb = mydf1.drop(['Side Effect', 'Probability'], axis=1)
                                # st.write(comb)
                                value_counts_df = comb.value_counts().reset_index()
                                # st.write(comb['Drug Combination'].str.contains("|".join(filterDict['Cardiac']), case=False))
                                value_counts_df.columns = ['Drug Combination', 'Total No. of Side Effect']
                                st.dataframe(filterDF.filter_dataframe6(value_counts_df), width=1000000, height=250)
                            # st.write(finalDF2)
                            st.markdown("###### ***Drug Drug Side Effect Visualizer [SPECIFIC]***")
                            if st.checkbox("Enable (Not Always Recomended)"):
                                finalDF2_ = finalDF2[~finalDF2['Side Effect with Probability'].str.contains(allKW, case=False)]
                                finalDF_specific = finalDF2_.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                                finalDF_specific['val'] = 1
                                G = nx.from_pandas_edgelist(finalDF_specific,
                                                           source="Drug Combination",
                                                            target="Side Effect with Probability",
                                                            edge_attr="val",
                                                            create_using=nx.Graph()
                                                           )
                                net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                                node_degree = dict(G.degree)
                                nx.set_node_attributes(G, node_degree, 'size')
                                partition = cl.best_partition(G)
                                nx.set_node_attributes(G, partition, 'group')
                                net.from_nx(G)
                                net.save_graph("ddse.html")
                                with open("ddse.html",'r') as f: 
                                    html_data = f.read()
                                agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                                if agree_:
                                    net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                                    node_degree = dict(G.degree)
                                    nx.set_node_attributes(G, node_degree, 'size')
                                    partition = cl.best_partition(G)
                                    nx.set_node_attributes(G, partition, 'group')
                                    net.from_nx(G)
                                    net.save_graph("ddse_specific.html")
                                    with open("ddse_specific.html",'r') as f: 
                                        html_data = f.read()
                                st.components.v1.html(html_data,height=800)
                    else: pass
                st.markdown("----")
    try: 
        if len(option5) == 0 and len(go_backend) == 22: go_backend+=["","",""]
    except: pass
    try:
        if len(option5) == 0 and len(selectedTBDrug) > 0: go_backend.insert(23, "")
    except: pass
    try:
        if len(option5) == 0 and len(selectedTBDrug) == 0: go_backend.append("")
    except: pass
    cntrl = 0
    try:
        if len(option5) >= 0:
            # st.write(check_patient_conformation)
            # st.write(go_backend)
                check_patient_conformation.pop(0)
                # st.write(len(check_patient_conformation))
                if len("".join([str(x) for x in check_patient_conformation])) > 0:
                    check_patient_data = 0
                    # try:
                    for cpd in check_patient_conformation:
                            if len(str(cpd)) == 0: check_patient_data+=1
                    # except: pass
                    if check_patient_data > 0:
                        st.error("One or more compulsory field is blank. Please fill all :red[*] section(s) to save and download the report!")
                    if check_patient_data == 0:                    
                            requireNextVisit = st.selectbox("Next Visit", ["","Require", "Not require"])
                            if len(requireNextVisit) == 0: st.warning("Please select a option for next visit date for patient!")
                            else:
                                if requireNextVisit == "Require":
                                    nextVisit = st.date_input("Select a date")
                                    dtSplit = str(nextVisit).split("-")
                                    dt_ = datetime.now().strftime('%Y/%m/%d %H:%M:%S').split(" ")[0]
                                    dt__ = dt_.split("/")
                                    go_backend.append(f"{dt__[2]}/{dt__[1]}/{dt__[0]}")
                                    go_backend.append(f"{dtSplit[2]}/{dtSplit[1]}/{dtSplit[0]}")
                                    currentDate = datetime(int(dt_.split("/")[0]), int(dt_.split("/")[1]), int(dt_.split("/")[2]))
                                    dt2_ = str(nextVisit).split("-")
                                    selectedDate = (datetime(int(dt2_[0]), int(dt2_[1]), int(dt2_[2])))
                                    dateDiff = selectedDate - currentDate                        
                                    if dateDiff.days > 0:
                                        if st.button("Save Data & Generate Report"):
                                            if patientType == "New Patient":
                                                if varifydata == 4:
                                                    go_backend.pop(3)                     
                                                    dataToInsert = '"'+'", "'.join([str(x) for x in go_backend])+'"'
                                                    cursor.execute(f'''INSERT INTO patient_data (`uniqueusr`, `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `patient_tb_health`, `infection_age`, `treatment_status`, `country_code`, `contact_no`, `address`, `continent`, `country`, `state`, `pin`, `medical_history`, `travel_history`, `strain_info`, `dst_done`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `date_time`, `next_visit`) VALUES ({dataToInsert})''')
                                                    cursor.execute("USE u164935248_trial_pttrs")
                                                    cursor.execute(f"SELECT `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `address`, `state`, `pin`, `country`, `continent`, `country_code`, `contact_no`, `patient_tb_health`, `infection_age`, `treatment_status`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `next_visit` from patient_data WHERE uniqueusr = '{userID}' AND patient_id = {newPatientID} ORDER BY `visit_no` DESC LIMIT 1")
                                                    try:
                                                        pddb = cursor.fetchall()[0]
                                                        id, visit, name, age, gender, bg, contact, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, nextVisit = pddb[0], pddb[1], pddb[2], pddb[3], pddb[4], pddb[5], "".join([pddb[11].split('(')[0], pddb[12]]), pddb[13], pddb[14], pddb[15], pddb[16], pddb[17], pddb[18], pddb[19], pddb[20], pddb[21], pddb[22]
                                                        address_ = ", ".join(pddb[6:11])
                                                        if len(address_) > 80:
                                                            address_ = address_[:80]+" ..."
                                                        cursor.execute(f"SELECT `salutation`, `first_name`, `middle_name`, `last_name`, `speciality`, `short_name` from usr_info WHERE uniqueusr = '{userID}'")
                                                        drdb = cursor.fetchall()[0]
                                                        drName, speciality = " ".join(drdb[0:4]), drdb[4]
                                                        if len(drName[3:]) > 25:
                                                            drName = "Dr. "+drdb[5]
                                                        generate_report(id, visit, name, age, gender, bg, address_, contact, drName, speciality, nextVisit, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, userID)
                                                        st.success("Data saved successfully and report generated successfully.")
                                                        with open(f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf", "rb") as file:
                                                            btn=st.download_button(
                                                        label="Download Report",
                                                        data=file,
                                                        file_name=f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf",
                                                        mime="application/octet-stream",
                                                    )
                                                    except:
                                                        st.error("Fill all the fields correctly. Then click on 'Save Data' followed by 'Generate Report'.")
                                                else: st.warning("Something is going wrong. Please fill the required fields appropriately")
                                            if patientType == "Re-visit":
                                                if varifydata == 4:
                                                    go_backend.insert(0, userID)
                                                    try:
                                                        if len(option5) == 0: 
                                                            go_backend.insert(24, "")
                                                            go_backend.pop(26)
                                                    except: pass
                                                    dataToInsert = '"'+'", "'.join([str(x) for x in go_backend])+'"'
                                                    cursor.execute(f'''INSERT INTO patient_data (`uniqueusr`, `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `patient_tb_health`, `infection_age`, `treatment_status`, `country_code`, `contact_no`, `address`, `continent`, `country`, `state`, `pin`, `medical_history`, `travel_history`, `strain_info`, `dst_done`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `date_time`, `next_visit`) VALUES ({dataToInsert})''')
                                                    cursor.execute("USE u164935248_trial_pttrs")
                                                    cursor.execute(f"SELECT `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `address`, `state`, `pin`, `country`, `continent`, `country_code`, `contact_no`, `patient_tb_health`, `infection_age`, `treatment_status`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `next_visit` from patient_data WHERE uniqueusr = '{userID}' AND patient_id = {patientID} ORDER BY `visit_no` DESC LIMIT 1")
                                                    try:
                                                        pddb = cursor.fetchall()[0]
                                                        id, visit, name, age, gender, bg, contact, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, nextVisit = pddb[0], pddb[1], pddb[2], pddb[3], pddb[4], pddb[5], "".join([pddb[11].split('(')[0], pddb[12]]), pddb[13], pddb[14], pddb[15], pddb[16], pddb[17], pddb[18], pddb[19], pddb[20], pddb[21], pddb[22]
                                                        address_ = ", ".join(pddb[6:11])
                                                        if len(address_) > 80:
                                                            address_ = address_[:80]+" ..."
                                                        cursor.execute(f"SELECT `salutation`, `first_name`, `middle_name`, `last_name`, `speciality`, `short_name` from usr_info WHERE uniqueusr = '{userID}'")
                                                        drdb = cursor.fetchall()[0]
                                                        drName, speciality = " ".join(drdb[0:4]), drdb[4]
                                                        if len(drName[3:]) > 25:
                                                            drName = "Dr. "+drdb[5]
                                                        generate_report(id, visit, name, age, gender, bg, address_, contact, drName, speciality, nextVisit, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, userID)
                                                        st.success("Data saved successfully and report generated successfully.")
                                                        with open(f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf", "rb") as file:
                                                            btn=st.download_button(
                                                        label="Download Report",
                                                        data=file,
                                                        file_name=f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf",
                                                        mime="application/octet-stream",
                                                    )
                                                    except:
                                                        st.error("Fill all the fields correctly. Then click on 'Save Data' followed by 'Generate Report'.")
                                                else: st.warning("Something is going wrong. Please fill the required fields appropriately")
                                    if dateDiff.days < 0: 
                                        st.warning("Next visit can't be any past day!")
                                    if dateDiff.days == 0:
                                        st.warning("Next visit can't be same date as today's!")
                                if requireNextVisit == "Not require":
                                    dt_ = datetime.now().strftime('%Y/%m/%d %H:%M:%S').split(" ")[0]
                                    dt__ = dt_.split("/")
                                    go_backend.append(f"{dt__[2]}/{dt__[1]}/{dt__[0]}") 
                                    go_backend.append("Not require")
                                    if st.button("Save Data & Generate Report"):
                                        if patientType == "New Patient":
                                            if varifydata == 4:
                                                go_backend.pop(3)                    
                                                dataToInsert = '"'+'", "'.join([str(x) for x in go_backend])+'"'
                                                cursor.execute(f'''INSERT INTO patient_data (`uniqueusr`, `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `patient_tb_health`, `infection_age`, `treatment_status`, `country_code`, `contact_no`, `address`, `continent`, `country`, `state`, `pin`, `medical_history`, `travel_history`, `strain_info`, `dst_done`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `date_time`, `next_visit`) VALUES ({dataToInsert})''')
                                                cursor.execute("USE u164935248_trial_pttrs")
                                                cursor.execute(f"SELECT `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `address`, `state`, `pin`, `country`, `continent`, `country_code`, `contact_no`, `patient_tb_health`, `infection_age`, `treatment_status`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `next_visit` from patient_data WHERE uniqueusr = '{userID}' AND patient_id = {newPatientID} ORDER BY `visit_no` DESC LIMIT 1")
                                                try:
                                                    pddb = cursor.fetchall()[0]
                                                    id, visit, name, age, gender, bg, contact, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, nextVisit = pddb[0], pddb[1], pddb[2], pddb[3], pddb[4], pddb[5], "".join([pddb[11].split('(')[0], pddb[12]]), pddb[13], pddb[14], pddb[15], pddb[16], pddb[17], pddb[18], pddb[19], pddb[20], pddb[21], pddb[22]
                                                    address_ = ", ".join(pddb[6:11])
                                                    if len(address_) > 80:
                                                        address_ = address_[:80]+" ..."
                                                    cursor.execute(f"SELECT `salutation`, `first_name`, `middle_name`, `last_name`, `speciality`, `short_name` from usr_info WHERE uniqueusr = '{userID}'")
                                                    drdb = cursor.fetchall()[0]
                                                    drName, speciality = " ".join(drdb[0:4]), drdb[4]
                                                    if len(drName[3:]) > 25:
                                                        drName = "Dr. "+drdb[5]
                                                    generate_report(id, visit, name, age, gender, bg, address_, contact, drName, speciality, nextVisit, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, userID)
                                                    st.success("Data saved successfully and report generated successfully.")
                                                    with open(f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf", "rb") as file:
                                                        btn=st.download_button(
                                                    label="Download Report",
                                                    data=file,
                                                    file_name=f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf",
                                                    mime="application/octet-stream",
                                                    )
                                                except:
                                                    st.error("Fill all the fields correctly. Then click on 'Save Data' followed by 'Generate Report'.")
                                            else: st.warning("Something is going wrong. Please fill the required fields appropriately")
                                        if patientType == "Re-visit":
                                            if varifydata == 4:
                                                go_backend.insert(0, userID)
                                                try:
                                                    if len(option5) == 0: 
                                                        go_backend.insert(24, "")
                                                        go_backend.pop(26)
                                                except: pass
                                                # st.write(go_backend) 
                                                dataToInsert = '"'+'", "'.join([str(x) for x in go_backend])+'"'
                                                cursor.execute(f'''INSERT INTO patient_data (`uniqueusr`, `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `patient_tb_health`, `infection_age`, `treatment_status`, `country_code`, `contact_no`, `address`, `continent`, `country`, `state`, `pin`, `medical_history`, `travel_history`, `strain_info`, `dst_done`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `date_time`, `next_visit`) VALUES ({dataToInsert})''')
                                                cursor.execute("USE u164935248_trial_pttrs")
                                                cursor.execute(f"SELECT `patient_id`, `visit_no`, `name`, `age`, `gender`, `blood_group`, `address`, `state`, `pin`, `country`, `continent`, `country_code`, `contact_no`, `patient_tb_health`, `infection_age`, `treatment_status`, `test_name`, `known_amr_strain`, `amr_strain_resistant_drug`, `amc`, `selected_tb_drug`, `selected_amc_drug`, `next_visit` from patient_data WHERE uniqueusr = '{userID}' AND patient_id = {patientID} ORDER BY `visit_no` DESC LIMIT 1")
                                                try:
                                                    pddb = cursor.fetchall()[0]
                                                    id, visit, name, age, gender, bg, contact, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, nextVisit = pddb[0], pddb[1], pddb[2], pddb[3], pddb[4], pddb[5], "".join([pddb[11].split('(')[0], pddb[12]]), pddb[13], pddb[14], pddb[15], pddb[16], pddb[17], pddb[18], pddb[19], pddb[20], pddb[21], pddb[22]
                                                    address_ = ", ".join(pddb[6:11])
                                                    if len(address_) > 80:
                                                        address_ = address_[:80]+" ..."
                                                    cursor.execute(f"SELECT `salutation`, `first_name`, `middle_name`, `last_name`, `speciality`, `short_name` from usr_info WHERE uniqueusr = '{userID}'")
                                                    drdb = cursor.fetchall()[0]
                                                    drName, speciality = " ".join(drdb[0:4]), drdb[4]
                                                    if len(drName[3:]) > 25:
                                                        drName = "Dr. "+drdb[5]
                                                    generate_report(id, visit, name, age, gender, bg, address_, contact, drName, speciality, nextVisit, tb_health, infection_age, treatment, testNames, amrStrain, resistantDrugs, amcDetails, tbDrug, amcDrug, userID)
                                                    st.success("Data saved successfully and report generated successfully.")
                                                    with open(f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf", "rb") as file:
                                                        btn=st.download_button(
                                                    label="Download Report",
                                                    data=file,
                                                    file_name=f"tb_report_{userID}_pid_{id}_vno_{visit}.pdf",
                                                    mime="application/octet-stream",
                                                    )
                                                except:
                                                    st.error("Fill all the fields correctly. Then click on 'Save Data' followed by 'Generate Report'.")
                                            else: st.warning("Something is going wrong. Please fill the required fields appropriately")
    except: pass
    try:
        if len(requireNextVisit) > 0 and dateDiff.days > 0:
            if st.button("Next Patient"):
                try:
                    os.remove(f"tb_report_{userID}_pid_{id_-1}_vno_{newVisitID_}.pdf")
                    # pyautogui.hotkey('f5')
                except:
                    os.remove(f"tb_report_{userID}_pid_{id_-1}_vno_{getvisitno}.pdf")
                    # pyautogui.hotkey('f5')
    except: pass
    try:
        if requireNextVisit == "Not require":
            if st.button("Next Patient"):
                try:
                    os.remove(f"tb_report_{userID}_pid_{id_}_vno_{newVisitID_-1}.pdf")
                    # pyautogui.hotkey('f5')
                except:
                    os.remove(f"tb_report_{userID}_pid_{id_}_vno_{getvisitno}.pdf")
                    # pyautogui.hotkey('f5')
    except: pass

# def app_decision(userID):
#     config = {
#         'user': 'u164935248_trial_pttrs',
#         'password': 'Trial_pttrs1',
#         'host': '89.117.157.103',
#         'use_pure': True,
#         'raise_on_warnings': True,
#     }
#     connect2 = mc.connect(**config)
#     cursor = connect2.cursor()
#     cursor.execute("USE u164935248_trial_pttrs")
#     cursor.execute(f"SELECT regas FROM usr_info WHERE uniqueusr = '{userID}'")
#     getRegAs = cursor.fetchall()[0][0]
#     if getRegAs == "Doctor":
#         doctorWala()
#     else:
#         pass

def other():    
    st.title("Personalized Tuberculosis Treatment Recommender System (PTTRS)")
    # st.markdown("##### A Precision-Medicine Based Application for Recommending Personalized Treatment to Tuberculosis Patients"+" (<span style='color: Tomato'><i>Trial Version</i></span>)", unsafe_allow_html=True)
    # st.markdown("<span style='color: Tomato'> <i>This interface is the prototype of the core part of actual application.</i></span>", unsafe_allow_html=True)
    st.markdown("####")
    config = {
        'user': 'u164935248_trial_pttrs',
        'password': 'Trial_pttrs1',
        'host': '89.117.157.103',
        'use_pure': True,
        'raise_on_warnings': True,
    }
    connect2 = mc.connect(**config)
    cursor = connect2.cursor()
    userID = ''
    
    engine = create_engine('mysql://u164935248_trial_pttrs:Trial_pttrs1@89.117.157.103/u164935248_trial_pttrs')
    
    # authenticator = Auth
    
    
    # name, authentication_status, username = sauth.login('Login', 'main')
    # if authentication_status:
    #     sauth.logout('Logout', 'main')
    #     if username == 'jsmith':
    #         st.write(f'Welcome *{name}*')
    #         st.title('Application 1')
    #     elif username == 'rbriggs':
    #         st.write(f'Welcome *{name}*')
    #         st.title('Application 2')
    # elif authentication_status == False:
    #     st.error('Username/password is incorrect')
    # elif authentication_status == None:
    #     st.warning('Please enter your username and password')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("----")
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute("SELECT * FROM data_geo_loc")
        option1Data = cursor.fetchall()
        inputDataList1 = []
        # inputDataList1.append('')
        for i in option1Data:
            inputDataList1.append(i[0])
        st.write("##### ***Location information***")
        option1 = st.multiselect(
            'Enter geographical location or travel history [optional]', sorted(
                list(set(inputDataList1)))
        )
    
        locs = []
        locsStrain = []
    
        if len(option1) == 0:
            cursor.execute(f"SELECT * FROM `data_geo_loc`")
            outData1 = cursor.fetchall()
            for i in outData1:
                locs.append(i[0])
                locsStrain.append(i[1][0].upper()+i[1][1:])
            # st.write(locs)
    
            df1 = {
                "Geographical Location": locs,
                "TB Strain": locsStrain
            }
            st.caption("Display all TB strain based on geographical location [default] (data sorted by Geographical Location)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
    
        else:
            for op in option1:
                cursor.execute(
                    f"SELECT * FROM `data_geo_loc` WHERE geoloc LIKE '%{op}%'")
                outData1 = cursor.fetchall()
                for i in outData1:
                    locs.append(i[0])
                    locsStrain.append(i[1][0].upper()+i[1][1:])
            df1 = {
                "Geographical Location": locs,
                "TB Strain": locsStrain
            }    
            st.caption("Search result (data sorted by Geographical Location)")
            st.dataframe(pd.DataFrame(df1), width=600, height=200)
        st.markdown("----")
    with col2:
        st.markdown("----")
        cursor.execute("USE u164935248_trial_pttrs")
        cursor.execute("SELECT * FROM data_geo_loc")
        option1Data = cursor.fetchall()
        inputDataList1 = []
        inputDataList1.append('')
        for i in option1Data:
            inputDataList1.append(i[1][0].upper()+i[1][1:])
        st.write("##### ***Strain information***")
        option1 = st.selectbox(
            'Enter TB strain(s) [optional]', sorted(tuple(set(inputDataList1)))
        )
    
        cursor.execute(
            f"SELECT * FROM `data_geo_loc` WHERE strain LIKE '%{option1}%' ORDER BY strain")
        outData1 = cursor.fetchall()
    
        locs = []
        locsStrain = []
    
        for i in outData1:
            locs.append(i[0])
            locsStrain.append(i[1])
    
        df1 = {
            "TB Strain": locsStrain,
            "Geographical Location": locs
        }
    
        if len(locs) == 351:
            st.caption("Display all geographical location based on TB strain [default] (data sorted by TB strain)")
        else:
            st.caption("Search result (data sorted by TB strain)")
        st.dataframe(pd.DataFrame(df1), width=600, height=200)
        st.markdown("----")
    st.markdown("####")
    # st.markdown("####")
    # st.markdown("####")
    opt4 = []
    amrdrugs = []
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("----")
        st.write("##### ***AMR (Antimicrobial Resistance) report and strain***")
        option3 = st.selectbox("Have you done drug susceptibility testing (DST) or any other test for AMR detection??", ["", "Yes", "No"])
        if option3 == "Yes":
            st.text_input("AMR strain name [optional]")
            cursor.execute("SELECT `Drug for TB` FROM `data_anti-tb_drugs_sideeffects`")
            amrdata = cursor.fetchall()
            for i in amrdata:
                amrdrugs.append(i[0][0].upper()+i[0][1:])
            option4 = st.multiselect("Resistant drug(s)", amrdrugs) 
            opt4+=option4
        if option3 == "No":
            cursor.execute("SELECT `Drug for TB` FROM `data_anti-tb_drugs_sideeffects`")
            amrdata = cursor.fetchall()
            for i in amrdata:
                amrdrugs.append(i[0][0].upper()+i[0][1:])
            st.warning("We can't proceed without a lab diagnosis for this section. Please move forward to the next section")
        st.markdown("----")
    with col4:
        st.markdown("----")
        st.write("##### ***AMC (Associated Medical Condition) details***")
        cursor.execute("SELECT `disease` FROM `data_amc_drugs`")
        amcDiseaseData = cursor.fetchall()
        disease = []
        for i in amcDiseaseData:
            disease.append(i[0][0].upper()+i[0][1:].replace("iv/aids", "IV/AIDS"))
        option5 = st.multiselect("Select an associative disease with TB", sorted(disease))
    
        disearDrugDict = {
            "Diabetes" : ["Rifampin", "Isoniazid"],
            "HIV/AIDS" : ["Rifampin", "Bedaquiline", "Delamanid"],
            "Thyroid": "",
            "Asthma": "",
            "Rheumatoid arthritis" : ["Isoniazid", "Pyrazinamide"]
        }
        notpresdrug = []
        for x in option5:
            notpresdrug+=disearDrugDict[x]
        notpresdrug+=opt4
        st.markdown("----")
        # st.write(set(notpresdrug))
    
        # if len(disease) > 0:
        #     for dis in disease:
        #         cursor.execute("SELECT * FROM ")
    
    # st.markdown("####")
    # st.markdown("####")
    open("filtered_tb_drugs", "w").write("\n".join(sorted(list(set(amrdrugs).difference(set(notpresdrug))))))
    # cursor.execute("SELECT `Drug for TB` FROM `data_anti-tb_drugs_sideeffects` ")
    # option2 = st.multiselect()
    
    # cursor.execute("SELECT * FROM `data_anti-tb_drugs_sideeffects`")
    # data = cursor.fetchall()
    # print(data)
    
    
    # if 'filtered_tb_drugs' not in st.session_state.keys():
    #     # filtered_tb_drugs = ['IND','USA','BRA','MEX','ARG']
    #     # st.write(filtered_tb_drugs)
    #     filtered_tb_drugs = open("filtered_tb_drugs").readlines()
    #     # print(filtered_tb_drugs)
    #     # filtered_tb_drugs = ['4-Aminosalicylic acid\n', 'Amikacin\n', 'Amoxicillin-clavulanate\n', 'Bedaquiline\n', 'Capreomycin\n', 'Ciprofloxacin\n', 'Clarithromycin\n', 'Clavulanic acid\n', 'Clofazimine\n', 'Cycloserine\n', 'Delamanid\n', 'Enviomycin\n', 'Ethambutol\n', 'Ethionamide\n', 'Fluoroquinolones\n', 'Gatifloxacin\n', 'Imipenem\n', 'Isoniazid\n', 'Kanamycin\n', 'Levofloxacin\n', 'Linezolid\n', 'Meropenem\n', 'Morinamide\n', 'Moxifloxacin\n', 'Ofloxacin\n', 'P-aminosalicylic acid\n', 'Pretomanid\n', 'Protionamide\n', 'Pyrazinamide\n', 'Rifabutin\n', 'Rifamate\n', 'Rifampicin\n', 'Rifampin\n', 'Rifapentine\n', 'Streptomycin\n', 'Terizidone\n', 'Thioacetazone\n', 'Viomycin']
    #     st.session_state['filtered_tb_drugs'] = filtered_tb_drugs
    # else:
    #     filtered_tb_drugs = st.session_state['filtered_tb_drugs']
    import math as mt
    totSD__ = []
    filtered_tb_drugs = "".join(open("filtered_tb_drugs").readlines()).split("\n")
    totalSelectedDrugs = []
    if len(filtered_tb_drugs) > 1:    
        df = pd.read_csv("se.csv")
        def checkbox_container(data):
            st.write("##### ***Suggested Drugs for TB***")
            cols = st.columns(10)
            if cols[-1].button('Select All'):
                for i in data:
                    st.session_state['dynamic_checkbox_' + i] = True
                st.experimental_rerun()
            if cols[-2].button('UnSelect All'):
                for i in data:
                    st.session_state['dynamic_checkbox_' + i] = False
                st.experimental_rerun()
            makeColumn = mt.ceil(len(filtered_tb_drugs)/10)
            cols2 = st.columns(makeColumn)
            dataCount = 1
            colCnt = 0
            for i in data:
                if dataCount % 10 ==0:colCnt+=1
                with cols2[colCnt]:
                    st.checkbox(i, key='dynamic_checkbox_' + i)
                dataCount+=1
    
        def get_selected_checkboxes():
            return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]
        st.markdown("####")
        st.markdown("----")
        checkbox_container(filtered_tb_drugs)
        # st.write('You selected:')
        selectedTBDrug = [x for x in get_selected_checkboxes() if x[0] != '_']
        if len(selectedTBDrug) > 0:
            st.markdown("####") 
            st.write(f"###### Selected TB drug(s) [{len(selectedTBDrug)}]: {', '.join(selectedTBDrug)}")
        st.markdown("----")
        def amc_checkbox_container(data_, amcD):
            st.write(f"###### ***{amcD}***")
            # cols_amc = st.columns(10)
            # if cols[-1].button('Select All'):
            #     for i in data:
            #         st.session_state['dynamic_checkbox_' + i] = True
            #     st.experimental_rerun()
            # if cols_amc[-1].button('Un Select All'):
            #     for i in data_:
            #         st.session_state['dynamic_checkbox_' + i] = False
            #     st.experimental_rerun()
            # makeColumn = mt.ceil(len(filtered_tb_drugs)/10)
            # cols2 = st.columns(makeColumn)
            # dataCount = 1
            # colCnt = 0
            for i_ in data_:
                # if dataCount % 10 ==0:colCnt+=1
                # with cols2[colCnt]:
                st.checkbox(i_, key='dynamic_checkbox__' + i_)
                # dataCount+=1
    
        def amc_get_selected_checkboxes():
            return [i_.replace('dynamic_checkbox__','') for i_ in st.session_state.keys() if i_.startswith('dynamic_checkbox__') and st.session_state[i_]]
        totalSelectedDrugs = []
        if len(option5) > 0:
            st.markdown("####")
            st.markdown("----")
            st.write("##### ***Available Drugs for AMCs***")
            amcList = ["Diabetes", "HIV/AIDS", "Thyroid", "Asthma", "Rheumatoid arthritis"]
            # filteredAMC = []
            cols3 = st.columns(5)
            cols3Indx = 0
            col6 = st.columns(10)
            # if col6[-1].button('UnSelect All'):
            #     for i in selectedAMCDrug:
            #         st.session_state['dynamic_checkbox__' + i] = False
            #     st.experimental_rerun()
            selAMCData = []
            for amcDisease in option5:
                # filteredAMC.append(amcDisease)
                if amcDisease in amcList:
                    with cols3[cols3Indx]:
                        # st.write(amcDisease)
                        amc_checkbox_container(sorted(list(set(df[df['disease'] == amcDisease]['drug']))), amcDisease)
                        selAMCData += list(set(df[df['disease'] == amcDisease]['drug']))
                cols3Indx+=1
            selectedAMCDrug = amc_get_selected_checkboxes()
            if len(selectedAMCDrug) > 0:
                st.write(f"###### Selected AMC drug(s) [{len([myx for myx in selectedAMCDrug if myx in selAMCData])}]: {', '.join([myx for myx in selectedAMCDrug if myx in selAMCData])}")
            st.markdown("----")
            totalSelectedDrugs = selectedTBDrug+selectedAMCDrug
        if len(option5) == 0:
            totalSelectedDrugs = selectedTBDrug
        # st.write(len(totalSelectedDrugs))
            
        st.markdown("####")
        # st.markdown("####")
        # st.markdown("####")
        st.markdown("----")
        selDF = []
        st.write(f"##### ***Mono Drug Side Effect Visualizer***")
        if len(totalSelectedDrugs) == 0:st.warning("Select at least 1 drug (TB/AMC) to visualize mono drug side effect network")
        if len(totalSelectedDrugs) > 0:
            if st.checkbox("Enable Visualizer & Side Effect Informations"):
                mseDF = []
                for selectedDrug in totalSelectedDrugs:
                    mseDF.append(df[df['drug']==selectedDrug])
                if len(mseDF) > 0:
                    selectedDrugDF = pd.concat(mseDF, ignore_index=True)
                    # st.write(selectedDrugDF)
                    selDF = selectedDrugDF
                    selectedDrugDF = selectedDrugDF.drop(['disease'], axis=1)
                    selectedDrugDF['val'] = 1
                    selectedDrugDF = selectedDrugDF.groupby(["drug", "se"], sort=False, as_index=False).sum()
                    G = nx.from_pandas_edgelist(selectedDrugDF,
                                               source="drug",
                                                target="se",
                                                edge_attr="val",
                                                create_using=nx.Graph()
                                               )
                    net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                    node_degree = dict(G.degree)
                    nx.set_node_attributes(G, node_degree, 'size')
                    partition = cl.best_partition(G)
                    nx.set_node_attributes(G, partition, 'group')
                    net.from_nx(G)
                    net.save_graph("mdse.html")
                    with open("mdse.html",'r') as f: 
                        html_data = f.read()
                    agree = st.checkbox('Enable Network Filters & Selection Menu')
                    if agree:
                        net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                        node_degree = dict(G.degree)
                        nx.set_node_attributes(G, node_degree, 'size')
                        partition = cl.best_partition(G)
                        nx.set_node_attributes(G, partition, 'group')
                        net.from_nx(G)
                        net.save_graph("mdse.html")
                        with open("mdse.html",'r') as f: 
                            html_data = f.read()
                    st.components.v1.html(html_data,height=800)
            st.markdown("----")
            st.markdown("####")
            mdInfoCols = st.columns([2,1])
            ddata = []
            mymseDF = []
            for selectedDrug in totalSelectedDrugs:
                mymseDF.append(df[df['drug']==selectedDrug])
                ddata.append({
                    "Disease": list(set(df[df['drug']==selectedDrug]['disease']))[0],
                    "Drug": selectedDrug,
                    "Total SE": len(df[df['drug']==selectedDrug])
                }) 
            peptide_Drug = ['Dulaglutide', 'Omalizumab', 'Mepolizumab', 'Reslizumab', 'Benralizumab', 'Etanercept', 'Adalimumab']
            filteredDrug, peptideDrug = [], []
            # st.write(totalSelectedDrugs)
            for myDrug in totalSelectedDrugs:
                if myDrug not in peptide_Drug: filteredDrug.append(myDrug)
                else: peptideDrug.append(myDrug)
            totalSelectedDrugs = filteredDrug
            # st.write(totalSelectedDrugs)
            # st.write(peptideDrug)       
            with mdInfoCols[0]:
                st.markdown("----")
                st.write(f"##### ***Mono Drug Side Effects***")
                pd.concat(mymseDF).to_sql(f'mse_data_{userID}', con=engine, index=False, if_exists='replace')
                st.dataframe(filterDF.filter_dataframe(pd.read_sql(f'SELECT * FROM `mse_data_{userID}`', con=engine).rename(columns={"disease":"Disease", "drug": "Drug", "se":"Side Effects"})), width=1000000, height=250)
                st.markdown("----")
            with mdInfoCols[1]:
                st.markdown("----")
                st.write(f"##### ***Drug Info***")
                st.dataframe(filterDF.filter_dataframe2(pd.DataFrame(ddata), ), width=1000000, height=250)
                st.markdown("----")
            # st.write(totalSelectedDrugs)
            allDrugNameStrucSMILES = {}
            allDrugNameStrucInchi = {}
            for drugName, Struc_ in zip(pd.read_csv("all_drugs_name_cid_struc_smiles.csv")['drug'], pd.read_csv("all_drugs_name_cid_struc_smiles.csv")['struc']):
                allDrugNameStrucSMILES.update({drugName : Struc_})
            for drugName, Struc_ in zip(pd.read_csv("all_drugs_name_cid_struc_inchi.csv")['drug'], pd.read_csv("all_drugs_name_cid_struc_inchi.csv")['struc']):
                allDrugNameStrucInchi.update({drugName : Struc_})
            # st.write(allDrugNameStrucSMILES)
            smiles, inchi = [], []
            for drg_ in totalSelectedDrugs:
                smiles.append(allDrugNameStrucSMILES[drg_])
            for drg__ in totalSelectedDrugs:
                inchi.append(allDrugNameStrucInchi[drg__])
            # st.write(smiles, inchi)
            unique_combinations = []
            for r in range(1, len(totalSelectedDrugs) + 1):
                unique_combinations.extend(combinations(totalSelectedDrugs, r))
            ucCount = 0
            for uComb in unique_combinations:
                if len(uComb) == 2: ucCount+=1
    
    
            predSe = []
            ddCombination = set()
            # allow_display = 0
            if len(totalSelectedDrugs) >= 2:
                if st.button("Predict Drug-Drug Side Effect"):
                    # allow_display += 1
                    myPeptideDrug = ", ".join(peptideDrug)
                    if len(peptideDrug) > 0: st.write('<span style="color: tomato;">'+f"**Important Note: For {myPeptideDrug} drug(s), no discrete structure found on PubChem. Hence, those drug(s) are not considered for making the drug pair(s).**"+'</span>', unsafe_allow_html=True)
                    myC_ = 1
                    with st.spinner('Your query submitted successfully. Please wait...'):
                        for sm_, in_ in zip(range(len(smiles)-1), range(len(inchi)-1)):
                            for sm__, in__ in zip(range(sm_+1,len(smiles)), range(in_+1,len(inchi))):
                                # st.write(f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}")
                                ddCombination.add(f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}")                    
                                os.chdir(rf'{os.getcwd()}')
                                def calculate_descriptors(smiles):
                                    mol = Chem.MolFromSmiles(smiles)
                                    if mol is None:
                                        return "Invalid SMILES"
                                    descriptor_values = [descriptor(mol) for name, descriptor in Descriptors._descList]
                                    logp = Crippen.MolLogP(mol)
                                    des_ = descriptor_values + [logp]
                                    return [0 if np.isnan(x) else x for x in des_]
                                def inchi_calculate_descriptors(smiles):
                                    mol = Chem.MolFromInchi(smiles)
                                    if mol is None:
                                        return "Invalid SMILES"
                                    descriptor_values = [descriptor(mol) for name, descriptor in Descriptors._descList]
                                    logp = Crippen.MolLogP(mol)
                                    des_ = descriptor_values + [logp]
                                    return [0 if np.isnan(x) else x for x in des_]
                                d1_d2_descriptor_names = ["d1_d2_abs_diff_"+desc[0] for desc in Descriptors._descList] + ['d1_d2_abs_diff_LogP']
                                uniqueSideEffects = "".join(open("uniqueSideEffects").readlines()).split("\n")
                                mapppingSE = {}
                                c = 0
                                for sideEffect in uniqueSideEffects:
                                    mapppingSE.update({sideEffect: c})
                                    c+=1
                                try:
                                # st.write(sm_)
                                # st.write(smiles[sm_])
                                # st.write(inchi_calculate_descriptors(smiles[sm_]))
                                # st.write(sm__)
                                # st.write(smiles[sm__])  
                                # st.write(inchi_calculate_descriptors(smiles[sm__]))
                                    s1_s2_abs_diff = np.round(np.abs(np.subtract(np.abs(calculate_descriptors(smiles[sm_])), np.abs(calculate_descriptors(smiles[sm__])))), decimals=6)                            
                                except:         
                                #     st.write(inchi_calculate_descriptors(inchi[in_]))  
                                #     st.write(inchi_calculate_descriptors(inchi[in__]))     
                                    s1_s2_abs_diff = np.round(np.abs(np.subtract(np.abs(inchi_calculate_descriptors(inchi[in_])), np.abs(inchi_calculate_descriptors(inchi[in__])))), decimals=6)            
                                if len(s1_s2_abs_diff) > 0:
                                    col_header = d1_d2_descriptor_names+uniqueSideEffects
                                    x = csr_matrix((0, len(col_header)-1))
                                    c = 0
                                    for lable in range(len(mapppingSE)):
                                        seMat = [0] * len(uniqueSideEffects)
                                        seMat[lable] = 1
                                        merged_array = np.hstack((s1_s2_abs_diff, np.array(seMat[:-1])))
                                        new_row = csr_matrix(merged_array)
                                        x = vstack([x.astype(float), new_row])
                                        c+=1
                                    model = joblib.load('ppmodel.joblib')
                                    model_out = model.predict_proba(x)
                                    mapppingSE = {}
                                    c = 0
                                    for sideEffect in uniqueSideEffects:
                                        mapppingSE.update({c : sideEffect})
                                        c+=1
                                    c = 0
                                    outScore = {}
                                    for i in model_out:
                                        outScore.update({mapppingSE[c]: list(i)[c]})
                                        c+=1
                                    col_header = ["d1_d2_abs_diff_"+desc[0] for desc in Descriptors._descList] + ['d1_d2_abs_diff_LogP']
                                    inpX = csr_matrix((0, len(col_header)))
                                    inpX = vstack([inpX.astype(float), s1_s2_abs_diff])
                                    progress_text = f"Prediction in progress (Drug Combination {myC_}/{ucCount}-> [{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}]). Please wait..."
                                    myC_+=1
                                    my_bar = st.progress(0, text=progress_text)
                                    k = 0
                                    for i, j in zip(range(len(mapppingSE)), outScore.keys()):
                                        os.chdir(rf'{os.getcwd()}'+'/models')
                                        model = joblib.load(f'model_{i}.joblib')
                                        os.chdir(rf'{os.getcwd()}'.replace('/models', ""))
                                        specificModelPredict = model.predict(inpX)[0]
                                        if i%131 == 0:
                                            my_bar.progress(k+9, text=progress_text)
                                            k+=9
                                        if specificModelPredict != -1:
                                            predSe.append({
                                                "Drug Combination" : f"{totalSelectedDrugs[sm_]} & {totalSelectedDrugs[sm__]}",
                                                "Side Effect with Probability": j+" ["+str(outScore[mapppingSE[i]])+"]" 
                                            })
                                    my_bar.empty()
                    # st.write(pd.DataFrame(predSe), unsafe_allow_html=True)
                    pd.DataFrame(predSe).to_sql(f'predicted_dd_se_{userID}', con=engine, index=False, if_exists='replace')
                    ddCombSEPredDF = pd.read_sql(f'SELECT * FROM `predicted_dd_se_{userID}`', con=engine)
                    notInSE = 'Infection Upper Respiratory|CMV infection|Brachial plexus injury|Motion sickness|Esophageal spasm|Bladder atony|Nausea|Eating disorder|Pancreatic cancer|Breakthrough bleeding|Thyroid cyst|Leriche syndrome|Eye injury|Candida Infection|EBV infection|Periodontal disease|Cholecystitis acute|Bad breath|Dermatophytosis|Transfusion reaction|Spinal cord injury|Bladder diverticulum|Sunburn|Albuminuria|Ekbom Syndrome|Dandruff|Abuse|Failure to thrive|Infectious mononucleosis|Floaters|Sleep apnea|Trichomoniasis|Bundle branch block right|HIV disease|Renal cancer|Thyroid cancer|Infection|Tremor|Bone marrow transplant|Encephalitis viral|Sick sinus syndrome|Acquired immune deficiency syndrome|Ear infection|Proteinuria|Viral rash NOS|Renal cyst|Acne rosacea|Head injury|Viral pneumonia|Atypical mycobacterial infection|Nasal polyp|Renal agenesis|Bleeding|Peyronies Disease|Anemia aplastic|Diaphragmatic hernia|Faecal incontinence|Bruxism|Animal bite|Pneumocystis carinii infection|Abnormal Laboratory Findings|Faecal impaction|Tinea Capitis|Breast cyst|Sinus headache|Confusion|Carcinoma of Prostate|Tinea cruris|Pyuria|Mitral valve disease NOS|Gallbladder cancer|Balance disorder|Duodenal ulcer perforation|Arthritis bacterial|Anal fistula|Onychomycosis|Mast cell disease|Drowsiness|Coccidioidomycosis|Bulimia|Alcohol consumption|Supernumerary nipple|Breast cancer|Soft tissue infection|Vitamin B 12 deficiency|Cystitis Interstitial|Arthritis infective|Oily Skin|Femoral neck fracture|Bacterial infection|Bacterial endocarditis|Abnormal ECG|Kidney transplant|Difficulty in walking|Salivary gland enlargement|Acute kidney failure|External ear infection|Basal cell carcinoma|Choriocarcinoma|Lyme Disease|Abnormal cervical smear|Lung neoplasm malignant|Hepatitis B|Alcohol abuse|Vitamin D Deficiency|Pneumocystis carinii pneumonia|Tuberculin test positive|Tinea|Rib fracture|Acid reflux|Acne|Post thrombotic syndrome|Night sweat|Mixed connective tissue disease|Ejaculation Premature|Chicken pox|Diarrhea infectious|Xerosis|Decreased lacrimation|Right heart failure|Traumatic arthropathy|ADVERSE DRUG EFFECT|CYSTO|Streptococcal infection|Cystic Fibrosis|Cholecystectomies|Gastroenteritis viral|Parasitic infection intestinal|Cholecystitis chronic|Typhoid|Nightmare|Soft tissue injuries|Chest infection|Polio|Heart attack|Ovarian cancer|Rubella|Ulcer|Abdominal hernia|Skin abrasion|Kidney failure|Fractured pelvis NOS|Adenocarcinoma|Pilonidal cyst|Umbilical hernia|Cryptococcosis|Nocturia|Hepatitis B surface antigen positive|Eyelid diseases|Aseptic necrosis bone|Hepatorenal syndrome|Intervertebral Disc Herniation|Brain neoplasm|Esophageal rupture|Hypercalcinuria|Adrenal carcinoma|Deglutition disorder|Swollen scrotum|Whiplash Injury|Hernia Inguinal|Wrist fracture|Abnormal mammogram|Carcinoid syndrome|Abnormal vision|Heat stroke|Sinus tachycardia|Tension headache|Psychosomatic disease|Viral Pharyngitis|Obesity|Synovial cyst|Dacrocystitis|Drug addiction|Abnormal LFTs|Carcinoma of the colon|Peripheral nerve injury|Tooth Impacted|Bacterial vaginitis|Gonorrhea|Dry skin|Infection Viral|Duodenal ulcer haemorrhage|Cryptorchidism|Rotator cuff syndrome|Fracture nonunion|Tetanus|Pancreatic pseudocyst|Sleep walking|Coma|Bladder cancer|Ovarian Cyst|Arteriosclerotic heart disease|Abnormal movements|Nephrotic syndrome|Phobia|Acidosis|Arthritis rheumatoid|Wound dehiscence|Spinal Compression Fracture|Anthrax|Bundle branch block left|Bone Fracture Spontaneous|Superior vena cava syndrome|Drug withdrawal|Tinea pedis|Nodule Skin|Vitamin B deficiency|Body tinea|Vaginal dysplasia|Dehydration|Caesarean Section|Nasal septal perforation|Black stools|Aspergillosis|Pneumonia Klebsiella|Respiratory failure|Mycobacterium tuberculosis infection|Head ache|Hepatic failure|Acute brain syndrome|Tooth disease|Diphtheria|Arthropathy|Septic abortion|Bone marrow failure|Psychosexual disorder|Dizziness|Endometrial cancer|Anaemia hypochromic|Myoglobinuria|Thyroid neoplasia|Abscess|Bacterial pneumonia|Breast Lump|Septic shock|Conjunctivitis viral|Food poisoning|Cardiac failure|Mycosis fungoides|Hepatitis toxic|Renal mass|Acromegaly|Adenoid hypertrophy|Cutaneous mycosis|Legionella|Fungal disease|Humerus fracture|Salivary Gland Calculus|Flu|Thyroidectomy|Flashing lights|Femur fracture|Skin Striae|Infection Urinary Tract|Uterine infection|Tendon injury|Bulging|Abdominal pain upper|Flashbacks|Hepatitis C antibody positive|Cervical vertebral fracture|Adjustment disorder|Injury of neck|Spinal fracture|Eosinophilic pneumonia acute|Renal colic|Hip fracture|Scar|Hepatitis A|Agitated|Urogenital abnormalities|Polyuria|Bacterial conjunctivitis|Transurethral resection of the prostate|Hernia hiatal|Anal fissure|Incisional hernia|Defaecation urgency|Cryptosporidiosis|Neumonia|Hepatitis C|Urosepsis|Sinus arrest|Pneumonia staphylococcal|Back injury|Cutaneous candidiasis|Thyroid adenoma|Hair disease|Adenomyosis|Sjogrens syndrome|Narcolepsy|Anal pruritus|Heat rash|Eye infection|Hallucination|Cardiac disease|Spider angioma|Esophageal stenosis|Dermoid cyst|Vaginal prolapse|Vaginal discharge|Burns Second Degree|Sexually transmitted diseases|Pelvic infection|Esophageal cancer|Cystic acne|Tinea versicolor|Bone fracture|Abnormal EEG|Sinus bradycardia|Ankle fracture|Meningitis Viral|Gastric Cancer|Night cramps|Carcinoma of the cervix|Brain concussion|Nodule|Feeling unwell|Thyroid disease|Flatulence|Glucosuria'
                    ddCombSEPredDF = ddCombSEPredDF[~ddCombSEPredDF['Side Effect with Probability'].str.contains(notInSE, case=False)]
                    noSideEffect = []
                    totSideEffectDF = []
                    for i_i in ddCombination:
                        if len(ddCombSEPredDF[ddCombSEPredDF['Drug Combination']==i_i]) == 0:
                            noSideEffect.append({
                                "Drug Combination": i_i,
                                "Side Effect with Probability": "No Side Effect [1.0]"
                            })
                        totSideEffectDF.append({
                            "Drug Combination": i_i,
                            "Total No. of Side Effect": len(ddCombSEPredDF[ddCombSEPredDF['Drug Combination']==i_i])
                        })
                    xx = pd.DataFrame(noSideEffect)
                    finalDFDB = pd.concat([ddCombSEPredDF, xx], ignore_index=True)
                    totSideEffectDFDB = pd.DataFrame(totSideEffectDF).sort_index(ascending=False)
                    finalDFDB.to_sql(f'final_dd_se_{userID}', con=engine, index=False, if_exists='replace')
                    totSideEffectDFDB.to_sql(f'tot_side_effect_df_{userID}', con=engine, index=False, if_exists='replace')    
                else: pass
            else:
                if len(peptideDrug) > 0 and len(totalSelectedDrugs) == 1:
                    jpd = ", ".join(peptideDrug)
                    st.warning(f"Atleast 2 non-peptide drugs are require to making the drug pair(s). {jpd} drug(s) can't be consider, since this all are peptide based drugs!")
                if len(totalSelectedDrugs) == 1 and len(peptideDrug) == 0:
                    st.warning(f"Atleast 2 drugs are require to making the drug pair(s).")
    
    filterDict = {
                'Cardiac': ['Cardiac', 'heart', 'pericard', 'carotid', 'arterial', 'atri', 'ventri', 'vascul'],
                'Renal': ['Renal', 'Kidney'],
                'Liver': ['Hepato', 'Hepatic', 'liver'],
                'Cervical': ['Cervical', 'cervix'],
                'Breast': ['Breast'],
                'Respiratory': ['Respiratory', 'pulmonary', 'lung', 'Pneumo'],
                'Brain': ['Brain', 'Cerebral', 'Cerebellar'],
                'Eye': ['Eye', 'Cornea', 'Retin'],
                'Digestive': ['Gastr', 'Intestin', 'Duoden', 'bowel'],
                'Skin': ['Skin', 'derma'],
                'Ortho': ['Bone', 'joint', 'muscle', 'musculoskeletal', 'muscular']
            }
    # st.write(allow_display)
    if len(totalSelectedDrugs) >= 2:
        if st.checkbox("Display result", help="Please enable **after** the prediction"):
            # st.write(totSD__)
            query_finalDF = f'SELECT * FROM `final_dd_se_{userID}`'
            finalDF = pd.read_sql(query_finalDF, con=engine)
            finalDF2 = finalDF.copy()
            query_totSideEffectDF = f'SELECT * FROM `tot_side_effect_df_{userID}`'
            df_from_db_totSideEffectDF = pd.read_sql(query_totSideEffectDF, con=engine)
            if len(finalDF) > 0:
                st.markdown("####")
                st.markdown("----")
                st.markdown("##### ***Drug Drug Side Effect Visualizer***")
                if st.checkbox("Enable Drug Drug Side Effect Visualizer (Not Always Recomended)", help="It is recomended that don't enable this option in case of large number of predicted side effects. It will takes a bit longer to load the network graphics/the browser may unresponsive at that moment."):
                    finalDF_ = finalDF.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                    finalDF_['val'] = 1
                    G = nx.from_pandas_edgelist(finalDF_,
                                               source="Drug Combination",
                                                target="Side Effect with Probability",
                                                edge_attr="val",
                                                create_using=nx.Graph()
                                               )
                    net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                    node_degree = dict(G.degree)
                    nx.set_node_attributes(G, node_degree, 'size')
                    partition = cl.best_partition(G)
                    nx.set_node_attributes(G, partition, 'group')
                    net.from_nx(G)
                    net.save_graph("ddse.html")
                    with open("ddse.html",'r') as f: 
                        html_data = f.read()
                    agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                    if agree_:
                        net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                        node_degree = dict(G.degree)
                        nx.set_node_attributes(G, node_degree, 'size')
                        partition = cl.best_partition(G)
                        nx.set_node_attributes(G, partition, 'group')
                        net.from_nx(G)
                        net.save_graph("ddse.html")
                        with open("ddse.html",'r') as f: 
                            html_data = f.read()
                    st.components.v1.html(html_data,height=800)
                st.markdown("----")
                st.markdown("####")
                ddCols = st.columns([2,1])
                getDF = ''
                with ddCols[0]: 
                    st.markdown("----")
                    st.markdown("##### ***Poly Drug Side Effects [Predicted]***")
                    finalDF[['Side Effect', 'Probability']] = finalDF['Side Effect with Probability'].str.split('[', expand=True)
                    finalDF['Probability'] = finalDF['Probability'].str.rstrip(']')
                    finalDF = finalDF.drop('Side Effect with Probability', axis=1)
                    getDF = finalDF
                    st.dataframe(filterDF.filter_dataframe3(finalDF), width=1000000, height=250)
                    st.markdown("----") 
                with ddCols[1]: 
                    st.markdown("----")
                    st.markdown("##### ***Drug Combination Info***")
                    st.dataframe(filterDF.filter_dataframe4(df_from_db_totSideEffectDF), width=1000000, height=250)
                    st.markdown("----")
                st.markdown("----")
                st.markdown("##### ***Analyze Poly Drug Side Effects [Predicted] More Specifically***")
                if st.checkbox("Enable"):        
                    option_radio = st.radio(
                        "**Select an Option**",
                        ['None','Cardiac', 'Renal', 'Liver', 'Cervical', 'Breast', 'Respiratory', 'Brain', 'Eye', 'Digestive', 'Skin', 'Ortho', 'Other'],
                        # index=None
                        horizontal=True
                    )
                    # st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    if option_radio != 'None':
                        if option_radio != 'Other':
                            filterCols_1 = st.columns([2,1])
                            with filterCols_1[0]:
                                st.markdown('<div style="background-color:Bisque;font-size:50px;text-align:center;"></div>', unsafe_allow_html=True)
                                mydf1 = getDF[getDF['Side Effect'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                st.dataframe(filterDF.filter_dataframe5(mydf1), width=1000000, height=250)
                            with filterCols_1[1]:
                                # st.write(getDF.columns)
                                st.markdown("#####")
                                mydf1 = getDF[getDF['Side Effect'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                comb = mydf1.drop(['Side Effect', 'Probability'], axis=1)
                                # st.write(comb)
                                value_counts_df = comb.value_counts().reset_index()
                                # st.write(comb['Drug Combination'].str.contains("|".join(filterDict['Cardiac']), case=False))
                                value_counts_df.columns = ['Drug Combination', 'Total No. of Side Effect']
                                st.dataframe(filterDF.filter_dataframe6(value_counts_df), width=1000000, height=250)
                            # st.write(finalDF2)
                            st.markdown("###### ***Drug Drug Side Effect Visualizer [SPECIFIC]***")
                            if st.checkbox("Enable (Not Always Recomended)", help="It is recomended that don't enable this option in case of large number of predicted side effects. It will takes a bit longer to load the network graphics/the browser may unresponsive at that moment."):
                                finalDF2_ = finalDF2[finalDF2['Side Effect with Probability'].str.contains("|".join(filterDict[option_radio]), case=False)]
                                finalDF_specific = finalDF2_.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                                finalDF_specific['val'] = 1
                                G = nx.from_pandas_edgelist(finalDF_specific,
                                                           source="Drug Combination",
                                                            target="Side Effect with Probability",
                                                            edge_attr="val",
                                                            create_using=nx.Graph()
                                                           )
                                net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                                node_degree = dict(G.degree)
                                nx.set_node_attributes(G, node_degree, 'size')
                                partition = cl.best_partition(G)
                                nx.set_node_attributes(G, partition, 'group')
                                net.from_nx(G)
                                net.save_graph("ddse.html")
                                with open("ddse.html",'r') as f: 
                                    html_data = f.read()
                                agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                                if agree_:
                                    net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                                    node_degree = dict(G.degree)
                                    nx.set_node_attributes(G, node_degree, 'size')
                                    partition = cl.best_partition(G)
                                    nx.set_node_attributes(G, partition, 'group')
                                    net.from_nx(G)
                                    net.save_graph("ddse_specific.html")
                                    with open("ddse_specific.html",'r') as f: 
                                        html_data = f.read()
                                st.components.v1.html(html_data,height=800)
                        else:
                            # allKW = list(filterDict.values())
                            # st.warning("|".join(list(chain(*allKW))))
                            allKW = "Cardiac|heart|pericard|carotid|arterial|atri|ventri|vascul|Renal|Kidney|Hepato|Hepatic|liver|Cervical|cervix|Breast|Respiratory|pulmonary|lung|Pneumo|Brain|Cerebral|Cerebellar|Eye|Cornea|Retin|Gastr|Intestin|Duoden|bowel|Skin|derma|Bone|joint|muscle|musculoskeletal|muscular"
                            filterCols_1 = st.columns([2,1])
                            with filterCols_1[0]:
                                mydf1 = getDF[~getDF['Side Effect'].str.contains(allKW, case=False)]
                                st.dataframe(filterDF.filter_dataframe5(mydf1), width=1000000, height=250)
                            with filterCols_1[1]:
                                # st.write(getDF.columns)
                                mydf1 = getDF[~getDF['Side Effect'].str.contains(allKW, case=False)]
                                comb = mydf1.drop(['Side Effect', 'Probability'], axis=1)
                                # st.write(comb)
                                value_counts_df = comb.value_counts().reset_index()
                                # st.write(comb['Drug Combination'].str.contains("|".join(filterDict['Cardiac']), case=False))
                                value_counts_df.columns = ['Drug Combination', 'Total No. of Side Effect']
                                st.dataframe(filterDF.filter_dataframe6(value_counts_df), width=1000000, height=250)
                            # st.write(finalDF2)
                            st.markdown("###### ***Drug Drug Side Effect Visualizer [SPECIFIC]***")
                            if st.checkbox("Enable (Not Always Recomended)"):
                                finalDF2_ = finalDF2[~finalDF2['Side Effect with Probability'].str.contains(allKW, case=False)]
                                finalDF_specific = finalDF2_.groupby(["Drug Combination", "Side Effect with Probability"], sort=False, as_index=False).sum()
                                finalDF_specific['val'] = 1
                                G = nx.from_pandas_edgelist(finalDF_specific,
                                                           source="Drug Combination",
                                                            target="Side Effect with Probability",
                                                            edge_attr="val",
                                                            create_using=nx.Graph()
                                                           )
                                net = Network(notebook=True, width="100%", height="800px", bgcolor='#222222', font_color='white', cdn_resources='remote')
                                node_degree = dict(G.degree)
                                nx.set_node_attributes(G, node_degree, 'size')
                                partition = cl.best_partition(G)
                                nx.set_node_attributes(G, partition, 'group')
                                net.from_nx(G)
                                net.save_graph("ddse.html")
                                with open("ddse.html",'r') as f: 
                                    html_data = f.read()
                                agree_ = st.checkbox('Enable Network Filters & Selection Menu ')
                                if agree_:
                                    net = Network(notebook=True, width="100%", height="650px", bgcolor='#222222', font_color='white', select_menu=True, filter_menu=True, cdn_resources='remote')
                                    node_degree = dict(G.degree)
                                    nx.set_node_attributes(G, node_degree, 'size')
                                    partition = cl.best_partition(G)
                                    nx.set_node_attributes(G, partition, 'group')
                                    net.from_nx(G)
                                    net.save_graph("ddse_specific.html")
                                    with open("ddse_specific.html",'r') as f: 
                                        html_data = f.read()
                                st.components.v1.html(html_data,height=800)
                    else: pass
                st.markdown("----")
