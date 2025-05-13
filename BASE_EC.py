## STEP 1 : Libraries and initialisation
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.compose import make_column_selector as selector
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import  Ridge
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import plotly.express as px


# STEP 2 : Streamlit configuration
st.set_page_config(page_title="ACV Bâtiments E+C-", layout="wide")
st.title("Analyse du Cycle de Vie – Base E+C-")
st.markdown("Ce tableau de bord interactif guide les étudiants à travers chaque étape du notebook original.")


# STEP 3 : Data loading
st.title("Step 3 - Importation de la base E+C-")
uploaded_file = st.file_uploader("Importez le fichier Excel E+C- (feuille 'batiments')", type=["xlsx"])
df_raw = pd.read_excel(uploaded_file, sheet_name='batiments', header=[0,1])

#dealing with multi-index
df_raw.columns = df_raw.columns.droplevel(0)
st.dataframe(df_raw.head(3))
st.subheader("Statistiques descriptives")
st.write(df_raw.describe())
