from dotenv import load_dotenv
from openai import OpenAI

from app.rag.loader import load_text_file
from app.rag.chunker import chunk_text
from app.rag.embeddings import create_embedding
from app.rag.vector_store import retrieve_top_chunks


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

client = OpenAI()


# ---------------------------------------------------------
# DOCUMENT PATH
# ---------------------------------------------------------

file_path = "data/raw/engineering_risk_basics.txt"


# ---------------------------------------------------------
# STEP 1 — LOAD DOCUMENT
# ---------------------------------------------------------

document = load_text_file(file_path)

print("DOCUMENT LOADED")
print("-" * 50)
print(document)


# ---------------------------------------------------------
# STEP 2 — CHUNK DOCUMENT
# ---------------------------------------------------------

chunks = chunk_text(
    document,
    chunk_size=300,
    overlap=50,
)

print("\nDOCUMENT CHUNKED")
print("-" * 50)

print(f"Number of chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n--- CHUNK {index} ---")
    print(chunk)


# ---------------------------------------------------------
# STEP 3 — CREATE EMBEDDINGS AND STORE THEM
# ---------------------------------------------------------

print("\nCREATING EMBEDDINGS")
print("-" * 50)

stored_chunks = []


for index, chunk in enumerate(chunks, start=1):

    embedding = create_embedding(
        text=chunk,
        client=client,
    )

    # Store the original text together with its embedding.
    stored_chunks.append(
        {
            "text": chunk,
            "embedding": embedding,
        }
    )

    print(f"\n--- EMBEDDING FOR CHUNK {index} ---")
    print(f"Characters: {len(chunk)}")
    print(f"Vector dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")


# ---------------------------------------------------------
# STEP 4 — EMBED THE USER QUERY
# ---------------------------------------------------------

query = "How can engineering risk be reduced?"

print("\nUSER QUERY")
print("-" * 50)
print(query)


query_embedding = create_embedding(
    text=query,
    client=client,
)

print(f"Query vector dimensions: {len(query_embedding)}")


# ---------------------------------------------------------
# STEP 5 — SEMANTIC RETRIEVAL
# ---------------------------------------------------------

results = retrieve_top_chunks(
    query_embedding=query_embedding,
    stored_chunks=stored_chunks,
    top_k=2,
)


print("\nSEMANTIC SEARCH RESULTS")
print("-" * 50)


for rank, result in enumerate(results, start=1):

    print(f"\n--- RESULT {rank} ---")

    print(
        f"Similarity score: "
        f"{result['score']:.4f}"
    )

    print(result["text"])