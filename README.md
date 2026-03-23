# 💼 Applied AI & Agent Systems Portfolio  
**Author:** Yanal Kat (Inal-Qat)**  
**MSc Business Information Systems | Python Backend Developer | AI & Data Applications**

This portfolio showcases production-oriented AI systems that move beyond notebooks into deployable, integration-ready architectures.

It combines:

- Classical machine learning
- Retrieval-Augmented Generation (RAG)
- LLM-based agent systems
- MCP tool orchestration
- API-first AI services
- Workflow automation (n8n)
- Observability & containerized deployment

The focus is on building **enterprise-ready AI platforms** — not just models.

---

## 🧩 Project Portfolio

| # | Project | Description | Key Skills & Tools |
|:-:|:--------|:------------|:------------------|
| 1 | [MCP Tool Server + Agent Runtime Platform](./project01-mcp-tool-server-agent) | Production-style AI integration architecture separating MCP tool server from agent runtime. Includes HTTP/SSE transport, FastAPI API layer, Prometheus metrics, Docker multi-container setup, and n8n workflow orchestration. Demonstrates enterprise-ready agent platform design. | `MCP`, `FastAPI`, `Docker`, `Prometheus`, `LLM Agents`, `AI Architecture`, `n8n`, `Groq`, `Observability` |
| 2 | [Production-Ready GenAI Agent API](./project02-genai-agent-api) | Internal GenAI agent service exposed via REST API with structured validation, authentication, logging, and Dockerized deployment. | `FastAPI`, `Pydantic`, `Docker`, `LLM Agents`, `API Design`, `Groq` |
| 3 | [Snowflake AI Analyst Agent](./project03-snowflake-ai-analyst-agent) | Natural-language-to-SQL agent with safe query generation and execution against Snowflake sample data. | `LangGraph`, `Snowflake`, `SQL`, `Streamlit`, `Agent Orchestration` |
| 4 | [Agentic Customer Analytics Assistant](./project04-agentic-customer-analytics-assistant) | ML + agent workflow system combining classical modeling and tool-driven reasoning. | `Machine Learning`, `LangChain`, `LangGraph`, `Groq` |
| 5 | [Educational LLM Assistant (RAG Application)](./project05-educational-llm-assistant) | Retrieval-Augmented Generation system for PDF question answering with vector search. | `RAG`, `FAISS`, `Sentence-Transformers`, `Streamlit` |
| 6 | [Predictive Maintenance](./project06-predictive-maintenance) | Machine learning pipeline predicting machine failures from sensor data. | `RandomForest`, `XGBoost`, `Feature Engineering` |
| 7 | [Sales Forecasting](./project07-sales-forecasting) | Demand forecasting pipeline using regression models and time-series preprocessing. | `Time Series`, `XGBoost` |
| 8 | [Customer Churn Prediction](./project08-customer-churn) | Supervised ML model predicting telecom churn. | `Logistic Regression`, `scikit-learn` |
| 9 | [Customer Review Sentiment Analysis](./project09-customer-review-sentiment) | NLP sentiment classification pipeline. | `TF-IDF`, `NLTK` |
| 10 | [Sales & Profit Dashboard (Power BI)](./project10-powerbi-dashboard) | Executive dashboard exploring sales and profit metrics. | `Power BI`, `DAX` |
| 11 | [Expenses Analysis](./project11-expenses-analysis) | Exploratory data analysis of personal expense trends. | `Pandas`, `Visualization` |

---

## 🧠 Core Competencies

### AI & Agent Systems
- LLM Agents & Agentic Architecture (LangChain / LangGraph / MCP)
- Tool-Oriented Agent Design (Model Context Protocol)
- Retrieval-Augmented Generation (RAG)
- Guardrails, Routing & Structured Tool Traces
- Prompt Engineering & LLM Evaluation

### AI Platform & Integration
- API-First AI Services (FastAPI, Pydantic)
- MCP Tool Servers & HTTP/SSE Transport
- Workflow Orchestration (n8n)
- Containerized Multi-Service Architectures (Docker Compose)
- Observability & Metrics (Prometheus)
- Structured Logging & Latency Monitoring

### Machine Learning & Analytics
- Classification & Regression Modeling
- Time Series Forecasting
- Feature Engineering & EDA
- NLP & Text Classification
- SQL & Analytical Querying

### Data & BI
- Data Cleaning & Wrangling (pandas, NumPy)
- Visualization (Matplotlib, Seaborn)
- Business Intelligence (Power BI, DAX)

---

## 🎯 Portfolio Focus

This portfolio emphasizes applied, integration-ready AI:

- Designing AI services rather than standalone notebooks
- Separating tool execution from agent runtime
- Building deployable multi-container architectures
- Instrumenting systems with observability and metrics
- Integrating AI into real-world workflows (n8n)

The goal is to bridge machine learning, software engineering, and enterprise AI architecture.

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