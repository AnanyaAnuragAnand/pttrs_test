import streamlit as st
def app_info():
    st.title("PTTRS App Information")
    st.write("""
        PTTRS (Personalized Tuberculosis Treatment Recommender System) is a precision-medicine based application for recommending personalized treatment to tuberculosis patients.
                
        ### Key Features
        - Feature 1: Help to study & visualize side effect(s) of mono drug & poly drug, by double ML model (for more specificity), for TB and associted medical conditions (AMCs).
        - Feature 2: Help to study and visualize side effect(s) organ-wise of human body.
        - Feature 3: Smart patient data management (only for Doctors and patients).
        
        ### Version
        Current version: 1.0.0 (Beta)
        
        ### Release Date
        05/02/2024
        
        This app is a part of BBLSERVER.
    """)