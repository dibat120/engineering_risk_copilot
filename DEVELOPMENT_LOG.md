# Engineering Risk Copilot — Development Log

## Project
Engineering Risk Copilot

## Context
J.D. Power AI Engineer Job Application Sprint

## Objective
Build a portfolio-ready Applied AI prototype demonstrating practical
experience with LLM APIs, RAG, API integration, AI engineering,
evaluation, and software engineering practices.

---

# Day 1 — Project Definition & Architecture

## Status
COMPLETED

## Main Activities
- Analyzed the J.D. Power AI Engineer job requirements.
- Mapped job requirements to ATS keywords.
- Identified existing evidence, evidence strength, gaps, and sprint actions.
- Selected the Engineering Risk Copilot as the sprint project.
- Defined the initial software architecture.
- Defined the project directory structure.

## Key Engineering Decision
Separate the application into modular layers including:

- core
- agents
- RAG
- services
- tools
- models
- evaluation
- tests
- user interface

## Target AI Architecture

User
→ Application
→ RAG / Tools
→ LLM
→ Grounded Engineering Risk Response

---

# Day 2 — Environment Setup & First LLM Integration

## Status
COMPLETED

## Environment

Operating System:
Windows 11

Python:
3.12.10

Virtual Environment:
.venv

IDE:
Visual Studio Code

## Main Activities

- Created project directory structure.
- Created Python 3.12.10 virtual environment.
- Activated `.venv`.
- Created root configuration files.
- Created `.env` for secrets management.
- Created `.env.example`.
- Created `.gitignore`.
- Installed OpenAI Python SDK.
- Installed python-dotenv.
- Created `app/core/llm.py`.
- Configured OpenAI API credentials.
- Configured OpenAI API billing.
- Added initial API credits.
- Tested first direct LLM API request.

---

# Milestone M1 — LLM API CONNECTED ✅

## Date
2026-08-23

## Test Command

```powershell
python app/core/llm.py

## 2026-08-23 — M2 RAG Pipeline

### M2.1 — Document Loading
**Status:** PASSED ✅

- Implemented text document loading.
- Successfully loaded `engineering_risk_basics.txt`.
- Confirmed document content is accessible to the ingestion pipeline.

### M2.2 — Document Chunking
**Status:** PASSED ✅

- Implemented document chunking.
- Configuration used:
  - `chunk_size = 300`
  - `overlap = 50`
- Test document generated 3 chunks.

### M2.3 — Embeddings
**Status:** PASSED ✅

- Connected the ingestion pipeline to the OpenAI Embeddings API.
- Successfully generated embeddings for all document chunks.
- Embedding vector dimension confirmed: 1536.

### M2.4 — End-to-End RAG Pipeline
**Status:** PASSED ✅

Implemented the complete RAG flow:

LOAD → CHUNK → EMBED → STORE → RETRIEVE → AUGMENT → GENERATE

Test question:

`How can engineering risk be reduced?`

The system successfully retrieved relevant document chunks and generated
an answer grounded in the supplied engineering-risk corpus.

### M2.5.1 — Source Metadata Flow
**Status:** PASSED ✅

Added provenance metadata to retrieved chunks.

The system now preserves and returns:

- source filename
- chunk ID
- semantic similarity score

Example retrieval:

- `engineering_risk_basics.txt` — Chunk 3 — similarity: 0.6367
- `engineering_risk_basics.txt` — Chunk 1 — similarity: 0.6075

The RAG pipeline can therefore associate generated answers with the
document chunks used as supporting context.

### M2.5.2 — Grounding Guardrail Test
**Status:** PASSED ✅

Out-of-context test question:

`What is the recommended inspection interval for a centrifugal pump?`

Retrieval results showed low semantic similarity:

- Chunk 3 — similarity: 0.1503
- Chunk 1 — similarity: 0.1000

Expected system response:

`The available context does not contain enough information to answer this question.`

The model correctly refused to fabricate an unsupported engineering answer.

### Engineering Observation

The vector retriever will still return the mathematically closest chunks
even when none of them contains sufficient information.

Therefore:

**retrieval does not automatically imply sufficient evidence.**

The generation layer must evaluate the retrieved context and decline to
answer when the available evidence is insufficient.

Future evaluation work will investigate retrieval thresholds and more
robust grounding strategies.

---

## Current Project Status

- M1 — OpenAI LLM API Connection ✅
- M2.1 — Document Loading ✅
- M2.2 — Document Chunking ✅
- M2.3 — Embeddings ✅
- M2.4 — End-to-End RAG Pipeline ✅
- M2.5.1 — Source Metadata Flow ✅
- M2.5.2 — Grounding Guardrail ✅

**Current milestone: M2 RAG CORE FUNCTIONAL ✅**

August 24, 2026 — Production Deployment Milestone
Engineering Risk Copilot successfully deployed end-to-end using Streamlit Community Cloud and Render. Public UI successfully communicates with the production FastAPI backend and executes the complete RAG workflow, including semantic retrieval, OpenAI-powered grounded generation, source attribution, similarity scoring, and grounding guardrails.