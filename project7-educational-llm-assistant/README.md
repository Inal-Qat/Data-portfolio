# 🎓 Educational LLM Assistant — RAG-Powered Learning & Evaluation Prototype  
*A Master-Level Demo of AI-Assisted Tutoring, Feedback & Document Understanding*

**Author:** Yanal Kat  
**Tech Stack:** Python · LangChain (0.2.x) · FAISS · Sentence-Transformers · HuggingFace · Streamlit · UMAP

---

## 📘 Overview

This project implements a Retrieval-Augmented Generation (RAG) educational assistant capable of:

- Processing and indexing educational PDF documents  
- Answering student-style questions using an LLM  
- Evaluating responses based on Bloom’s Taxonomy  
- Generating structured tutor-style feedback  
- Visualizing document clusters using UMAP embeddings  
- Providing an interactive learning interface through Streamlit  

The goal of this prototype is to demonstrate how AI can support educators, enhance feedback quality, and reduce grading time.

---

## 🧠 Features

### 🔍 Intelligent Document Understanding (RAG)
- PDF parsing  
- Recursive text chunking  
- Embedding generation with Sentence-Transformers  
- FAISS vector database for efficient retrieval  

### 💬 LLM Answer Generation
- Custom HFLLM wrapper for lightweight HuggingFace inference  

### 🎓 Bloom’s Taxonomy Evaluation
Automatically classifies generated answers into cognitive levels:  
Remember · Understand · Apply · Analyze · Evaluate · Create  
Provides a clear and human-readable evaluation summary.

### 🎨 Embedding Visualization
- UMAP-based 2D semantic visualization of the processed documents  

### 🌐 Streamlit Application Modes

**Isolated Mode**  
Upload and process a single PDF temporarily.

**Library Mode**  
Load all PDFs inside the data/ directory into a persistent knowledge base.

---

## 📁 Project Structure

project7-educational-llm-assistant/  
│  
├── app.py — Streamlit UI  
├── README.md  
├── environment.yml — Conda environment configuration  
├── requirements.txt  
│  
├── notebook/  
│   └── project7-slm-app.ipynb  
│  
├── data/ — PDF files for Library Mode  
│  
└── src/  
    ├── loader.py — PDF loading and parsing  
    ├── rag_pipeline.py — Embeddings, retrieval, HFLLM wrapper  
    ├── evaluation.py — Bloom’s Taxonomy evaluator  
    └── visualization.py — UMAP visualizations  

---

## 📸 Screenshots

*(Make sure your screenshot filenames contain no spaces.)*

Example image references:

![Isolated Mode - Main](screenshots/app_isolated_main.png)  
![Isolated Mode - Result](screenshots/app_isolated_result.png)  
![Library Mode - Main](screenshots/app_library_main.png)  
![Library Mode - Result 1](screenshots/app_library_result1.png)  
![Library Mode - Result 2](screenshots/app_library_result2.png)

---

## 🔮 Future Enhancements

- BLEU and ROUGE scoring for automated evaluation  
- Higher-quality evaluator models (GPT-4o, Claude, DeepSeek, etc.)  
- Tutor and student accounts for a complete classroom workflow  
- Dashboards and analytics for student performance tracking  
- RAG chunk citations showing which document segments were used  

---

## License  
MIT License