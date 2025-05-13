#cd C:\Users\anges\.anaconda
#python streamlit_tp.py
#streamlit run TEST.py


import streamlit as st
import numpy as np
import pandas as pd
st.image("https://cdn.futura-sciences.com/buildsv6/images/largeoriginal/c/3/d/c3d36fbae8_127078_ingenieurs-transverses-zinkevych-fotolia.jpg", use_container_width=True)


st.title("📁 Mon application Streamlit")
st.subheader("Try out the app")
st.text("this is a simple text element")

#2 Sidebar
#choix dans une liste deroulante (dans la sidebar )
graph_type = st.sidebar.selectbox("Choisissez un type de graphique :", ["Ligne", "Barres", "Aucun"])

st.write(f"Vous avez choisi le type de graphique :{graph_type}")

#3 Uploading a Cv
uploaded_file = st.file_uploader("Télechargez un fichier CSV", type=["csv"])
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.write("Voici un aperçu de votre fichier :")
    st.dataframe(df.head())

    #4 Affichage du graphique en fonction du type choisi
    if graph_type == "Ligne":
        st.line_chart(df)
    elif graph_type == "Barres":
        st.bar_chart(df)
    else:
        st.write("Aucun graphique sélectionné.")

#4 SLider
age = st.slider("Quel âge avez-vous ?", 0, 100, 25)
st.write(f"Vous avez {age} ans.")

# Checkbox
if st.checkbox("Afficher un tableau aleatoire"):
  st.write(pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C']))

st.write("Merci d'avoir utilisé le site internet de Samuel")

