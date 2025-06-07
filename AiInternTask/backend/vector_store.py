from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from chromadb import Client
import uuid
import streamlit as st
import re

# Initialize ChromaDB in-memory
client = Client(Settings(anonymized_telemetry=False))
collection = client.create_collection(name="wasserstoff_docs")

# Load sentence embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Extract contact info from text using regex
def extract_contact_info(text):
    # Match emails
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

    # Try to extract name from formats like:
    # - Contact: Name – email
    # - Name – email
    name_match = re.search(r"(?:(?:Contact:|By|From)?\s*)?([A-Z][a-z]+\s[A-Z][a-z]+)\s[–-]\s", text)

    name = name_match.group(1) if name_match else None
    email = email_match.group() if email_match else None

    if name or email:
        return f"📬 Contact Person: {name if name else 'N/A'}\n📧 Email: {email if email else 'N/A'}"
    return None


# ✅ Add all chunks of a document to the vector store
def add_chunks(chunks, doc_id):
    for i, chunk in enumerate(chunks):
        metadata = {
            "doc_id": doc_id,
            "chunk_index": i
        }
        collection.add(
            documents=[chunk],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )

# ✅ Query the documents and show most relevant results
def query_documents(question, top_k=5):
    question_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    if not results['documents'][0]:
        return []

    top_results = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        top_results.append({
            "document": doc.strip(),
            "metadata": meta,
            "similarity": dist
        })

    return top_results
