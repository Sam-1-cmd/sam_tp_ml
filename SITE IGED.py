import streamlit as st
from PIL import Image
import pandas as pd
import openai
# Configuration de la page
st.set_page_config(
    page_title="IGED Innovation groupe étude digitale",
    page_icon="📚",
    layout="wide"
)

st.markdown(
    """
    <div style="position: relative; text-align: center; color: white; margin-bottom: 2rem;">
        <img src="https://urls.fr/ZmO3Ro" alt="Image d'accueil" style="width: 90%; height: auto; border-radius: 10px; display: block; margin: 0 auto;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                   background-color: rgba(0, 0, 0, 0.6); 
                   padding: 20px; border-radius: 10px; width: 80%; max-width: 600px;">
            <h1 style="margin: 0; font-size: 2.5rem;">Bienvenue sur notre plateforme</h1>
            <p style="margin: 10px 0 0; font-size: 1.2rem;">Cours particuliers sur mesure</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# CSS personnalisé
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Header avec logo et navigation
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("IGED")
    st.subheader("Innovation Groupe Étude Digitale")

# Navigation
menu = ["Accueil", "Nos Services", "Nos Professeurs", "Tarifs", "Contact", "Espace Élève"]
choice = st.sidebar.selectbox("Navigation", menu)

# Section Accueil
if choice == "Accueil":
    st.header("Votre réussite, notre priorité")
    st.image("https://www.entreprenanteafrique.com/wp-content/uploads/2019/09/Enko-John-Wesley_Abidjan-1024x630.jpg", use_container_width=True)
    
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

openai.api_key = st.secrets["OPENAI_API_KEY"]

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


    with col3:
        st.title("Assistant IA")

        user_input = st.text_input("Pose ta question à l'IA 👇")

        if user_input:
              output = get_chatgpt_response(user_input)
              st.write("🧠 Réponse de l'IA :")
              st.write(output)



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
    profs = pd.DataFrame({
        'Photo': ["prof1.jpg", "prof2.jpg", "prof3.jpg"],
        'Nom': ["Marie Dupont", "Jean Martin", "Sophie Leroy"],
        'Matières': ["Mathématiques/Physique", "Français/Philosophie", "Anglais/Espagnol"],
        'Expérience': ["15 ans d'expérience, ancienne professeure en CPGE",
                      "10 ans d'expérience, correcteur du bac",
                      "Bilingue, 8 ans d'expérience en lycée international"],
        'Diplômes': ["Agrégée de Mathématiques", "Docteur en Lettres Modernes", "Master en Langues Étrangères"]
    })

    for i in range(len(profs)):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(profs['Photo'][i], width=150)
        with col2:
            st.subheader(profs['Nom'][i])
            st.write(f"**Matières:** {profs['Matières'][i]}")
            st.write(f"**Expérience:** {profs['Expérience'][i]}")
            st.write(f"**Diplômes:** {profs['Diplômes'][i]}")
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
        with st.form(key='contact_form'):
            nom = st.text_input("Nom*")
            email = st.text_input("Email*")
            telephone = st.text_input("Téléphone")
            sujet = st.selectbox("Sujet", ["Demande d'information", "Inscription", "Recrutement", "Autre"])
            message = st.text_area("Message*")
            submitted = st.form_submit_button("Envoyer")
            if submitted:
                if nom and email and message:
                    st.success("Message envoyé! Nous vous répondrons dans les 48h.")
                    st.markdown(f"""
                    <form action="https://formsubmit.co/brousybah08@gmail.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_next" value="https://ton-site.com/merci">
                    <input type="text" name="Nom" value="{nom}" hidden>
                    <input type="email" name="Email" value="{email}" hidden>
                    <textarea name="Message" hidden>{message}</textarea>
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
        st.image("platforme.jpg", width=500)

# Pied de page
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.write("© 2023 IGED - Tous droits réservés")
with footer_col2:
    st.write("Mentions légales | CGV | Politique de confidentialité")
with footer_col3:
    st.write("Suivez-nous: [Facebook] [Instagram] [LinkedIn]")
