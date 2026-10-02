import streamlit as st
import time
import pandas as pd
import os

st.set_page_config(page_title='PDF AI Assistant', layout='wide')
st.title('PDF AI Assistant')
st.write("This application helps to deal with huge pdf files, using AI")

st.write('-------------------------------------------------------------')
uploaded_file = st.file_uploader('Choose a pdf file', type=["pdf"])

if uploaded_file is not None:
    st.write(f'Successfully uploaded a pdf file {uploaded_file}')
else:
    st.write('Pdf file not uploaded')

st.write('-------------------------------------------------------------')
if st.button('Start AI Assistant'):
    with st.spinner('AI Assistant is working right now...'):
        with open("main.py", "r", encoding="utf-8") as f:
            exec(f.read())

        st.success("✅ Sikeres elemzés! Az adatok frissültek.")
        time.sleep(2)
        st.rerun()

st.write('-------------------------------------------------------------')
excel_fajl = "pdf_excel.xlsx"

if os.path.exists(excel_fajl):
    st.write('Excel file already existing')
    adatok = pd.read_excel(excel_fajl)
    st.dataframe(adatok)
else:
    st.write('Excel file not existing')