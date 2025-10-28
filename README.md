#  Bilingual Health Education Chatbot

A **local, CPU-friendly chatbot** that helps patients understand clinical terms in **plain English** and **Traditional Chinese (Taiwan)**.  
It uses **retrieval-augmented generation (RAG)** with hospital-approved patient education materials (e.g., CDC, MOHW/HPA leaflets) to give **accurate, grounded, and bilingual answers**.

---

##  Features
-  **Retrieval-Augmented Generation (RAG)** – answers are based only on vetted patient education PDFs.  
-  **Bilingual output** – English and Traditional Chinese explanations in one response.  
-  **Grounded answers** – always cites hospital-approved sources at the end.  
-  **Runs locally** – no paid APIs or cloud services required. Works on CPU.  
-  **Human-friendly format** – answers look like:

Answer:
English: "PrEP is highly effective ..."
Mandarin: "暴露前預防性投藥（PrEP）在正確規律服用時..."
Sources:
1: cdc-prep-leaflet.pdf (chunk 0)
2: cdc-prep-guide.pdf (chunk 1)

```bash
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

```
---

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/health-education-chatbot.git
cd health-education-chatbot
```
### 2. Create virtual environment
```bash
python -m venv llmenv-chat
source llmenv-chat/bin/activate   # Linux/Mac
.\llmenv-chat\Scripts\activate    # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Data Preparation

## 1. Download patient education PDFs (CDC, NHS, Taiwan HPA).

## 2. Place them into:
```bash
data/leaflets/
```
## 3. Build the FAISS index:
```bash
python ingest.py
```
### 5. Run the Chatbot

Start the Flask server:
```bash
python app_chat.py
```
Open http://127.0.0.1:5000 in your browser.
You can now ask questions like:

-  **“What is PrEP and how effective is it?”

<img width="943" height="783" alt="Health education chatbot 0" src="https://github.com/user-attachments/assets/345a03fe-7bac-4ae7-87a7-14bb4f7f764e" />
<img width="1058" height="840" alt="Health education chatbot 1" src="https://github.com/user-attachments/assets/cb6ff618-6ec3-4af6-9f42-ab2f66000338" />
<img width="1051" height="855" alt="Health education chatbot 2" src="https://github.com/user-attachments/assets/d63d6390-8e15-4051-a6fb-43b051247deb" />
<img width="969" height="829" alt="Health education chatbot 3" src="https://github.com/user-attachments/assets/c3853625-b6bd-45c3-8378-c0b84e77cdfd" />
<img width="960" height="821" alt="Health education chatbot 4" src="https://github.com/user-attachments/assets/6d4b063f-d7e9-4041-b91b-7abff9e347c6" />


Notes on Use

-  **This chatbot is for educational purposes only.
-  **It is not a diagnostic tool and should not replace medical advice.
-  **Always consult healthcare professionals for personal medical concerns.

Please cite the original CDC / NHS / MOHW-HPA sources when redistributing patient education content.



