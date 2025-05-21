import streamlit as st

# Configuration de la page
st.set_page_config(page_title="ELECTRO SOLUT – Vente d'ordinateurs", layout="wide")

# --- Bannière avec logo ---
st.markdown("""
    <div style="background-color:#0A5275;padding:20px;border-radius:10px;">
        <h1 style="color:white;text-align:center;">💻 ELECTRO SOLUT</h1>
        <h3 style="color:white;text-align:center;">Votre partenaire en solutions informatiques</h3>
    </div>
""", unsafe_allow_html=True)

# --- Présentation de l'entreprise ---
st.header("📢 À propos de nous")
st.write("""
**ELECTRO SOLUT** est une entreprise spécialisée dans la vente d'ordinateurs portables, de bureau et d’accessoires tech haut de gamme.
Nous proposons des produits fiables, performants et adaptés à tous les besoins (étudiants, professionnels, gamers, etc.).
""")

# --- Catalogue de produits ---
st.header("🛒 Nos produits")
cols = st.columns(3)

with cols[0]:
    st.image("https://images.unsplash.com/photo-1517336714731-489689fd1ca8", caption="Ordinateur portable ProBook", use_container_width=True)
    st.write("💰 **Prix :** 899 €")
    st.write("💡 Idéal pour les professionnels.")

with cols[1]:
    st.image("https://images.unsplash.com/photo-1587202372775-a429ef54b29b", caption="Ordinateur Gamer X-Treme", use_container_width=True)
    st.write("💰 **Prix :** 1299 €")
    st.write("🎮 Hautes performances pour gaming et montage vidéo.")

with cols[2]:
    st.image("https://images.unsplash.com/photo-1584270354949-1f7f25e6b3b9", caption="Mini PC Compact", use_container_width=True)
    st.write("💰 **Prix :** 499 €")
    st.write("🧳 Ultra-portable, idéal pour les déplacements.")

# --- Formulaire de contact ---
st.header("📬 Contactez-nous")
with st.form(key='contact_form'):
    nom = st.text_input("Nom")
    email = st.text_input("Email")
    message = st.text_area("Votre message")
    envoyer = st.form_submit_button("Envoyer")

    if envoyer:
        st.success("✅ Merci pour votre message ! Nous vous répondrons dans les plus brefs délais.")

# --- Pied de page ---
st.markdown("""
    <hr>
    <div style="text-align:center;">
        <p>© 2025 ELECTRO SOLUT – Tous droits réservés.</p>
        <p>📧 contact@electrosolut.com | 📞 +33 1 23 45 67 89</p>
    </div>
""", unsafe_allow_html=True)
