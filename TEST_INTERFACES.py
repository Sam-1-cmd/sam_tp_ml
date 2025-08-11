import io
import os
import datetime as dt
import streamlit as st

# -------------------------------------------------
# ICPE-VRD Analyzer — UX centrée Utilisateur + Panneau Admin
# Dépendances: streamlit uniquement
# Lancement:  streamlit run app.py
# -------------------------------------------------

st.set_page_config(page_title="ICPE-VRD Analyzer", layout="wide")

# ----------------- Styles légers -----------------
st.markdown("""
<style>
.badge {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;}
.badge.low {background:#E6F4EA; color:#137333;}
.badge.med {background:#FFF4E5; color:#8A5200;}
.badge.high{background:#FCE8E6; color:#A50E0E;}
.card {border:1px solid #eee; border-radius:12px; padding:12px; margin-bottom:10px;}
.small {opacity:.8; font-size:12px;}
hr {margin: 0.8rem 0;}
</style>
""", unsafe_allow_html=True)

# ----------------- Etat session -----------------
if "docs" not in st.session_state:
    st.session_state.docs = []             # noms de fichiers chargés (maquette)
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False      # login admin (démo)

# ----------------- Helpers -----------------
def severity_badge(level: str):
    level = level.lower()
    cls = "low" if level == "faible" else "med" if level == "moyenne" else "high"
    st.markdown(f'<span class="badge {cls}">{level.capitalize()}</span>', unsafe_allow_html=True)

def fake_results(query: str, k: int, contexte: dict):
    """Génère des extraits factices pour illustrer l'UI côté utilisateur."""
    base_docs = st.session_state.docs or ["arrete_1510.pdf", "guide_entrepots.pdf"]
    out = []
    for i in range(k):
        doc = base_docs[i % len(base_docs)]
        page = 1 + (i % 14)
        text = (
            f"[Extrait simulé] Contexte: {contexte.get('type_intervention','(n/a)')} — Projet: {contexte.get('projet','(n/a)')}\n"
            f"• Source: {doc} — page {page}\n"
            f"• Lien avec: '{(query or '')[:60]}…'\n"
            "• Points: accès pompiers, bassins de rétention, seuils rubrique 1510, eaux pluviales.\n"
            "• Note: Démonstration UI (aucun embed/ranking réel)."
        )
        out.append({"doc": doc, "page": page, "text": text, "version": "v1", "is_current": True})
    return out

def export_txt(query: str, res: list, contexte: dict) -> bytes:
    report = io.StringIO()
    report.write("ICPE-VRD — Fiche d’analyse (maquette)\n")
    report.write(f"Date: {dt.datetime.now().isoformat()}\n")
    report.write(f"Projet: {contexte.get('projet','')}, Commune: {contexte.get('commune','')}\n")
    report.write(f"Type d’intervention: {contexte.get('type_intervention','')}\n")
    report.write(f"Question: {query}\n\n")
    for i, d in enumerate(res, 1):
        report.write(f"[{i}] {d['doc']} p.{d['page']}\n{d['text']}\n\n")
    return report.getvalue().encode("utf-8")

# ----------------- Sidebar (rôle) -----------------
st.sidebar.title("ICPE-VRD Analyzer")
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_column_width=True)

role = st.sidebar.radio("Profil", ["Utilisateur chantier / AMO", "Admin (index & docs)"], horizontal=False)

