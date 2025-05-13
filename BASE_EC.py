#step 1: Import the libraries
import streamlit as st
import pandas as pd

#step 2: Set the title of the app
st.title('Page analyse Base E+C- empreinte carbone')

#Step 3: file uploader
uploaded_file = st.file_uploader("Importez le fichier Excel E+C- ", type=["csv"])
df_raw = pd.read_excel(uploaded_file, sheet_name='batiments', header_name="")
st.dataframe(df_raw.head(3))
