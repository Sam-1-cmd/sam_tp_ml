import streamlit as st
import openai

# Configuration de la page
st.set_page_config(
    page_title="Institut IGED",
    page_icon="📘",
    layout="wide"
)

# Configuration de l'API OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Pour un test local, tu peux temporairement remplacer par :
# openai.api_key = "ta_clé_personnelle"

# Fonction pour obtenir une réponse de ChatGPT
def get_chatgpt_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    message = completions.choices[0].text.strip()
    return message

# Titre principal
st.title("Bienvenue à l'Institut IGED 🎓")
st.write("Institut de soutien scolaire et d’excellence académique.")

# Barre de menu horizontale
menu = st.selectbox("Navigation", ["Accueil", "Nos services", "Prendre un rendez-vous", "Contact"])

# Page d'accueil
if menu == "Accueil":
    st.header("À propos de nous")
    st.write("""
        IGED est un institut de soutien scolaire pour les élèves du primaire au lycée.
        Nous mettons l'accent sur la réussite, la rigueur, et la motivation.
    """)
    
    st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754", caption="Nos élèves en cours", use_column_width=True)

    st.subheader("Notre équipe pédagogique")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://randomuser.me/api/portraits/women/1.jpg", caption="Mme. Keïta – Mathématiques")
    with col2:
        st.image("https://randomuser.me/api/portraits/men/2.jpg", caption="M. N’Guessan – Physique-Chimie")
    with col3:
        st.image("https://randomuser.me/api/portraits/women/3.jpg", caption="Mme. Coulibaly – Français")

# Page Services
elif menu == "Nos services":
    st.header("Nos services 📚")
    st.markdown("""
    - **Soutien scolaire personnalisé**
    - **Préparation au brevet et au baccalauréat**
    - **Cours de langues (Anglais, Espagnol, etc.)**
    - **Stages de vacances**
    """)

# Page Prendre un rendez-vous
elif menu == "Prendre un rendez-vous":
    st.header("Réserver un rendez-vous 🗓️")

    with st.form(key='rendez_vous_form'):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        date = st.date_input("Date souhaitée")
        heure = st.time_input("Heure")
        message = st.text_area("Message ou commentaires")
        submit = st.form_submit_button("Envoyer")

        if submit:
            st.success(f"Merci {name}, votre demande de rendez-vous a bien été enregistrée !")

# Page Contact + Assistant IA
elif menu == "Contact":
    col1, col2, col3 = st.columns([1, 1, 1])

    # Bloc Contact
    with col1:
        st.header("Contactez-nous 📞")
        with st.form(key='contact_form'):
            name = st.text_input("Nom complet")
            email = st.text_input("Adresse Email")
            message = st.text_area("Votre message")
            submit_button = st.form_submit_button("Envoyer")
            if submit_button:
                st.success("Votre message a été envoyé avec succès.")

    # Bloc Infos pratiques
    with col2:
        st.header("Informations pratiques")
        st.markdown("""
        **Adresse :** 10 Rue de l'Éducation, Abidjan  
        **Téléphone :** +225 01 23 45 67 89  
        **Email :** contact@institutiged.ci  
        **Horaires :** Lundi - Samedi, 8h - 18h
        """)

    # Bloc Assistant IA
    with col3:
        st.header("Assistant IA 🤖")
        prompt = st.text_input("Posez votre question")
        if st.button("Demander à l'IA"):
            if prompt:
                response = get_chatgpt_response(prompt)
                st.success(response)
            else:
                st.warning("Veuillez saisir une question avant d’envoyer.")
