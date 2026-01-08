# 💼 Data Science & AI Portfolio  
**Author:** Yanal Kat (Inal-Qat)  
**MSc Business Information Systems | Applied AI, Data Science & Machine Learning**  

A curated portfolio of end-to-end Data & AI projects demonstrating strong analytical thinking, modern machine learning practices, and the design of production-oriented, agentic AI systems.

The portfolio spans classical data science, forecasting, NLP, RAG, and LLM-based agent services designed for real-world business integration.

---

## 🧩 Project Portfolio

| # | Project | Description | Key Skills & Tools |
|:-:|:--------|:------------|:------------------|
| 1 | [Production-Ready GenAI Agent API](./project1-genai-agent-api) | Internal GenAI agent service exposed via a REST API. Implements agent-based decision logic, tool routing (calculator, time), strict request/response validation, authentication, observability (metrics, logging), and Dockerized deployment. Designed as an AI backend service for integration into business systems. | `FastAPI`, `Pydantic`, `Docker`, `LLM Agents`, `Agent Architecture`, `API Design`, `Observability`, `Groq` |
| 2 | [Snowflake AI Analyst Agent](./project2-snowflake-ai-analyst-agent) | AI-powered analytics agent that translates natural language questions into safe, schema-aware SQL, executes them against Snowflake sample data, and returns data-backed answers via a Streamlit chat interface. Built with explicit agent state, guardrails, and transparent execution. | `LangGraph`, `LLM Agents`, `Snowflake`, `SQL`, `Streamlit`, `Pydantic`, `Groq`, `Agent Orchestration` |
| 3 | [Agentic Customer Analytics Assistant](./project3-agentic-customer-analytics-assistant) | End-to-end intelligent analytics system combining classical ML with LangChain tools and LangGraph workflows. Performs customer analysis, insight generation, and tool-driven reasoning through a Streamlit UI. | `Machine Learning`, `LangChain`, `LangGraph`, `Groq`, `Agents`, `Feature Engineering`, `Streamlit`, `scikit-learn` |
| 4 | [Educational LLM Assistant (RAG Application)](./project4-educational-llm-assistant) | Retrieval-Augmented Generation system for processing PDFs and answering educational questions using embeddings, vector search, and LLM-based evaluation. Includes UMAP visualization and Streamlit interface. | `RAG`, `LangChain`, `FAISS`, `Sentence-Transformers`, `HuggingFace`, `Streamlit`, `UMAP` |
| 5 | [Predictive Maintenance](./project5-predictive-maintenance) | Machine learning pipeline predicting potential machine failures from sensor data, including feature engineering, model benchmarking, and explainability. | `RandomForest`, `XGBoost`, `EDA`, `Feature Engineering`, `scikit-learn` |
| 6 | [Sales Forecasting](./project6-sales-forecasting) | Demand forecasting pipeline estimating product sales using regression models, time-series preprocessing, and feature importance analysis. | `Time Series`, `XGBoost`, `RandomForestRegressor`, `EDA`, `Visualization` |
| 7 | [Customer Churn Prediction](./project7-customer-churn) | Supervised ML model predicting telecom customer churn using demographics, usage metrics, and service-level features. | `Logistic Regression`, `Feature Engineering`, `scikit-learn` |
| 8 | [Customer Review Sentiment Analysis](./project8-customer-review-sentiment) | NLP classification pipeline analyzing customer reviews and classifying sentiment using traditional text-processing techniques. | `NLP`, `TF-IDF`, `Logistic Regression`, `NLTK` |
| 9 | [Sales & Profit Dashboard (Power BI)](./project9-powerbi-dashboard) | Interactive executive dashboard exploring sales, profit, and regional performance using the Superstore dataset. | `Power BI`, `DAX`, `Data Visualization`, `Business Intelligence` |
| 10 | [Expenses Analysis](./project10-expenses-analysis) | Exploratory data analysis of personal expenses with trend visualization and insights into spending behavior. | `Python`, `Pandas`, `Matplotlib`, `Seaborn` |

---

## 🧠 Core Competencies

- Data Cleaning, Wrangling & Visualization  
- Predictive Modeling (Classification & Regression)  
- Time Series Forecasting  
- Natural Language Processing (NLP) 
- SQL & Analytical Querying  
- Retrieval-Augmented Generation (RAG)  
- **LLM Agents & Agentic System Design (LangChain / LangGraph)**  
- **API-First AI Services (FastAPI, Pydantic, Docker)**
- AI Safety, Guardrails & Observability 
- Dashboarding & Business Intelligence (Power BI)  
- Python (NumPy, pandas, scikit-learn, XGBoost, Matplotlib, Seaborn)  

---

## Portfolio Focus
This portfolio emphasizes applied, integration-ready AI — moving beyond notebooks and demos toward:

- AI services
- agent orchestration
- production constraints
- real-world business integration

---

## 🧰 Environment Setup
The portfolio uses a unified Anaconda environment for all Python-based projects.  
You can recreate it via:

```bash
conda env create -f environment.yml
conda activate data-portfolio
```
---
## Contact
* Email: ynal.qat@gmail.com
* LinkedIn: linkedin.com/in/yanal-kat-4677b229
* Location: Augsburg, Germany