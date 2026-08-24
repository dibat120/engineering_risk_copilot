import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from app.rag.loader import load_text_file
from app.rag.chunker import chunk_text
from app.rag.embeddings import create_embedding
from app.rag.pipeline import answer_with_rag


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Load environment variables from the local .env file.
load_dotenv()

# Read the model name from the environment.
model = os.getenv("OPENAI_MODEL")

if not model:
    raise ValueError("OPENAI_MODEL is missing from the .env file.")

# Create the authenticated OpenAI client.
#
# The SDK automatically reads OPENAI_API_KEY from
# the environment.
client = OpenAI()


# ---------------------------------------------------------
# CORPUS CONFIGURATION
# ---------------------------------------------------------

# Current prototype knowledge base.
file_path = "data/raw/engineering_risk_basics.txt"

# Human-readable source name stored with each chunk.
source_name = "engineering_risk_basics.txt"


# ---------------------------------------------------------
# APPLICATION LIFESPAN
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Prepare the RAG knowledge base once when FastAPI starts.

    Instead of rebuilding document embeddings every time a user
    asks a question, we:

    1. load the document;
    2. chunk it;
    3. create embeddings;
    4. attach source metadata;
    5. keep the resulting knowledge units in application memory.

    This is still an in-memory prototype.
    A persistent vector database may replace this later.
    """

    # -----------------------------------------------------
    # STEP 1 — LOAD DOCUMENT
    # -----------------------------------------------------

    document = load_text_file(file_path)


    # -----------------------------------------------------
    # STEP 2 — CHUNK DOCUMENT
    # -----------------------------------------------------

    chunks = chunk_text(
        document,
        chunk_size=300,
        overlap=50,
    )


    # -----------------------------------------------------
    # STEP 3 — EMBED + STORE KNOWLEDGE UNITS
    # -----------------------------------------------------

    stored_chunks = []

    for chunk_id, chunk in enumerate(chunks, start=1):

        embedding = create_embedding(
            text=chunk,
            client=client,
        )

        stored_chunks.append(
            {
                "text": chunk,
                "embedding": embedding,
                "source": source_name,
                "chunk_id": chunk_id,
            }
        )


    # -----------------------------------------------------
    # STEP 4 — SAVE KNOWLEDGE BASE IN FASTAPI MEMORY
    # -----------------------------------------------------

    # app.state lets us keep application-level objects
    # available to our endpoints.
    app.state.stored_chunks = stored_chunks

    print(
        f"RAG knowledge base ready: "
        f"{len(stored_chunks)} chunks loaded."
    )

    # FastAPI starts serving requests here.
    yield

    # Nothing specific to clean up yet.


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="Engineering Risk Copilot API",
    description="API backend for the Engineering Risk Copilot RAG application.",
    version="0.2.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class AskRequest(BaseModel):
    """
    JSON request expected by POST /ask.

    Example:

    {
        "question": "How can engineering risk be reduced?"
    }
    """

    question: str


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Engineering Risk Copilot API",
        "status": "running",
        "version": "0.2.0",
    }


# ---------------------------------------------------------
# HEALTH ENDPOINT
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Engineering Risk Copilot API",
        "rag_ready": True,
    }


# ---------------------------------------------------------
# ASK ENDPOINT — RAG CONNECTED
# ---------------------------------------------------------

@app.post("/ask")
def ask_question(request: AskRequest):
    """
    Answer a user question using the Engineering Risk
    Copilot RAG pipeline.

    Flow:

    HTTP question
        ↓
    FastAPI
        ↓
    Query embedding
        ↓
    Semantic retrieval
        ↓
    Context augmentation
        ↓
    OpenAI LLM
        ↓
    Grounded answer
        ↓
    Answer + source metadata
    """

    # Run the complete RAG pipeline using the knowledge
    # base prepared when FastAPI started.
    result = answer_with_rag(
        question=request.question,
        stored_chunks=app.state.stored_chunks,
        client=client,
        model=model,
        top_k=2,
    )


    # -----------------------------------------------------
    # FORMAT SOURCES AS STRUCTURED JSON
    # -----------------------------------------------------

    # pipeline.py already gives us the raw retrieval results.
    #
    # Here we transform them into API-friendly structured
    # metadata that Streamlit can later display cleanly.
    sources = []

    for item in result["results"]:

        sources.append(
            {
                "source": item.get("source", "unknown"),
                "chunk_id": item.get("chunk_id", "unknown"),
                "similarity": round(item.get("score", 0.0), 4),
            }
        )


    # -----------------------------------------------------
    # RETURN API RESPONSE
    # -----------------------------------------------------

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": sources,
    }