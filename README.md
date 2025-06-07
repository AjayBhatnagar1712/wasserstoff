# 🧠 Wasserstoff AI Internship Task - Document Research Chatbot

This project is a document research & theme identification chatbot, built for the Wasserstoff Gen-AI Internship.

---

## 🚀 Features

- ✅ Upload PDFs or scanned images (OCR-powered)
- ✅ Extract and chunk document content
- ✅ Store in a vector database (ChromaDB)
- ✅ Ask questions from uploaded docs
- ✅ Theme summarization using Transformers
- ✅ Accurate citations with chunk metadata
- ✅ Tabular view of top document matches
- ✅ Downloadable answers
- ✅ Simple Streamlit UI

---

## 📦 Tech Stack

| Tool         | Purpose                        |
|--------------|--------------------------------|
| Python       | Core logic                     |
| PyMuPDF / Tesseract | Text + OCR extraction   |
| ChromaDB     | Vector store                   |
| Sentence-Transformers | Embedding model       |
| Transformers | Theme summarization (offline) |
| Streamlit    | Web UI                         |

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/ajay-bhatnagar/wasserstoff/AiInternTask.git
cd AiInternTask
pip install -r requirements.txt
streamlit run app.py
