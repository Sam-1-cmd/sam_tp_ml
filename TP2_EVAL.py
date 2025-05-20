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

# STEP 3 : Data loading
st.title("Step 3 - Importation de la base E+C-")
uploaded_file = st.file_uploader("Importez le fichier Excel E+C- (feuille 'batiments')", type=["xlsx"])
df_raw = pd.read_excel(uploaded_file, sheet_name='batiments', header=[0,1])

#dealing with multi-index
df_raw.columns = df_raw.columns.droplevel(0)
st.dataframe(df_raw.head(3))
st.subheader("Statistiques descriptives")
st.write(df_raw.describe())

# STEP 4 : Initial scatter plot
st.title("step 4 - Nuage de points")
st.write("Tous les bâtiments sont représentés dans le diagramme ci-dessous. ")
fig = px.scatter(df_raw, x=df_raw['id_batiment'], y=df_raw['eges'])
st.plotly_chart(fig, use_container_width=True)

# STEP 4b : BASIC data cleaning
st.subheader("step 4b - Nettoyage de base des données")
df_raw = df_raw.drop((df_raw[df_raw["eges"]>2500]).index)
df_raw= df_raw.drop((df_raw[df_raw["eges"]<500]).index)
st.dataframe(df_raw)
fig = px.scatter(df_raw, x=df_raw['id_batiment'], y=df_raw['eges'])
st.plotly_chart(fig, use_container_width=True)

# STEP 5: Feature Extraction (Separating input features and target features in df_raw)
st.title("STEP 5: Feature Extraction")

# 5a. List input features
All_columns =  df_raw.columns
features_input_col = []
for n in range(len(All_columns)):
    col_name = All_columns[n]
    if ("eges" in col_name):
        break
    if "id" not in col_name:
        features_input_col.extend([col_name])
st.markdown("list des features which can be used as inputs")
st.write(features_input_col)

# 5b. List target features
features_target_col=[]
for n in range(len(All_columns)):
    col_name = All_columns[n]
    if ("eges" in col_name):
        features_target_col.extend([col_name])
st.markdown("")
st.markdown("list des features which can be used as target")
st.write(features_target_col)


# STEP 6: Numeric Correlation Analysis
st.title("STEP 6: Numeric Correlations")
st.markdown("features with high correlation (But do not included categorical")
df_features_in = pd.DataFrame(df_raw, columns=features_input_col)
st.write(df_features_in.corrwith(df_raw["eges"], numeric_only=True).sort_values(ascending=True)[:5])

st.markdown("features with low correlation (But not included categorical)")
st.write(df_features_in.corrwith(df_raw["eges"], numeric_only=True).sort_values(ascending=False)[:5])

# STEP 7: Categorical Correlation Analysis
st.title("STEP 7: Categorical Correlations")
#Generation dummies to be able to carry out correlation with categorical features
st.markdown('Creating dummies for categorical features')
df_d= pd.get_dummies(df_features_in)
st.dataframe(df_d.head(10))

st.markdown("features with correlation to HIGH eges:")
st.write(df_d.corrwith(df_raw["eges"]).sort_values(ascending=False)[:5])
st.markdown("features with correlation to LOW eges:")
st.write(df_d.corrwith(df_raw["eges"]).sort_values()[:5])

st.write("Merci d'avoir utilisé le site internet de Samuel")

