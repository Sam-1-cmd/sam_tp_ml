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

# ---- Bannière Supérieure Améliorée ----
st.markdown("""
<div style="background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%); 
            padding: 3rem 1rem; border-radius: 10px; color: white; 
            text-align: center; margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">IGED</h1>
    <p style="font-size: 1.5rem; margin: 0.5rem 0 1.5rem 0;">
    Innovation Groupe Étude Digitale
    </p>
    <div style="display: flex; justify-content: center; gap: 1.5rem;">
        <a href="#formule" style="background: #ff6b6b; border: none; padding: 0.75rem 2rem; 
                      border-radius: 30px; color: white; text-decoration: none;
                      font-weight: 600; cursor: pointer;">Nos Formules</a>
        <a href="#contact" style="background: rgba(255,255,255,0.2); border: 2px solid white; 
                      padding: 0.75rem 2rem; border-radius: 30px; color: white; 
                      text-decoration: none; font-weight: 600; cursor: pointer;">Contact Rapide</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Layout Principal (2 Colonnes) ----
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    # Section Présentation
    st.markdown("""
    ## 📚 Votre réussite, notre priorité
    
    **IGED** combine expertise pédagogique et solutions digitales pour :
    - 🎯 **Programmes personnalisés** avec suivi algorithmique
    - 👨‍🏫 **+50 professeurs** certifiés (95% de satisfaction)
    - 📈 **92% de réussite** aux examens 2023
    - 💻 **Plateforme interactive** disponible 24h/24
    """)
    
    # Témoignage
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;
                border-left: 4px solid #6e48aa;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <img src="https://randomuser.me/api/portraits/women/65.jpg" 
                 style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover;">
            <div>
                <p style="font-weight: bold; margin: 0 0 0.2rem 0; font-size: 1.1rem;">Amina K., 16 ans</p>
                <p style="margin: 0; color: #555;">"Avec IGED, ma moyenne en maths est passée de 8 à 15 en 3 mois !"</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vidéo explicative
    st.video("https://youtu.be/5agcs8--Szo?si=4tg2qHFHuiRqvxrk")

with col_right:
    # Formulaire Compact
    with st.form(key='contact_rapide'):
        st.markdown("### ✉️ Demande de contact")
        name = st.text_input("Nom complet*")
        niveau = st.selectbox("Niveau scolaire*", 
                            ["Primaire", "Collège", "Lycée", "Supérieur"])
        phone = st.text_input("Téléphone*")
        submitted = st.form_submit_button("Être rappelé(e)")
        if submitted:
            if name and phone:
                st.success(f"Merci {name.split()[0]}! Un conseiller vous contactera pour le {niveau}.")
            else:
                st.error("Veuillez remplir les champs obligatoires (*)")
    
    # Carte des centres
    with st.expander("📍 Nos centres en Côte d'Ivoire", expanded=True):
        st.map(data=pd.DataFrame({
            'lat': [5.3167, 5.3541, 7.6906],  # Yamoussoukro/Abidjan/Bouaké
            'lon': [-4.0333, -4.0016, -5.0303],
            'name': ['IGED Yamoussoukro', 'IGED Abidjan', 'IGED Bouaké']
        }), zoom=6)
    
    # Assistant IA
    st.markdown("""
    <div style="background: #f0f2f6; padding: 1.25rem; border-radius: 10px; margin-top: 1.5rem;">
        <h4 style="margin-top: 0;">🤖 Assistant IGED</h4>
        <p>Obtenez une réponse immédiate à vos questions :</p>
        <ul style="margin-bottom: 0;">
            <li>Disponibilité des professeurs</li>
            <li>Tarifs et financements</li>
            <li>Méthodes pédagogiques</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Poser une question →", key="assistant_btn"):
        st.session_state.show_chat = True

# ---- Pied de Page ----
st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.markdown("**IGED**  \nInnovation Groupe Étude Digitale  \n© 2024 Tous droits réservés")
with footer_cols[1]:
    st.markdown("📞 [07 45 50 24 52](tel:+2250745502452)  \n✉️ [contact@iged-ci.com](mailto:contact@iged-ci.com)")
with footer_cols[2]:
    st.markdown("[Facebook](https://facebook.com) | [Instagram](https://instagram.com) | [LinkedIn](https://linkedin.com)")

# ---- CSS Personnalisé ----
st.markdown("""
<style>
    [data-testid="stForm"] {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stVideo {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# CSS personnalisé
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")  

# Fonction pour l'envoi d'emails avec pièces jointes
def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        msg.attach(attach)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# Header avec logo et navigation
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("IGED")
    st.subheader("Innovation Groupe Étude Digitale")

# Navigation - Ajout de "Recrutement" dans le menu
menu = ["Accueil", "Nos Services", "Nos Professeurs", "Tarifs", "Contact", "Espace Élève", "Recrutement"]
choice = st.sidebar.selectbox("Navigation", menu)

# Fonction pour les réponses ChatGPT
def get_chatgpt_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erreur API OpenAI : {e}")
        return "Une erreur est survenue en contactant ChatGPT."

# Section Accueil
if choice == "Accueil":
    st.header("Votre réussite, notre priorité")
    st.image("https://www.entreprenanteafrique.com/wp-content/uploads/2019/09/Enko-John-Wesley_Abidjan-1024x630.jpg", 
             use_container_width=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### Bienvenue chez IGED

        **IGED - Innovation Groupe Étude Digitale** est un centre de soutien scolaire innovant
        qui combine expertise pédagogique et solutions digitales pour offrir un accompagnement
        personnalisé à chaque élève.

        - 📈 Résultats garantis
        - 👩‍🏫 Professeurs qualifiés
        - 💻 Plateforme digitale interactive
        - 🏆 95% de satisfaction
        """)

    with col2:
        with st.form(key='contact_form'):
            st.write("Programmer un rendez-vous avec un collaborateur IGED")
            name = st.text_input("Nom de l'élève")
            niveau = st.selectbox("Niveau scolaire", ["Primaire", "Collège", "Lycée", "Supérieur"])
            matiere = st.text_input("Matière(s) concernée(s)")
            phone = st.text_input("Téléphone")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Envoyer la demande")
            
            if submitted:
                message = f"Demande de cours pour {name}\nNiveau: {niveau}\nMatière: {matiere}\nContact: {phone} | {email}"
                st.markdown(f"""
                <form action="https://formsubmit.co/brousybah08@gmail.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_next" value="https://ton-site.com/merci">
                    <input type="text" name="Nom" value="{name}" hidden>
                    <input type="email" name="Email" value="{email}" hidden>
                    <textarea name="Message" hidden>{message}</textarea>
                    <button type="submit">Envoyer</button>
                </form>
                """, unsafe_allow_html=True)
                st.success("Demande envoyée! Nous vous contacterons sous 48h.")

    with col3:
        st.title("Assistant IA")
        
        option = st.selectbox("Choisis une action :", 
                            ["Poser une question", "Afficher une aide", "Quitter"])

        if option == "Poser une question":
            user_input = st.text_input("Écris ta question ici")
            if user_input:
                with st.spinner("L'IA réfléchit..."):
                    output = get_chatgpt_response(user_input)
                st.write(output)

        elif option == "Afficher une aide":
            st.info("Tape ta question pour interagir avec l'IA. Tu peux poser des questions sur:\n- Tes cours\n- De l'aide aux devoirs\n- Des conseils méthodologiques")

        elif option == "Quitter":
            st.warning("Au revoir 👋")

# Section Nos Services
elif choice == "Nos Services":
    st.header("Nos Solutions Pédagogiques")
    tabs = st.tabs(["Cours Particuliers", "Stages Intensifs", "Aide aux Devoirs", "Préparation Examens"])

    with tabs[0]:
        st.subheader("Cours Particuliers à Domicile ou en Ligne")
        st.markdown("""
        - 🔄 **Suivi régulier** ou ⏱️ **ponctuel**  
        - 🌍 **Toutes matières**, 🎓 **tous niveaux**  
        - 🕒 **Créneaux flexibles** (matin/soir/week-end)  
        - 🔍 **Bilan pédagogique initial** gratuit  
        - ✉️ **Compte-rendu détaillé** après chaque séance  
        """)
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://tewmoutew.com/img/photos/2021-10-02-201830_bde15679.jpg" 
                style="width: 400px; border-radius: 10px;" />
                <p style="font-style: italic;">Nos professeurs se déplacent à votre domicile</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tabs[1]:
        st.subheader("Stages Intensifs pendant les Vacances")
        st.markdown("""
        - Stages de révision
        - Stages de remise à niveau
        - Préparation aux examens (Brevet, Bac, Concours)
        - En petits groupes ou individuels
        - 10h à 30h par semaine
        """)

    with tabs[2]:
        st.subheader("Aide aux Devoirs")
        st.markdown("""
        - Encadrement quotidien
        - Méthodologie de travail
        - Organisation du temps
        - Pour les élèves du primaire au collège
        """)

    with tabs[3]:
        st.subheader("Préparation aux Examens")
        st.markdown("""
        - BEPC
        - Baccalauréat toutes séries 
        - Concours post-bac
        - Examens blancs corrigés
        - Simulation d'oraux
        """)

# Section Nos Professeurs
elif choice == "Nos Professeurs":
    st.header("Notre Équipe Pédagogique")
    
    profs_data = [
        {
            "Photo": "https://via.placeholder.com/150",
            "Nom": "Marie Dupont",
            "Matières": "Mathématiques/Physique",
            "Expérience": "15 ans d'expérience, ancienne professeure en CPGE",
            "Diplômes": "Agrégée de Mathématiques"
        },
        {
            "Photo": "https://via.placeholder.com/150",
            "Nom": "Jean Martin",
            "Matières": "Français/Philosophie",
            "Expérience": "10 ans d'expérience, correcteur du bac",
            "Diplômes": "Docteur en Lettres Modernes"
        },
        {
            "Photo": "https://via.placeholder.com/150",
            "Nom": "Sophie Leroy",
            "Matières": "Anglais/Espagnol",
            "Expérience": "Bilingue, 8 ans d'expérience en lycée international",
            "Diplômes": "Master en Langues Étrangères"
        }
    ]

    for prof in profs_data:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(prof["Photo"], width=150)
        with col2:
            st.subheader(prof["Nom"])
            st.write(f"**Matières:** {prof['Matières']}")
            st.write(f"**Expérience:** {prof['Expérience']}")
            st.write(f"**Diplômes:** {prof['Diplômes']}")
        st.markdown("---")

# Section Tarifs
elif choice == "Tarifs":
    st.header("Nos Tarifs")
    st.markdown("""
    ### Forfaits Cours Particuliers
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Découverte")
        st.write("💶 35€/h")
        st.write("✅ 1 à 5h")
        st.write("✅ Bilan initial")
        st.write("✅ Suivi mensuel")

    with col2:
        st.subheader("Progrès")
        st.write("💶 32€/h")
        st.write("✅ 10h à 20h")
        st.write("✅ Programme personnalisé")
        st.write("✅ 1 examen blanc offert")

    with col3:
        st.subheader("Excellence")
        st.write("💶 30€/h")
        st.write("✅ 30h et plus")
        st.write("✅ Coordinateur pédagogique")
        st.write("✅ 2 examens blancs offerts")

    st.markdown("""
    ---
    ### Autres Services
    - **Aide aux devoirs:** 25€/h
    - **Stages intensifs:** 250€ la semaine (10h)
    - **Préparation examens:** 40€/h (spécial concours)

    *50% de réduction d'impôt sur les cours à domicile*
    """)

# Section Contact
elif choice == "Contact":
    st.header("Contactez-nous")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nos Coordonnées")
        st.markdown("""
        **IGED - Innovation Groupe Étude Digitale**
        📍 YAMOUSSOKRO, CÔTE D'IVOIRE
        📞 07 45 50 24 52
        ✉️ brousybah08@gmail.com
        📞 Vous pouvez aussi nous appeler : [**Appeler maintenant**](tel:+3374502452)     
        """)
        st.markdown("""
        **Horaires d'ouverture:**
        Lundi-Vendredi: 9h-19h
        Samedi: 9h-17h     
        """)

        st.subheader("Nos Agences")
        st.write("📍 ABIDJAN | YAMOUSSOUKO | BOUAKE ")

    with col2:
        st.subheader("Formulaire de Contact")
        with st.form(key='contact_form2'):
            nom = st.text_input("Nom*")
            email = st.text_input("Email*")
            telephone = st.text_input("Téléphone")
            sujet = st.selectbox("Sujet", ["Demande d'information", "Inscription", "Recrutement", "Autre"])
            message = st.text_area("Message*")
            submitted = st.form_submit_button("Envoyer")
            
            if submitted:
                if nom and email and message:
                    st.success("Message envoyé! Nous vous répondrons dans les 48h.")
                    contact_message = f"Nouveau message de {nom}\nEmail: {email}\nTéléphone: {telephone}\nSujet: {sujet}\nMessage: {message}"
                    st.markdown(f"""
                    <form action="https://formsubmit.co/brousybah08@gmail.com" method="POST">
                        <input type="hidden" name="_captcha" value="false">
                        <input type="hidden" name="_next" value="https://ton-site.com/merci">
                        <input type="text" name="Nom" value="{nom}" hidden>
                        <input type="email" name="Email" value="{email}" hidden>
                        <textarea name="Message" hidden>{contact_message}</textarea>
                        <button type="submit">Envoyer</button>
                    </form>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Veuillez remplir les champs obligatoires (*)")

# Section Espace Élève
elif choice == "Espace Élève":
    st.header("Espace Élève IGED")
    tab1, tab2 = st.tabs(["Connexion", "Première visite"])

    with tab1:
        with st.form("login"):
            st.write("Connectez-vous à votre espace")
            username = st.text_input("Identifiant")
            password = st.text_input("Mot de passe", type="password")
            connect = st.form_submit_button("Se connecter")
            if connect:
                st.warning("Cette fonctionnalité sera disponible dans la version finale")

    with tab2:
        st.write("""
        ### Nouveau chez IGED ?

        Notre plateforme digitale vous permet de:
        - Accéder à vos cours en ligne
        - Consulter vos progrès
        - Échanger avec votre professeur
        - Télécharger des ressources

        **Demandez vos identifiants à votre conseiller pédagogique**
        """)
        st.image("https://via.placeholder.com/500x300?text=Plateforme+IGED", width=500)

# Section Recrutement (Nouvelle section ajoutée)
elif choice == "Recrutement":
    st.title("🚀 Rejoignez notre équipe pédagogique")
    
    with st.expander("Pourquoi nous rejoindre ?"):
        st.markdown("""
        - Environnement dynamique et innovant
        - Formation continue offerte
        - Rémunération compétitive (+30% vs marché)
        - Flexibilité horaire
        """)
    
    tab1, tab2 = st.tabs(["Postuler", "Processus de recrutement"])
    
    with tab1:
        with st.form(key='recruitment_form'):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Nom complet*")
                email = st.text_input("Email*")
                phone = st.text_input("Téléphone*")
            with cols[1]:
                niveau = st.multiselect("Niveaux enseignés*", 
                                      ["Primaire", "Collège", "Lycée", "Supérieur"])
                matieres = st.text_input("Matières enseignées* (séparées par des virgules)")
            
            experience = st.text_area("Expérience pédagogique* (années, établissements)")
            motivation = st.text_area("Pourquoi souhaitez-vous rejoindre IGED ?*")
            
            cv = st.file_uploader("CV (PDF uniquement)*", type="pdf")
            video = st.file_uploader("Vidéo de présentation (optionnel)", type=["mp4", "mov"])
            
            submitted = st.form_submit_button("Soumettre ma candidature")
            
            if submitted:
                # Validation des champs
                if not all([name, email, phone, niveau, matieres, experience, motivation, cv]):
                    st.error("Veuillez remplir tous les champs obligatoires")
                else:
                    # Traitement du CV
                    with open(f"CV_{name.replace(' ', '_')}.pdf", "wb") as f:
                        f.write(cv.getbuffer())
                    
                    # Envoi email
                    try:
                        send_email_with_attachments(
                            subject=f"Candidature {name}",
                            body=f"Nouvelle candidature...",
                            attachments=[f"CV_{name.replace(' ', '_')}.pdf"]
                        )
                        st.success("Candidature envoyée avec succès!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erreur lors de l'envoi: {str(e)}")
    
    with tab2:
        st.markdown("""
        ### Notre processus en 4 étapes :
        1. 📝 Analyse de votre candidature (48h)
        2. 📞 Entretien téléphonique (30min)
        3. 🎤 Entretien pédagogique (1h)
        4. 🏫 Journée d'immersion (optionnelle)
        
        *Nous répondons à toutes les candidatures sous 72h*
        """)
# Pied de page
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.write("© 2023 IGED - Tous droits réservés")
with footer_col2:
    st.write("[Mentions légales] | [CGV] | [Politique de confidentialité]")
with footer_col3:
    st.write("Suivez-nous: [Facebook] [Instagram] [LinkedIn]")
