import os, re
from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from rag_core import RAGIndex  # uses your existing FAISS index/load
from prompts import SYSTEM_PROMPT, USER_TEMPLATE

device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------- LLM ----------
LLM_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tok = AutoTokenizer.from_pretrained(LLM_NAME)
if tok.pad_token_id is None and tok.eos_token_id is not None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(LLM_NAME).to(device).eval()

# ---------- RAG ----------
idx = RAGIndex()
idx.load("store")  # assumes ingest.py already built store/faiss.index + meta.pkl

# ---------- Hygiene helpers ----------
JUNK_BLOCKS = re.compile(
    r"(?:^|\n)\s*(Sources?|Snippets?|Roles?)\s*:.*$",
    re.IGNORECASE | re.DOTALL,
)

def sanitize_user(q: str) -> str:
    """Strip pasted 'Sources:', 'Snippets:', 'Roles:' etc. from the user message."""
    return JUNK_BLOCKS.sub("", q or "").strip()

def is_prep_query(q: str) -> bool:
    ql = (q or "").lower()
    return any(k in ql for k in ["prep", "pre-exposure", "pre exposure"])

def topical_filter(results, query):
    """If asking about PrEP, keep only filenames likely about PrEP."""
    if not is_prep_query(query):
        return results
    keep = []
    for (text, meta, score) in results:
        name = meta.get("source", "").lower()
        if any(k in name for k in ["prep", "pre-exposure", "preexposure"]):
            keep.append((text, meta, score))
    return keep

def score_floor(results, min_ip=0.25):
    """Cosine≈inner-product since embeddings are normalized."""
    return [(t, m, s) for (t, m, s) in results if s >= min_ip]

def format_contexts(results):
    lines = []
    for i, (txt, meta, score) in enumerate(results, start=1):
        src = f"[Source {i}] {meta['source']} (chunk {meta['chunk_id']})"
        excerpt = " ".join((txt or "").split())
        if len(excerpt) > 650:
            excerpt = excerpt[:650] + "..."
        lines.append(f"{src}\n{excerpt}\n")
    return "\n".join(lines)

def build_prompt(question, mode, results):
    contexts = format_contexts(results)
    return f"<|system|>\n{SYSTEM_PROMPT}\n<|user|>\n{USER_TEMPLATE.format(question=question, contexts=contexts, mode=mode)}\n<|assistant|>\n"

def generate_answer(prompt, max_new_tokens=420):
    enc = tok(prompt, return_tensors="pt").to(device)
    out = model.generate(
        **enc,
        max_new_tokens=max_new_tokens,
        temperature=0.2,          # tighter
        top_p=0.9,
        no_repeat_ngram_size=5,   # reduce repeats
        repetition_penalty=1.05,
        pad_token_id=tok.pad_token_id,
        eos_token_id=tok.eos_token_id,
    )
    new_tokens = out[0][enc["input_ids"].shape[-1]:]
    text = tok.decode(new_tokens, skip_special_tokens=True).strip()
    # remove stray code fences if any
    text = text.replace("```json", "```").strip("` \n")
    return text

# ---------- Flask ----------
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    raw_q = (data.get("message") or "").strip()
    mode = (data.get("mode") or "both").lower()  # en | zh | both

    q = sanitize_user(raw_q)
    if not q:
        return jsonify({"answer": "Please enter a question.", "sources": []})

    # Retrieve top-k, then guard
    initial = idx.search(q, top_k=12)           # [(text, meta, score), ...]
    topical = topical_filter(initial, q)
    filtered = score_floor(topical, min_ip=0.25)
    results = filtered[:4]

    if not results:
        return jsonify({
            "answer": "I don’t have source material on that topic yet. Please consult your care team.",
            "sources": []
        })

    prompt = build_prompt(q, mode, results)
    answer = generate_answer(prompt)

    # Build sources for UI panel (independent of the model’s text)
    sources = []
    for i, (_, meta, _) in enumerate(results, start=1):
        sources.append({
            "label": f"Source {i}",
            "file": meta["source"],
            "chunk": meta["chunk_id"]
        })

    return jsonify({"answer": answer, "sources": sources})

if __name__ == "__main__":
    # 1) python ingest.py   (after placing vetted PDFs in data/leaflets/)
    # 2) python app_chat.py
    app.run(debug=True)
