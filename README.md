# 🏥 Bilingual Health Education Chatbot

A **local, CPU-friendly chatbot** that helps patients understand clinical terms in **plain English** and **Traditional Chinese (Taiwan)**.  
It uses **retrieval-augmented generation (RAG)** with hospital-approved patient education materials (e.g., CDC, MOHW/HPA leaflets) to give **accurate, grounded, and bilingual answers**.

---

## ✨ Features
- 🔍 **Retrieval-Augmented Generation (RAG)** – answers are based only on vetted patient education PDFs.  
- 🌐 **Bilingual output** – English and Traditional Chinese explanations in one response.  
- ✅ **Grounded answers** – always cites hospital-approved sources at the end.  
- 💻 **Runs locally** – no paid APIs or cloud services required. Works on CPU.  
- 🧾 **Human-friendly format** – answers look like:

Answer:
English: "PrEP is highly effective ..."
Mandarin: "暴露前預防性投藥（PrEP）在正確規律服用時..."
Sources:
1: cdc-prep-leaflet.pdf (chunk 0)
2: cdc-prep-guide.pdf (chunk 1)


---

## Project Structure
.
├── app_chat.py # Flask app (main entry)
├── rag_core.py # RAG utilities (FAISS index, embedding, chunking)
├── prompts.py # System prompt + templates
├── ingest.py # One-time script to index PDFs
├── requirements.txt # Python dependencies
├── templates/
│ └── chat.html # Simple chat UI
├── static/
│ └── style.css # Basic CSS styling
└── data/
└── leaflets/ # Place hospital-approved patient PDFs here


---

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/health-education-chatbot.git
cd health-education-chatbot

2. Create virtual environment
python -m venv llmenv-chat
source llmenv-chat/bin/activate   # Linux/Mac
.\llmenv-chat\Scripts\activate    # Windows

3. Install dependencies
pip install -r requirements.txt

Data Preparation

Download patient education PDFs (CDC, NHS, Taiwan HPA).

Place them into:
data/leaflets/

3. Build the FAISS index:
python ingest.py

Run the Chatbot

Start the Flask server:
python app_chat.py

Open http://127.0.0.1:5000
 in your browser.
You can now ask questions like:

“What is PrEP and how effective is it?”


Notes on Use

This chatbot is for educational purposes only.
It is not a diagnostic tool and should not replace medical advice.
Always consult healthcare professionals for personal medical concerns.

Please cite the original CDC / NHS / MOHW-HPA sources when redistributing patient education content.



