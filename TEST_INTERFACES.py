import io
import os
import datetime as dt
import streamlit as st

# -------------------------------------------------
# ICPE-VRD Analyzer — UX utilisateur + panneau Admin
# Version : v0.3.1-maquette — Correctifs f-strings & doublons
# Dépendances : streamlit uniquement
# Lancement    : streamlit run app.py
# -------------------------------------------------

st.set_page_config(page_title="ICPE‑VRD Analyzer", layout="wide")

# ----------------- Styles & thème (Inter) -----------------
st.markdown(
    """
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 0.8rem; padding-bottom: 3rem; }
.badge {display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600;}
.badge.low {background:#E6F4EA; color:#137333;}
.badge.med {background:#FFF4E5; color:#8A5200;}
.badge.high{background:#FCE8E6; color:#A50E0E;}
.card {border:1px solid #eee; border-radius:12px; padding:12px; margin-bottom:10px;}
.small {opacity:.8; font-size:12px;}
hr {margin: 0.8rem 0;}
.kpi .stMetric {border:1px solid #eee; border-radius:12px; padding:8px;}
.suggest .stButton>button {width:100%;}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------- Etat session -----------------
ss = st.session_state
ss.setdefault("docs", [])                 # noms de fichiers (maquette)
ss.setdefault("admin_ok", False)          # login admin (démo)
ss.setdefault("last_index_at", None)      # date/heure dernière indexation
ss.setdefault("history", [])              # dernières questions soumises
ss.setdefault("prefill_query", "")        # pré-remplissage du champ question

# ----------------- Helpers -----------------
def severity_badge(level: str):
    level = (level or "").lower()
    cls = "low" if level == "faible" else "med" if level == "moyenne" else "high"
    st.markdown(
        f"<span class='badge {cls}'>{(level.capitalize() if level else '—')}</span>",
        unsafe_allow_html=True,
    )

def fake_results(query: str, k: int, contexte: dict):
    """Génère des extraits factices pour illustrer l'UI côté utilisateur."""
    base_docs = ss.docs or ["arrete_1510.pdf", "guide_entrepots.pdf"]
    out = []
    for i in range(k):
        doc = base_docs[i % len(base_docs)]
        page = 1 + (i % 14)
        text = (
            f"[Extrait simulé] Contexte: {contexte.get('type_intervention','(n/a)')} — "
            f"Projet: {contexte.get('projet','(n/a)')}\n"
            f"• Source: {doc} — page {page}\n"
            f"• Lien avec: '{(query or '')[:60]}…'\n"
            "• Points: accès pompiers, bassins de rétention, seuils rubrique 1510, eaux pluviales.\n"
            "• Note: Démonstration UI (aucun embed/ranking réel)."
        )
        out.append({
            "doc": doc,
            "page": page,
            "text": text,
            "version": "v1",
            "is_current": True
        })
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

# ----------------- Sidebar (profil) -----------------
st.sidebar.title("ICPE‑VRD Analyzer")
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_column_width=True)
role = st.sidebar.radio("Profil", ["Utilisateur chantier / AMO", "Admin (index & docs)"])

# ----------------- Panneau Admin -----------------
def render_admin():
    st.title("🛠️ Administration — Corpus & Index")
    st.caption("Réservé aux opérations d’ingestion et de (ré)indexation. Les utilisateurs finaux n’y ont pas accès.")

    with st.expander("Connexion (démo)", expanded=not ss.admin_ok):
        pwd = st.text_input("Mot de passe admin (démo)", type="password", placeholder="••••••••")
        colA, colB = st.columns([1,3])
        with colA:
            if st.button("Se connecter"):
                ss.admin_ok = (pwd == "admin")  # ⚠️ Démo, à remplacer par authentification réelle
                if not ss.admin_ok:
                    st.toast("Mot de passe incorrect", icon="❌")
        with colB:
            st.info("Mot de passe de démonstration : **admin** (remplacer par streamlit-authenticator / SSO).")

    if not ss.admin_ok:
        st.stop()

    st.subheader("📁 Documents du corpus")
    uploaded = st.file_uploader("Téléverser des PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded:
        ss.docs = list({*ss.docs, *[f.name for f in uploaded]})  # maquette : on ne lit pas, on stocke les noms
        st.success(f"{len(uploaded)} document(s) ajouté(s).")

    if ss.docs:
        st.write("Documents présents :")
        for i, n in enumerate(sorted(ss.docs), 1):
            st.markdown(f"- {i}. {n}")
    else:
        st.warning("Aucun document pour l’instant.")

    st.markdown("---")
    st.subheader("⚙️ Indexation")
    with st.expander("Paramètres avancés (pour experts)"):
        st.number_input(
            "Top‑K par défaut (maquette, tests internes)",
            min_value=1,
            max_value=50,
            value=5,
            help="N’affecte pas l’UI Utilisateur. Servira plus tard au RAG.",
        )
        st.caption("Quand le RAG sera branché : splitter, tailles de chunk, overlap, modèle d’embeddings, stockage FAISS, etc.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Construire l’index (mock)"):
            with st.status("", expanded=False) as s:
                st.write("Étapes simulées: extraction → chunking → embeddings → FAISS")
                ss.last_index_at = dt.datetime.now().isoformat(timespec="seconds")
                s.update(label="Index prêt (maquette)", state="complete")
                st.toast("Index construit", icon="✅")
    with col2:
        if st.button("Mettre à jour l’index (mock)"):
            with st.status("", expanded=False) as s:
                st.write("Mise à jour simulée: détection delta, réindexation partielle")
                ss.last_index_at = dt.datetime.now().isoformat(timespec="seconds")
                s.update(label="Mise à jour terminée (maquette)", state="complete")
                st.toast("Index mis à jour", icon="🔄")

    st.markdown("---")
    st.caption("Conseil: séparer cette page dans /pages/01_Admin.py et activer une authentification réelle.")

# ----------------- Panneau Utilisateur -----------------
def hero_and_kpis():
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("### ICPE‑VRD Analyzer")
        st.caption("Analyse réglementaire assistée • Démarches • Criticité • Aide à la rédaction")
    with c2:
        k1, k2, k3 = st.columns(3, gap="small")
        with k1:
            st.metric("Docs", len(ss.docs))
        with k2:
            st.metric("Dernière indexation", ss.last_index_at or "—")
        with k3:
            st.metric("Version", "v0.3.1‑maquette")
    st.markdown("---")

def suggestions_ui():
    st.write("Suggestions :")
    s1, s2, s3 = st.columns(3)
    if s1.button("Impact déplacement de bassin ?", use_container_width=True):
        ss.prefill_query = "Déplacement du bassin de rétention de 20 m vers l’ouest… Impacts ICPE ? Démarches ?"
    if s2.button("Seuils rubrique 1510 entrepôt ?", use_container_width=True):
        ss.prefill_query = "Quels sont les seuils applicables rubrique 1510 pour un entrepôt logistique de 50 000 m² ?"
    if s3.button("Voie pompiers : exigences ?", use_container_width=True):
        ss.prefill_query = "Quelles sont les exigences minimales pour la voie pompiers et compatibilités ICPE ?"

def render_user():
    hero_and_kpis()

    # Contexte (facultatif)
    with st.container(border=True):
        st.subheader("Contexte chantier (facultatif)")
        c1, c2, c3 = st.columns([2, 2, 2])
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
                    "Terrassement / Déblai‑Remblai",
                    "Autre",
                ],
                index=1,
