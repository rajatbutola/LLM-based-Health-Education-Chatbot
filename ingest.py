from rag_core import load_pdfs_to_chunks, RAGIndex

PDF_DIR = "data/leaflets"
STORE_DIR = "store"

if __name__ == "__main__":
    texts, metas = load_pdfs_to_chunks(PDF_DIR)
    if not texts:
        raise SystemExit(f"No PDFs found in {PDF_DIR}. Put vetted patient leaflets there.")
    print(f"Loaded {len(texts)} chunks from PDFs.")
    idx = RAGIndex()
    idx.build(texts, metas)
    idx.save(STORE_DIR)
    print(f"Index saved to {STORE_DIR}/")
