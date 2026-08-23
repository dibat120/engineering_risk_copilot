import os

from dotenv import load_dotenv
from openai import OpenAI

from app.rag.loader import load_text_file
from app.rag.chunker import chunk_text
from app.rag.embeddings import create_embedding
from app.rag.pipeline import answer_with_rag


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Load variables from the .env file
load_dotenv()

# Read the LLM model name from the environment
model = os.getenv("OPENAI_MODEL")

if not model:
    raise ValueError("OPENAI_MODEL is missing from the .env file.")

# Create authenticated OpenAI client
client = OpenAI()


# ---------------------------------------------------------
# DOCUMENT INFORMATION
# ---------------------------------------------------------

file_path = "data/raw/engineering_risk_basics.txt"

# This is the human-readable source name that will travel
# with every chunk created from this document.
source_name = "engineering_risk_basics.txt"


# ---------------------------------------------------------
# STEP 1 — LOAD DOCUMENT
# ---------------------------------------------------------

document = load_text_file(file_path)


# ---------------------------------------------------------
# STEP 2 — CHUNK DOCUMENT
# ---------------------------------------------------------

chunks = chunk_text(
    document,
    chunk_size=300,
    overlap=50,
)


# ---------------------------------------------------------
# STEP 3 — CREATE EMBEDDINGS + ATTACH METADATA
# ---------------------------------------------------------

stored_chunks = []

# enumerate(..., start=1) gives every chunk a unique ID:
#
# Chunk 1
# Chunk 2
# Chunk 3
# ...
for chunk_id, chunk in enumerate(chunks, start=1):

    # Convert the chunk text into an embedding vector
    embedding = create_embedding(
        text=chunk,
        client=client,
    )

    # Store the chunk together with:
    #
    # - its original text
    # - its numerical embedding
    # - its source document
    # - its chunk identifier
    #
    # This combination forms a richer knowledge unit.
    stored_chunks.append(
        {
            "text": chunk,
            "embedding": embedding,
            "source": source_name,
            "chunk_id": chunk_id,
        }
    )


# ---------------------------------------------------------
# STEP 4 — DEFINE USER QUESTION
# ---------------------------------------------------------

question = "What is the recommended inspection interval for a centrifugal pump?"


# ---------------------------------------------------------
# STEP 5 — RUN RAG PIPELINE
# ---------------------------------------------------------

result = answer_with_rag(
    question=question,
    stored_chunks=stored_chunks,
    client=client,
    model=model,
    top_k=2,
)


# ---------------------------------------------------------
# STEP 6 — DISPLAY ANSWER
# ---------------------------------------------------------

print("RAG QUESTION")
print("-" * 50)
print(question)

print("\nRAG ANSWER")
print("-" * 50)
print(result["answer"])


# ---------------------------------------------------------
# STEP 7 — DISPLAY SOURCES
# ---------------------------------------------------------

print("\nSOURCES")
print("-" * 50)
print(result["sources"])