# ----------------- Panneau Admin -----------------
def render_admin():
    st.title("🛠️ Administration — Corpus & Index")
    st.caption("Cette section est réservée aux opérations d’ingestion et de (ré)indexation. Les utilisateurs finaux n’y ont pas accès.")

    with st.expander("Connexion (démo)", expanded=not st.session_state.admin_ok):
        pwd = st.text_input("Mot de passe admin (démo)", type="password", placeholder="••••••••")
        colA, colB = st.columns([1,3])
        with colA:
            if st.button("Se connecter"):
                st.session_state.admin_ok = (pwd == "admin")   # ⚠️ démo : remplace par un vrai auth plus tard
        with colB:
            st.info("Mot de passe de démonstration : **admin** (à remplacer par streamlit-authenticator ou SSO interne).")

    if not st.session_state.admin_ok:
        st.stop()

    st.subheader("📁 Documents du corpus")
    uploaded = st.file_uploader("Téléverser des PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded:
        # Maquette : on ne lit pas, on mémorise les noms uniquement.
        st.session_state.docs = list({*st.session_state.docs, *[f.name for f in uploaded]})
        st.success(f"{len(uploaded)} document(s) ajouté(s).")

    if st.session_state.docs:
        st.write("Documents présents :")
        for i, n in enumerate(sorted(st.session_state.docs), 1):
            st.markdown(f"- {i}. {n}")
    else:
        st.warning("Aucun document pour l’instant.")

    st.markdown("---")
    st.subheader("⚙️ Indexation")
    with st.expander("Paramètres avancés (pour experts)"):
        k_admin = st.number_input("Top-K par défaut (maquette, pour tests internes)", min_value=1, max_value=50, value=5, help="N’affecte pas l’UI Utilisateur.")
        st.caption("Quand le RAG sera branché : choix du splitter, taille de chunk, overlap, modèle d’embeddings, stockage FAISS, etc.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Construire l’index (mock)"):
            with st.status("", expanded=False) as s:
                st.write("Étapes simulées: extraction → chunking → embeddings → FAISS.")
                s.update(label="Index prêt (maquette)", state="complete")
    with col2:
        if st.button("Mettre à jour l’index (mock)"):
            with st.status("", expanded=False) as s:
                st.write("Mise à jour simulée: détection delta, réindexation partielle.")
                s.update(label="Mise à jour terminée (maquette)", state="complete")

    st.markdown("---")
    st.caption("Conseil: séparer cette page dans /pages/01_Admin.py et activer une vraie authentification.")

# ----------------- Panneau Utilisateur -----------------
def render_user():
    st.title("🔎 ICPE-VRD Analyzer")
    st.caption(f"Date: {dt.date.today().isoformat()} • Corpus disponible: {len(st.session_state.docs)} document(s)")

    # Contexte (facultatif)
    with st.container(border=True):
        st.subheader("Contexte chantier (facultatif)")
        c1, c2, c3 = st.columns([2,2,2])
        with c1:
            projet = st.text_input("Nom du projet / site", placeholder="Plateforme logistique P3 Boisseaux")
        with c2:
            commune = st.text_input("Commune", placeholder="Boisseaux (45)")
        with c3:
            type_intervention = st.selectbox(
                "Type d’intervention VRD",
                [
                    "Déplacement réseau EU/EP",
                    "Création/Modification bassin de rétention",
                    "Reprofilage voirie / voie pompiers",
                    "Raccordement réseaux (élec, gaz, fibre)",
                    "Terrassement / Déblai-Remblai",
                    "Autre"
                ],
                index=1
            )
        st.caption("Ces champs aident à contextualiser l’analyse et le rapport exporté.")

    st.markdown("### Votre question")
    query = st.text_area(
        "Décrivez la situation ou posez votre question",
        height=120,
        placeholder="Ex: Déplacement du bassin de rétention de 20 m vers l’ouest pour libérer la voie pompiers. Impacts ICPE ? Démarches ?",
    )

    # Curseur d’exhaustivité (contrôle simple côté utilisateur)
    exha = st.slider("Niveau d’exhaustivité des extraits", 0, 100, 40,
                     help="Plus haut = plus d’extraits potentiels. Pas d’option technique type 'Top-K'.")
    top_k = 3 + int(exha / 25)   # 3..7

    if st.button("Analyser", type="primary"):
        if not query.strip():
            st.warning("Merci de saisir une question.")
            st.stop()

        contexte = {"projet": projet, "commune": commune, "type_intervention": type_intervention}
        with st.spinner("Analyse de la base documentaire (maquette)…"):
            res = fake_results(query, top_k, contexte)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📚 Extraits", "🧠 Synthèse", "📄 Démarches admin", "⚠️ Criticité", "✍️ Aide à la rédaction"]
        )

        with tab1:
            st.subheader("Extraits pertinents")
            for i, d in enumerate(res, 1):
                with st.expander(f"{i}. {d['doc']} — page {d['page']}"):
                    st.markdown(f"<div class='card'><pre>{d['text']}</pre>"
                                f"<div class='small'>Version: {d['version']} • is_current={d['is_current']}</div></div>",
                                unsafe_allow_html=True)

        with tab2:
            st.subheader("Synthèse (bientôt propulsée par LLM)")
            st.info("Ici viendra la synthèse automatique (obligations, points de vigilance, actions).")

        with tab3:
            st.subheader("Démarches administratives — proposition initiale (maquette)")
            st.write("- **PAC** (portée à connaissance) si la modification n’entraîne pas de dépassement de seuil ni changement notable.")
            st.write("- **Modification d’autorisation** si incidence significative sur l’impact environnemental ou sur la sécurité.")
            st.write("- **Étude d’impact** à réexaminer si le projet s’écarte substantiellement du scénario initial.")
            st.caption("Ces règles seront codées à partir d’un arbre de décision conforme aux textes ICPE (quand RAG/KB sera branché).")

        with tab4:
            st.subheader("Niveau de criticité (maquette)")
            colL, colM, colH = st.columns(3)
            with colL:
                st.write("• **Eaux pluviales** "); severity_badge("moyenne")
            with colM:
                st.write("• **Accès pompiers** "); severity_badge("faible")
            with colH:
                st.write("• **Risques inondation** "); severity_badge("moyenne")
            st.caption("La vraie version calculera des scores à partir des extraits + règles métiers.")

        with tab5:
            st.subheader("Aide à la rédaction (maquette)")
            st.write("Générer un **courrier PAC** :")
            st.code(
f"""Objet : Portée à connaissance – {projet or 'Projet X'} ({commune or 'Commune'})

Madame, Monsieur,
Dans le cadre du projet {projet or 'X'}, nous envisageons {type_intervention.lower()}.
Vous trouverez ci-joint les éléments descriptifs et les mesures de maîtrise envisagées.
Nous restons à votre disposition pour tout complément.

Cordialement,
Le maître d’ouvrage
""", language="text")

        # Export
        st.markdown("---")
        data = export_txt(query, res, contexte)
        st.download_button("📄 Télécharger la fiche (TXT)", data=data, file_name="analyse_icpe_vrd.txt", mime="text/plain")

# ----------------- Routage simple -----------------
if role.startswith("Admin"):
    render_admin()
else:
    render_user()

# ----------------- Pied de page -----------------
st.markdown("---")
st.caption("Maquette UX : panneau Utilisateur épuré • panneau Admin séparé pour ingestion & index. RAG à intégrer ensuite.")
