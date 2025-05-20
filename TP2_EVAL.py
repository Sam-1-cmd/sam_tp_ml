#cd C:\Users\anges\.anaconda
#python streamlit_tp.py
#streamlit run TEST.py


import streamlit as st
import numpy as np
import pandas as pd


st.title("Mon application TP2")
st.subheader("Try out the app")
st.text("this is a simple text element")

#Demander le nom de l'utilisateur et le saluer
nom = st.text("Quel est votre nom ?")
st.write(f"Bonjour{nom} .")

ploaded_file = st.file_uploader("Télechargez un fichier CSV", type=["csv"])
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.write("Voici un aperçu de votre fichier :")
    st.dataframe(df.head())



st.write("Merci d'avoir utilisé le site internet de Samuel")

