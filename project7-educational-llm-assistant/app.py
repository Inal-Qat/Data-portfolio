import os, sys, tempfile
import streamlit as st

# --- Ensure /src is discoverable ---
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from loader import load_documents
from rag_pipeline import build_vector_db, create_qa_chain
from evaluation import create_bloom_evaluator, format_evaluation_output
from visualization import visualize_vector_space


# --- App title ---
st.title("🎓 Educational LLM Assistant (RAG Prototype)")
st.write("Upload a PDF and ask questions — the model will answer and evaluate using Bloom’s Taxonomy.")

# --- Hugging Face Token ---
if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
    token = st.text_input("🔑 Enter your Hugging Face API Token:", type="password")
    if token:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = token


# =============================
# 🔧 MODE SWITCH
# =============================
st.sidebar.header("⚙️ Settings")
use_library = st.sidebar.toggle(
    "📚 Library Mode",
    help="Index and question ALL PDFs stored in the /data folder."
)


# =============================
# 📚 LIBRARY MODE
# =============================
if use_library:
    st.info("Using **Library Mode** — all PDFs in the `data/` folder will be indexed.")

    data_path = os.path.join(os.path.dirname(__file__), "data")
    docs = load_documents(data_path)

    if not docs:
        st.error("❌ No PDFs found in the data/ folder.")
    else:
        with st.spinner("⚙️ Building vector database..."):
            vector_db = build_vector_db(docs)
            qa = create_qa_chain(vector_db)
            bloom_eval = create_bloom_evaluator()

        st.success("✅ Library loaded. You can now ask a question.")

        # --- UMAP Visualization Toggle
        st.subheader("📊 Semantic Map of Your Library")
        if st.checkbox("Show UMAP Visualization"):
            fig = visualize_vector_space(vector_db, "Semantic Clusters of Library Chunks")
            st.pyplot(fig)

        # --- Ask Question
        question = st.text_input("💬 Ask a question about your library:")
        if question:
            with st.spinner("🤔 Thinking... generating answer and evaluation..."):
                response = qa.invoke({"question": question})

                context_docs = qa.retriever.invoke(question)
                context = " ".join(doc.page_content for doc in context_docs[:2])

                answer = response["result"]
                result = bloom_eval.invoke({"context": context, "answer": answer})

            st.markdown(format_evaluation_output(question, answer, result))


# =============================
# 📄 ISOLATED MODE (upload 1 file)
# =============================
else:
    st.info("Using **Isolated Mode** — upload a single PDF for temporary analysis.")
    uploaded_file = st.file_uploader("📄 Upload a PDF", type="pdf")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("⚙️ Extracting text..."):
            docs = load_documents(os.path.dirname(tmp_path))

        if not docs:
            st.error("❌ Could not extract text from this PDF. Please try another file.")
            os.remove(tmp_path)

        else:
            with st.spinner("⚙️ Building vector database..."):
                vector_db = build_vector_db(docs)
                qa = create_qa_chain(vector_db)
                bloom_eval = create_bloom_evaluator()

            st.success("✅ File processed! You can now ask a question.")

            question = st.text_input("💬 Ask a question about this document:")
            if question:
                with st.spinner("🤔 Thinking..."):
                    response = qa.invoke({"question": question})

                    context_docs = qa.retriever.invoke(question)
                    context = " ".join(doc.page_content for doc in context_docs[:2])

                    answer = response["result"]
                    result = bloom_eval.invoke({"context": context, "answer": answer})

                st.markdown(format_evaluation_output(question, answer, result))

        # --- Cleanup temporary file ---
        if os.path.exists(tmp_path):
            os.remove(tmp_path)