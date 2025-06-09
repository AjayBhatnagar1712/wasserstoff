import os
import streamlit as st
from backend.document_loader import load_document, chunk_text
from backend.vector_store import query_documents, add_chunks
from backend.summarizer import summarize_chunks

st.set_page_config(page_title="Wasserstoff AI Document Chatbot", layout="wide")
st.title("📄 Wasserstoff AI Document Chatbot")

uploaded_files = st.file_uploader("Upload PDFs or Images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
query = st.text_input("❓ Ask a question")

# Store responses
if 'history' not in st.session_state:
    st.session_state['history'] = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join("docs", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        doc_id = uploaded_file.name
        chunks = chunk_text(load_document(file_path))
        add_chunks(chunks, doc_id)

        st.success(f"✅ Extracted {len(chunks)} chunks from {uploaded_file.name}")

if query:
    st.subheader("🔍 AI Answer")
    results = query_documents(query)

    if results:
        results.sort(key=lambda r: r['similarity'], reverse=True)

        # Theme summarization
        top_chunks = results[:5]
        theme_summary = summarize_chunks(top_chunks)

        st.subheader("🧠 AI Theme Summary")
        st.success(theme_summary)

        # Best answer chunk
        best = results[0]
        answer = best['document']
        st.markdown(f"**📌 AI Answer from best match**\n\n{answer}")

        # 📥 Downloadable answer
        st.download_button("📥 Download Answer", answer, file_name="answer.txt")

        # 📚 Sources (Tabular view)
        st.subheader("📚 Sources (Top Matches)")
        import pandas as pd
        rows = []
        for r in results[:5]:
            meta = r['metadata']
            rows.append({
                "Document": meta.get("doc_id", "?"),
                "Chunk": meta.get("chunk_index", "?"),
                "Page": meta.get("page", "?"),
                "Similarity": round(r['similarity'], 4),
                "Excerpt": r['document'][:150] + "..."
            })
        df = pd.DataFrame(rows)
        st.dataframe(df)
    else:
        st.warning("No results found. Try a different question.")
