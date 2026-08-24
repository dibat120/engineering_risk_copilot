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

~~~text
LOAD
  ↓
CHUNK
  ↓
EMBED
  ↓
STORE
  ↓
RETRIEVE
  ↓
AUGMENT
  ↓
GENERATE
  ↓
SOURCE ATTRIBUTION
  ↓
GUARDRAIL
~~~

### 1. Load

Engineering documents are loaded into the application.

### 2. Chunk

Documents are divided into smaller text segments suitable for semantic
retrieval.

### 3. Embed

Each chunk is converted into a numerical embedding vector using the
OpenAI Embeddings API.

### 4. Store

Chunks, embeddings, and associated metadata are stored in memory for
retrieval during the current execution.

The current prototype does not yet use a persistent vector database.

### 5. Retrieve

The user's question is embedded and compared against stored document
embeddings using semantic similarity.

The most relevant chunks are ranked and selected for downstream generation.

### 6. Augment

The most relevant retrieved chunks are inserted into the LLM prompt as
external context.

### 7. Generate

The LLM generates an answer based on the retrieved context.

### 8. Source Attribution

The system preserves and displays source metadata including document name,
chunk ID, and semantic similarity score.

This provides basic traceability between the generated answer and the
retrieved source material.

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
- M2.3B — Semantic Retrieval ✅
- M2.4 — End-to-End RAG Pipeline ✅
- M2.5.1 — Source Metadata Flow ✅
- M2.5.2 — Grounding Guardrail Test ✅
- M2.6 — First Git Checkpoint ✅

**Current status: M2 — RAG CORE FUNCTIONAL**

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

~~~text
engineering_risk_copilot/
│
├── app/
│   ├── core/
│   │   └── llm.py
│   │
│   └── rag/
│       ├── __init__.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── loader.py
│       ├── pipeline.py
│       ├── retriever.py
│       └── vector_store.py
│
├── data/
│   └── raw/
│       └── engineering_risk_basics.txt
│
├── scripts/
│   ├── __init__.py
│   ├── ingest_documents.py
│   └── run_rag_demo.py
│
├── .env.example
├── .gitignore
├── DEVELOPMENT_LOG.md
├── README.md
└── requirements.txt
~~~

---

## Requirements

The current prototype uses:

~~~text
openai==3.3.1
python-dotenv==1.2.3
~~~

Install the project dependencies with:

~~~powershell
pip install -r requirements.txt
~~~

---

## Environment Configuration

Create a local `.env` file based on `.env.example`.

Example:

~~~text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=your_model_name_here
~~~

The real `.env` file must remain local and must never be committed to Git.

---

## Running the RAG Demo

From the project root:

~~~powershell
python -m scripts.run_rag_demo
~~~

The demo:

1. loads the engineering risk document;
2. chunks the document;
3. generates embeddings;
4. creates an in-memory collection of knowledge units;
5. embeds the user query;
6. performs semantic retrieval;
7. augments the LLM prompt with retrieved context;
8. generates a grounded answer;
9. displays source attribution.

---

## Security

API credentials are loaded through environment variables.

The local `.env` file is excluded from Git through `.gitignore` and must
never be committed to the repository.

`.env.example` documents the required configuration without exposing
credentials.

The local Python virtual environment `.venv/` is also excluded from version
control.

---

## Current Scope

This repository represents an early functional RAG prototype.

The current implementation includes:

- document loading;
- fixed-size text chunking with overlap;
- OpenAI embedding generation;
- in-memory vector storage;
- cosine-similarity semantic retrieval;
- context augmentation;
- OpenAI LLM-based answer generation;
- source metadata attribution;
- a basic grounding guardrail.

The current implementation does **not** yet include:

- a persistent vector database such as ChromaDB, FAISS, Pinecone, or Weaviate;
- large-scale PDF ingestion;
- production-grade document citation;
- automated retrieval and generation evaluation pipelines;
- production observability and tracing;
- FastAPI deployment;
- a public Streamlit user interface;
- agentic workflows or tool calling.

These capabilities are planned for later development stages.

---

## Engineering Lessons Learned

This prototype was intentionally built incrementally to expose the underlying
mechanics of RAG rather than hiding them behind higher-level frameworks.

Key observations include:

- retrieval is not the same as evidence sufficiency;
- a vector retriever will still return the mathematically closest chunks even
  when all available matches are weak;
- chunking strategy directly affects retrieval quality;
- source metadata should travel with retrieved knowledge units;
- grounding instructions are essential when generated answers may influence
  engineering decisions.

---

## Development Philosophy

Each major capability is:

1. implemented;
2. tested;
3. documented;
4. evaluated;
5. committed as a reproducible development milestone.

The objective is not only to build a working AI application, but also to
understand and document the engineering logic behind each component.

---

## Next Development Areas

Planned future work includes:

- persistent vector storage;
- larger engineering document corpus;
- PDF ingestion;
- retrieval evaluation;
- improved chunking strategy;
- source-aware answer formatting;
- automated eval datasets;
- observability and tracing;
- FastAPI integration;
- Streamlit user interface;
- cloud deployment;
- agentic workflows and tool calling.

---

## Status

**Prototype under active development — August 2026**