import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader

def load_documents(path: str) -> List:
    """
    Load PDF documents from either:
      - A folder containing multiple PDFs, or
      - A single PDF file path (e.g., from Streamlit upload)
    Returns a list of LangChain Document objects.
    """
    docs = []

    # --- Case 1: path is a folder ---
    if os.path.isdir(path):
        folder = Path(path)
        pdf_files = list(folder.glob("*.pdf"))
        if not pdf_files:
            print(f"⚠️ No PDF files found in {path}")
            return []
        for pdf in pdf_files:
            loader = PyPDFLoader(str(pdf))
            docs.extend(loader.load())
        print(f"✅ Loaded {len(pdf_files)} PDF(s), {len(docs)} pages total")

    # --- Case 2: path is a single PDF file ---
    elif os.path.isfile(path) and path.endswith(".pdf"):
        loader = PyPDFLoader(path)
        docs = loader.load()
        print(f"✅ Loaded 1 PDF, {len(docs)} pages total")

    # --- Case 3: invalid path ---
    else:
        print(f"⚠️ Invalid path or no PDFs found: {path}")
        return []

    return docs