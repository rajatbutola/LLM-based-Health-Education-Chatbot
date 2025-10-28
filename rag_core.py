import os, pickle, math
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# -------- Chunking --------
def chunk_text(text, chunk_size=800, overlap=120):
    tokens = text.split()
    out = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        out.append(" ".join(chunk))
        i += (chunk_size - overlap)
    return out

def load_pdfs_to_chunks(pdf_dir):
    docs, metas = [], []
    for name in os.listdir(pdf_dir):
        if not name.lower().endswith(".pdf"):
            continue
        path = os.path.join(pdf_dir, name)
        try:
            reader = PdfReader(path)
            pages = [p.extract_text() or "" for p in reader.pages]
            full = "\n".join(pages)
            for j, chunk in enumerate(chunk_text(full)):
                docs.append(chunk)
                metas.append({"source": name, "chunk_id": j})
        except Exception as e:
            print(f"[WARN] Failed {name}: {e}")
    return docs, metas

# -------- Indexing --------
class RAGIndex:
    def __init__(self, embed_model_name="intfloat/multilingual-e5-small"):
        self.model = SentenceTransformer(embed_model_name)
        self.index = None
        self.docs = None
        self.metas = None

    def build(self, texts, metas):
        self.docs = texts
        self.metas = metas
        # E5 expects "query: ..." or "passage: ..." prefix
        emb = self.model.encode([f"passage: {t}" for t in texts], batch_size=64, show_progress_bar=True, normalize_embeddings=True)
        dim = emb.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # cosine via normalized vectors → inner product
        self.index.add(emb.astype(np.float32))

    def save(self, store_dir):
        os.makedirs(store_dir, exist_ok=True)
        faiss.write_index(self.index, os.path.join(store_dir, "faiss.index"))
        with open(os.path.join(store_dir, "meta.pkl"), "wb") as f:
            pickle.dump({"docs": self.docs, "metas": self.metas}, f)

    def load(self, store_dir):
        self.index = faiss.read_index(os.path.join(store_dir, "faiss.index"))
        with open(os.path.join(store_dir, "meta.pkl"), "rb") as f:
            data = pickle.load(f)
            self.docs, self.metas = data["docs"], data["metas"]

    def search(self, query, top_k=4):
        q_emb = self.model.encode([f"query: {query}"], normalize_embeddings=True)
        D, I = self.index.search(q_emb.astype(np.float32), top_k)
        items = []
        for idx, score in zip(I[0].tolist(), D[0].tolist()):
            if idx == -1: 
                continue
            items.append((self.docs[idx], self.metas[idx], float(score)))
        return items
