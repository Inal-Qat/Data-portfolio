# 🎓 Educational LLM Assistant — RAG-Powered Learning & Evaluation Prototype  
*A Master-Level Demo of AI-Assisted Tutoring, Feedback & Document Understanding*

**Author:** Yanal Kat  
**Tech Stack:** Python · LangChain (0.2.x) · FAISS · Sentence-Transformers · HuggingFace · Streamlit · UMAP

---

## 📘 Overview

This project is a **Retrieval-Augmented Generation (RAG)** educational assistant capable of:

- Loading and processing educational PDF documents  
- Answering student-style questions using an LLM  
- Evaluating the response using **Bloom’s Taxonomy**  
- Producing structured tutor-style feedback  
- Visualizing document clusters using **UMAP embeddings**  
- Running interactively through a **Streamlit UI**

The prototype demonstrates how AI can support **educators, tutors, and students** by reducing grading time and improving the quality of instructional feedback.

---

## 🧠 Features

### 🔍 1. Intelligent Document Understanding (RAG)
- PDF parsing  
- Recursive chunking  
- Embeddings using `sentence-transformers`  
- FAISS vector store for similarity search  

### 💬 2. LLM Answer Generation
Includes a custom lightweight `HFLLM` wrapper for free-tier HuggingFace inference.

### 🎓 3. Bloom’s Taxonomy Evaluation  
Each answer is evaluated at one of the following cognitive levels:

> Remember · Understand · Apply · Analyze · Evaluate · Create 

The evaluator outputs a human-friendly feedback summary.

### 🎨 4. Vector Visualization
A UMAP-based plot provides a visual map of semantic document clusters.

### 🌐 5. Streamlit Web App
Two modes available:

#### **📄 Isolated Mode**
Process ONE uploaded PDF temporarily.

#### **📚 Library Mode**
Process *all* PDFs inside the `/data` folder as a reusable knowledge base.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Inal-Qat/project7-educational-llm-assistant.git
cd project7-educational-llm-assistant
```

### 2. Create Conda environment

``` bash 
conda env create -f environment.yml
conda activate slm-rag
```

### 3. Run the app 

```bash
streamlit run app.py
```

---

## Project Structure 

project7-educational-llm-assistant/
│
├── app.py                          # Streamlit UI
├── README.md
├── environment.yml                 # Conda environment
├── requirements.txt
│
├── notebook/
│   └── project7-slm-app.ipynb      # Full RAG + evaluation notebook
│
├── data/                           # PDF files (library mode)
│
└── src/
    ├── loader.py                   # PDF loader
    ├── rag_pipeline.py             # RAG pipeline + HFLLM wrapper
    ├── evaluation.py               # Bloom’s evaluator
    └── visualization.py            # UMAP plot

---

## Screenshots

![Streamlit UI](screenshots/app-isolated mode main.png)
![Streamlit UI](screenshots/app-isolated mode result.png)
![Streamlit UI](screenshots/app-library mode main.png)
![Streamlit UI](screenshots/app-library mode result 1.png)
![Streamlit UI](screenshots/app-library mode result 2.png)

---

## 🔮 Future Enhancements

### **🔷 BLEU / ROUGE automatic scoring**
Compare student answers to tutor-provided reference answers.

### **🔷 Higher-quality evaluator model**
Replacing the free-tier HuggingFace model with Claude, GPT-4o, DeepSeek, etc.

### **🔷 Tutor & Student Accounts**
Full classroom workflow:

- Tutors upload materials
- Students submit answers
- AI pre-evaluates
- Tutors give final grade

### **🔷 Dashboard & Analytics**
Track student performance over time.

### **🔷 Citations in Answers**
Show which PDF chunks were used as evidence.

---

## License 
MIT License 