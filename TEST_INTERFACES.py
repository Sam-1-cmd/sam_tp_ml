# pip install streamlit sentence-transformers faiss-cpu pypdf reportlab
import os, glob, io, datetime
import streamlit as st

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

st.set_page_config(page_title="ICPE-VRD Analyzer", layout="wide")

# ---- Sidebar ----
st.sidebar.image("logo.png", use_column_width=True) if os.path.exists("logo.png") else None
mode = st.sidebar.radio("Mode", ["Local (FAISS)", "Atlas Data API"], index=0)
uploaded = st.sidebar.file_uploader("Téléversez des PDF", type="pdf", accept_multiple_files=True)
rubrique = st.sidebar.multiselect("Rubrique", ["1510","Autre"])
source_filter = st.sidebar.multiselect("Source", ["Arrêté","Guide","Notice"])
st.sidebar.markdown("---")
build = st.sidebar.button("Construire l’index")

# ---- Helpers ----
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = "faiss_index"

@st.cache_resource(show_spinner=False)
def load_embedder():
    return HuggingFaceEmbeddings(model_name=EMB_MODEL)

def load_docs_from_files(files):
    docs = []
    for f in files:
        tmp = f.name
        with open(tmp, "wb") as out: out.write(f.read())
        for d in PyPDFLoader(tmp).load():
            # ajoute des métadonnées utiles (ex: déduire la source/simple mapping)
            d.metadata.update({"source": os.path.splitext(f.name)[0]})
            docs.append(d)
        os.remove(tmp)
    return docs

def split_docs(docs, size=1000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    return splitter.split_documents(docs)

@st.cache_resource(show_spinner=False)
def build_index(chunks):
    emb = load_embedder()
    store = FAISS.from_documents(chunks, emb)
    store.save_local(INDEX_DIR)
    return INDEX_DIR

def apply_filters(docs):
    if rubrique:
        docs = [d for d in docs if d.metadata.get("rubrique") in rubrique]
    if source_filter:
        docs = [d for d in docs if d.metadata.get("source_type") in source_filter]
    return docs

def load_or_build_store():
    emb = load_embedder()
    if os.path.isdir(INDEX_DIR):
        return FAISS.load_local(INDEX_DIR, emb, allow_dangerous_deserialization=True)
    return None

def export_pdf(extraits, query):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    y = 800
    c.setFont("Helvetica-Bold", 12); c.drawString(40, 820, "ICPE-VRD — Fiche d’analyse")
    c.setFont("Helvetica", 10); c.drawString(40, 805, f"Requête : {query}")
    for i, d in enumerate(extraits, 1):
        txt = (d.page_content[:900] + "…").replace("\n"," ")
        c.drawString(40, y, f"{i}. {d.metadata.get('source','?')} p.{d.metadata.get('page','?')}")
        y -= 14
        for line in [txt[j:j+100] for j in range(0, len(txt), 100)]:
            c.drawString(40, y, line); y -= 12
            if y < 80: c.showPage(); y = 800
    c.showPage(); c.save(); buf.seek(0)
    return buf

# ---- Main ----
st.title("🔎 ICPE-VRD Analyzer (RAG)")
st.caption(f"Index: {INDEX_DIR if os.path.isdir(INDEX_DIR) else '—'} • {datetime.date.today()}")

col1, col2 = st.columns([3,1])
with col1:
    query = st.text_area("Décrivez la modification VRD à analyser", height=120,
                         placeholder="Ex: Déplacement d’un bassin de rétention vers l’ouest…")
with col2:
    k = st.number_input("Top-K extraits", 1, 20, 5)

# Construire/mettre à jour l’index
if build and uploaded:
    with st.spinner("Extraction, découpage, vectorisation…"):
        docs = load_docs_from_files(uploaded)
        chunks = split_docs(docs)
        build_index(chunks)
    st.success("Index construit ✅")

store = load_or_build_store()
analyze = st.button("Analyser", type="primary")

if analyze:
    if not store:
        st.warning("Veuillez d’abord construire l’index (sidebar).")
    elif not query.strip():
        st.warning("Saisissez une requête.")
    else:
        with st.spinner("Recherche des extraits pertinents…"):
            res = store.similarity_search(query, k=k)
        tab1, tab2, tab3, tab4 = st.tabs(["📚 Extraits", "🧠 Analyse (GPT)", "📄 Démarche admin", "⚠️ Criticité"])
        with tab1:
            for d in res:
                with st.expander(f"{d.metadata.get('source','?')} — page {d.metadata.get('page','?')}"):
                    st.write(d.page_content)
                    st.caption(f"Version: {d.metadata.get('version','n/a')} • is_current={d.metadata.get('is_current', True)}")
        with tab2:
            st.info("Optionnel: appeler un LLM pour synthétiser. (désactivé en mode local)")
        with tab3:
            st.write("Règles métiers pour PAC / modif. d’autorisation, etc. (à compléter).")
        with tab4:
            st.write("Heuristiques de criticité environnementale (à compléter).")

        pdf_buf = export_pdf(res, query)
        st.download_button("📄 Télécharger la fiche PDF", data=pdf_buf, file_name="analyse_icpe_vrd.pdf", mime="application/pdf")
