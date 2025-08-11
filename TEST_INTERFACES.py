import io
import os
import datetime as dt
import streamlit as st

# -------------------------------------------------
# ICPE‑VRD Analyzer — UI minimaliste (sans LangChain)
# Objectif: avoir un visuel de l'interface avant d'intégrer le RAG
# Dépendances: uniquement 'streamlit'
# Lancement:  streamlit run app.py
# -------------------------------------------------

st.set_page_config(page_title="ICPE‑VRD Analyzer", layout="wide")

# ---------------- Sidebar ----------------
st.sidebar.title("ICPE‑VRD Analyzer")
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_column_width=True)

mode = st.sidebar.radio("Mode de travail", ["Local (maquette)", "Atlas Data API (bientôt)"])
uploaded = st.sidebar.file_uploader("Téléversez des PDF (maquette)", type=["pdf"], accept_multiple_files=True)

rubriques = st.sidebar.multiselect("Rubrique ICPE", ["1510", "2710", "Autre"], default=["1510"]) 
source_types = st.sidebar.multiselect("Type de source", ["Arrêté", "Guide", "Notice"], default=["Arrêté","Guide"]) 

st.sidebar.markdown("---")
build_clicked = st.sidebar.button("Construire l’index (mock)")
update_clicked = st.sidebar.button("Mettre à jour (mock)")

# Persistance simple en session
if "docs" not in st.session_state:
    st.session_state.docs = []

if uploaded:
    # En maquette, on ne lit pas les PDF; on mémorise juste les noms
    st.session_state.docs = [f.name for f in uploaded]

# ---------------- Header ----------------
st.title("🔎 ICPE‑VRD Analyzer — Maquette UI")
st.caption(
    f"Mode: {mode} • Documents: {len(st.session_state.docs)} • Date: {dt.date.today().isoformat()}"
)

# Feedback boutons mock
def notify(msg):
    with st.status("", expanded=False) as status:
        st.write(msg)
        status.update(label="OK", state="complete")

if build_clicked:
    notify("Étapes simulées: extraction → découpage → indexation (aucun traitement réel)")
if update_clicked:
    notify("MàJ simulée du corpus (aucun traitement réel)")

# ---------------- Zone requête ----------------
col1, col2 = st.columns([3,1])
with col1:
    query = st.text_area(
        "Décrivez la modification VRD à analyser",
        height=120,
        placeholder="Ex: Déplacement d’un bassin de rétention vers l’ouest pour libérer une voie pompière…",
    )
with col2:
    k = st.number_input("Top‑K extraits (mock)", min_value=1, max_value=20, value=5)

analyze = st.button("Analyser", type="primary")

# ---------------- Résultats (mock) ----------------

def fake_results(query: str, k: int):
    """Génère des extraits factices pour illustrer l'UI."""
    base_docs = st.session_state.docs or ["arrete_1510.pdf", "guide_entrepots.pdf"]
    out = []
    for i in range(k):
        doc = base_docs[i % len(base_docs)]
        page = 1 + (i % 12)
        text = (
            f"[Extrait simulé] Réponse liée à: '{query[:60]}…'\n"
            f"• Source: {doc} — page {page}\n"
            "• Contenu: obligations ICPE (rubrique 1510), accès pompiers, bassins de rétention.\n"
            "• Note: Ceci est un texte de démonstration, aucun calcul d'embed n'est fait."
        )
        out.append({"doc": doc, "page": page, "text": text, "version": "v1", "is_current": True})
    return out

if analyze:
    if not query.strip():
        st.warning("Saisissez une requête.")
    else:
        with st.spinner("Recherche simulée des extraits pertinents…"):
            res = fake_results(query, int(k))
        tab1, tab2, tab3, tab4 = st.tabs(["📚 Extraits", "🧠 Analyse (à venir)", "📄 Démarche admin", "⚠️ Criticité"])        
        with tab1:
            for i, d in enumerate(res, 1):
                with st.expander(f"{i}. {d['doc']} — page {d['page']}"):
                    st.write(d["text"]) 
                    st.caption(f"Version: {d['version']} • is_current={d['is_current']}")
        with tab2:
            st.info("Ici viendra la synthèse LLM quand l'API sera branchée.")
        with tab3:
            st.write("Règles métiers pour PAC / modif. d’autorisation — à implémenter.")
        with tab4:
            st.write("Heuristiques de criticité environnementale — à implémenter.")

        # Export simple d'un 'rapport' texte (pas de dépendance reportlab)
        report = io.StringIO()
        report.write("ICPE‑VRD — Fiche d’analyse (maquette)\n")
        report.write(f"Date: {dt.datetime.now().isoformat()}\n")
        report.write(f"Requête: {query}\n\n")
        for i, d in enumerate(res, 1):
            report.write(f"[{i}] {d['doc']} p.{d['page']}\n")
            report.write(d["text"] + "\n\n")
        st.download_button(
            "📄 Télécharger la fiche (TXT)",
            data=report.getvalue().encode("utf-8"),
            file_name="analyse_icpe_vrd.txt",
            mime="text/plain",
        )

# ---------------- Pied de page ----------------
st.markdown("---")
st.caption("Maquette UI sans LangChain/FAISS. Intégration RAG et PDF viendront ensuite.")
