import streamlit as st
from PIL import Image
import pandas as pd
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os

# Configuration de la page
st.set_page_config(
    page_title="IGED - Innovation Groupe Étude Digitale",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Styles CSS ----
def load_css():
    st.markdown("""
    <style>
        /* Styles globaux */
        [data-testid="stAppViewContainer"] {
            background-color: #f8f9fa;
        }
        .main-title {
            color: #6e48aa;
            font-size: 2.8rem;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .testimonial {
            border-left: 4px solid #6e48aa;
            padding-left: 1rem;
        }
        .btn-primary {
            background: #6e48aa;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ---- Fonctions Partagées ----
def send_email(sender, password, receiver, subject, body, attachment=None):
    """Fonction générique pour envoyer des emails"""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
        msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

def display_testimonial(name, role, text, img_url):
    """Affiche un témoignage formaté"""
    with st.container():
        st.markdown(f"""
        <div class="card testimonial">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <img src="{img_url}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover;">
                <div>
                    <h4 style="margin: 0;">{name}</h4>
                    <p style="margin: 0; color: #666;">{role}</p>
                </div>
            </div>
            <p style="font-style: italic; margin: 0;">"{text}"</p>
        </div>
        """, unsafe_allow_html=True)

# ---- Header Commun ----
def display_header():
    """Affiche l'en-tête commun à toutes les pages"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%); 
                padding: 2rem; border-radius: 10px; color: white; 
                text-align: center; margin-bottom: 2rem;">
        <h1 class="main-title" style="color: white;">IGED</h1>
        <p class="subtitle" style="color: white; font-size: 1.2rem;">
        Innovation Groupe Étude Digitale
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---- Navigation ----
menu = {
    "Accueil": "🏠",
    "Nos Services": "🎯", 
    "Nos Professeurs": "👩‍🏫",
    "Tarifs": "💳",
    "Contact": "✉️",
    "Espace Élève": "📚",
    "Recrutement": "💼"
}

def show_navigation():
    """Affiche le menu de navigation dans la sidebar"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=IGED+Logo", width=150)
        st.markdown("## Navigation")
        
        # Crée des boutons de navigation stylisés
        for page, icon in menu.items():
            if st.button(f"{icon} {page}", use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
        
        st.markdown("---")
        st.markdown("📞 [07 45 50 24 52](tel:+2250745502452)")
        st.markdown("✉️ [contact@iged-ci.com](mailto:contact@iged-ci.com)")

# ---- Pages ----
def home_page():
    """Page d'accueil"""
    display_header()
    
    cols = st.columns([2, 1], gap="large")
    
    with cols[0]:
        st.markdown("""
        ## 📚 Votre réussite, notre priorité
        
        **IGED** combine expertise pédagogique et solutions digitales pour :
        - 🎯 **Programmes personnalisés** avec suivi algorithmique
        - 👨‍🏫 **+50 professeurs** certifiés (95% de satisfaction)
        - 📈 **92% de réussite** aux examens 2023
        - 💻 **Plateforme interactive** disponible 24h/24
        """)
        
        display_testimonial(
            "Amina K., 16 ans",
            "Élève en Terminale S",
            "Avec IGED, ma moyenne en maths est passée de 8 à 15 en 3 mois !",
            "https://randomuser.me/api/portraits/women/65.jpg"
        )
        
        st.video("https://youtu.be/5agcs8--Szo?si=4tg2qHFHuiRqvxrk")
    
    with cols[1]:
        with st.container():
            st.markdown("### ✉️ Demande de contact")
            with st.form(key='contact_form'):
                name = st.text_input("Nom complet*")
                niveau = st.selectbox("Niveau scolaire*", 
                                    ["Primaire", "Collège", "Lycée", "Supérieur"])
                phone = st.text_input("Téléphone*")
                submitted = st.form_submit_button("Être rappelé(e)", type="primary")
                
                if submitted:
                    if name and phone:
                        st.success(f"Merci {name.split()[0]}! Un conseiller vous contactera pour le {niveau}.")
                    else:
                        st.error("Veuillez remplir les champs obligatoires (*)")
        
        with st.expander("📍 Nos centres en Côte d'Ivoire", expanded=True):
            st.map(data=pd.DataFrame({
                'lat': [5.3167, 5.3541, 7.6906],
                'lon': [-4.0333, -4.0016, -5.0303],
                'name': ['IGED Yamoussoukro', 'IGED Abidjan', 'IGED Bouaké']
            }), zoom=6)

def services_page():
    """Page Nos Services"""
    display_header()
    st.markdown("## 🎯 Nos Solutions Pédagogiques")
    
    tabs = st.tabs(["Cours Particuliers", "Stages Intensifs", "Aide aux Devoirs", "Préparation Examens"])
    
    with tabs[0]:
        cols = st.columns([1, 2])
        with cols[0]:
            st.image("https://tewmoutew.com/img/photos/2021-10-02-201830_bde15679.jpg")
        with cols[1]:
            st.markdown("""
            ### Cours Particuliers à Domicile ou en Ligne
            - 🔄 **Suivi régulier** ou ⏱️ **ponctuel**  
            - 🌍 **Toutes matières**, 🎓 **tous niveaux**  
            - 🕒 **Créneaux flexibles** (matin/soir/week-end)  
            - 🔍 **Bilan pédagogique initial** gratuit  
            """)
    
    with tabs[1]:
        st.markdown("""
        ### Stages Intensifs pendant les Vacances
        - Stages de révision
        - Stages de remise à niveau
        - Préparation aux examens (Brevet, Bac, Concours)
        - En petits groupes ou individuels
        - 10h à 30h par semaine
        """)
    
    # ... (autres onglets de services)

# ... (autres fonctions de pages)

# ---- Application Principale ----
def main():
    # Initialisation de la session
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Accueil"
    
    # Navigation
    show_navigation()
    
    # Affichage de la page courante
    if st.session_state.current_page == "Accueil":
        home_page()
    elif st.session_state.current_page == "Nos Services":
        services_page()
    # ... (autres conditions pour chaque page)
    
    # Pied de page commun
    st.markdown("---")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("**IGED**  \nInnovation Groupe Étude Digitale")
    with cols[1]:
        st.markdown("[Mentions légales]  \n[Politique de confidentialité]")
    with cols[2]:
        st.markdown("[Facebook] | [Instagram] | [LinkedIn]")

if __name__ == "__main__":
    main()
