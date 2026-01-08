# Project 10 — Production-Ready GenAI Agent API 
## Agentic AI | FastAPI | Pydantic | Docker

Project 10 simulate an internal GenAI agent service that provides controlled, observable AI capabilities to business systems via a REST API.

## Overview

The project demonstrates how to deploy a production-style GenAI agent as a backend service, focusing on:
- API-first design (no UI, no notebooks)
- strict request/response validation
- authentication and safety guardrails
- agent-based decision logic with tool routing
- containerized, observable deployment

This is not a chatbot demo — it is an AI capability exposed as a service that other systems can reliably integrate with.

<img src="images/shot1.png" width="800"/>
<img src="images/shot2.png" width="800"/>
<img src="images/shot3.png" width="800"/>
---

## Architecture (High Level)

Client Systems (BI, CRM, Internal Apps)
              |
              v
        FastAPI REST API
              |
        Agent Layer (Decision Logic)
          |           |
     Calculator     Time Tool
          |           |
          +---- LLM (Groq)
              |
         Structured Response

---
 
## Key Features

*API & Infrastructure*
- FastAPI service with OpenAPI documentation
- Pydantic schemas for strict input/output validation
- pydantic-settings for typed configuration via environment variables
- API-Key authentication via `X-API-Key`
- Docker & Docker Compose for reproducible local deployment

*Observability*
- `/health` endpoint for service checks
- `/metrics` endpoint (Prometheus-style counters & latency)
- Request-scoped middleware with:
    + `X-Request-ID` propagation
    + consistent structured logging
- Execution timing and success/failure tracking

*Agentic Behavior*

- Clean Agent abstraction separating API layer from AI logic
- Deterministic tool routing:
    + Math expressions → safe calculator tool
    + Time queries → timezone-aware time tool
    + All other inputs → LLM
- `tool_calls` returned in responses for full traceability

---

## Endpoints

`GET /health` 

Simple health check for orchestration and monitoring.

`POST /query`

Main agent interaction endpoint.

*Request*

{
  "user_input": "2*(3+4) - 5/2",
  "session_id": "demo-session-1",
  "debug": false
}

*Response*

{
  "request_id": "d1b3d131-7aa1-4649-ab39-f7f951f2d9ba",
  "answer": "11.5",
  "latency_ms": 3,
  "model": "llama-3.1-8b-instant",
  "warnings": [],
  "tool_calls": ["calculator.safe_eval"]
}

`Get /metrics`

Prometheus-style metrics for observability (optionally protected by API key).

---

## Agent Logic (Current)

The agent follows simple, explicit decision rules:

1. Math-only input → Calculator tool (safe AST evaluation)
2. Time queries → Time tool (timezone-aware)
3. All other input → LLM call

This design allows new tools or LangGraph-based workflows to be added *without changing the API contract*.

---

## Real-World Use Cases

1. Internal AI Assistant Service (Primary Use Case)

A company centralizes AI access behind a secure, observable API to:

- standardize AI usage across teams
- avoid uncontrolled direct LLM calls
- enforce guardrails and logging
- control costs and prompts centrally

Multiple systems (HR, Sales, Analytics, Support) call the same agent service.

---

2. AI-Powered Decision Support Microservice

An AI layer that:

- explains dashboards and reports
- summarizes structured and unstructured data
- reasons over business questions

The agent decides whether to use tools or an LLM, returning structured responses to BI tools.

---

3. AI Gateway / LLM Control Plane

A centralized “AI gateway” that:

- abstracts LLM providers
- applies authentication and safety checks
- logs and measures all AI usage

Comparable to an internal OpenAI proxy with agent logic.

---

## Example curl request 

curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{"user_input":"What time is it in Berlin?"}'

---

## Design Tradeoffs & Limitations

- Stateless by default (session_id reserved for future state)
- Tools are intentionally simple and deterministic
- No UI — API-first by design
- No cloud deployment (local containerization only)
- Built for clarity and extensibility, not maximum throughput
