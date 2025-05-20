#cd C:\Users\anges\.anaconda
#python streamlit_tp.py
#streamlit run TEST.py


import streamlit as st
import numpy as np
import pandas as pd


st.title("Mon application TP2")
st.subheader("TP2 EVALUATION ")

st.markdown(
    """
    <div style="position: relative; text-align: center; color: white;">
        <img src="https://cdn.futura-sciences.com/buildsv6/images/largeoriginal/c/3/d/c3d36fbae8_127078_ingenieurs-transverses-zinkevych-fotolia.jpg" style="width: 100%; height: auto; border-radius: 10px;" />
        <h1 style="position: absolute; top: 50%; left: 50%; 
                   transform: translate(-50%, -50%); 
                   background-color: rgba(0, 0, 0, 0.5); 
                   padding: 20px; border-radius: 10px;">
            Bienvenue sur mon application Streamlit 🚀
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

#Demander le nom de l'utilisateur et le saluer
nom = st.text("Quel est votre nom ?")
st.write(f"Bonjour{nom} .")

# Importation de fichier
st.title("Importation d'un fichier excel")
uploaded_file = st.file_uploader("Télechargez un fichier CSV", type=["csv"])



st.write("Merci d'avoir utilisé le site internet de Samuel")

