# Engineering Risk Copilot

An Applied AI prototype for retrieving engineering knowledge and generating
grounded, traceable answers using Retrieval-Augmented Generation (RAG).

---

## Project Objective

Engineering Risk Copilot explores how Large Language Models (LLMs) can be
combined with engineering documents to support risk-related knowledge
retrieval and decision support.

The prototype is designed around a simple principle:

> Retrieve relevant information from the supplied engineering knowledge base
> first, then use that information as context for the LLM response.

The current implementation focuses on transparency, traceability, and
grounding rather than relying only on the general knowledge of an LLM.

---

## Current Architecture

The current RAG pipeline follows:

LOAD
→ CHUNK
→ EMBED
→ STORE
→ RETRIEVE
→ AUGMENT
→ GENERATE
→ CITE
→ GUARDRAIL

### 1. Load

Engineering documents are loaded into the application.

### 2. Chunk

Documents are divided into smaller text segments suitable for semantic
retrieval.

### 3. Embed

Each chunk is converted into a numerical embedding vector using the
OpenAI Embeddings API.

### 4. Store

Chunks, embeddings, and associated metadata are stored for retrieval.

### 5. Retrieve

The user's question is embedded and compared against stored document
embeddings using semantic similarity.

### 6. Augment

The most relevant retrieved chunks are inserted into the LLM prompt as
external context.

### 7. Generate

The LLM generates an answer based on the retrieved context.

### 8. Cite

The system preserves source metadata including document name, chunk ID,
and similarity score.

### 9. Guardrail

If the retrieved context does not contain sufficient information, the
system is instructed not to fabricate an engineering answer.

---

## Current Milestones

### M1 — LLM API Connection ✅

- OpenAI Python SDK configured
- Environment variables loaded securely from `.env`
- Successful LLM API request completed

### M2 — RAG Pipeline ✅

- M2.1 — Document Loading ✅
- M2.2 — Document Chunking ✅
- M2.3 — Embedding Generation ✅
- M2.4 — End-to-End RAG Pipeline ✅
- M2.5.1 — Source Metadata Flow ✅
- M2.5.2 — Grounding Guardrail Test ✅

Current status:

**M2 — RAG CORE FUNCTIONAL**

---

## Grounding Test

The system was tested with a question whose answer was intentionally absent
from the supplied corpus:

> What is the recommended inspection interval for a centrifugal pump?

The retriever returned only weak semantic matches.

The system correctly responded:

> The available context does not contain enough information to answer this
> question.

This test demonstrates the first grounding guardrail implemented in the
prototype.

---

## Project Structure

```text
engineering_risk_copilot/
│
├── app/
│   ├── core/
│   └── rag/
│
├── data/
│   └── raw/
│
├── docs/
├── evals/
├── scripts/
├── tests/
├── ui/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt