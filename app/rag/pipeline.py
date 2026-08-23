from openai import OpenAI

from app.rag.embeddings import create_embedding
from app.rag.vector_store import retrieve_top_chunks


# ---------------------------------------------------------
# FUNCTION 1 — BUILD CONTEXT WITH SOURCE METADATA
# ---------------------------------------------------------

def build_context(results: list[dict]) -> str:
    """
    Combine retrieved chunks into a single context block.

    Unlike the previous version, each chunk is now accompanied
    by metadata identifying its source document and chunk number.

    Parameters
    ----------
    results : list[dict]
        List of retrieved chunks.

        Each result is expected to contain:

        - "text":
            Original text of the chunk.

        - "score":
            Semantic similarity score.

        - "source":
            Name of the source document.

        - "chunk_id":
            Identifier of the chunk inside the document.

    Returns
    -------
    str
        A single context block containing both the retrieved
        information and its source metadata.
    """

    # This temporary list will contain the formatted
    # representations of all retrieved chunks.
    context_parts = []

    # Process retrieved chunks one by one.
    for result in results:

        # Retrieve the metadata associated with this chunk.
        #
        # .get() is used instead of ["source"] so that
        # the program does not crash if metadata is missing.
        #
        # If the metadata is absent, we display "unknown".
        source = result.get("source", "unknown")
        chunk_id = result.get("chunk_id", "unknown")

        # Retrieve the original text.
        text = result["text"]

        # Build a readable context block containing
        # both the source information and the chunk text.
        #
        # Example:
        #
        # [SOURCE: engineering_risk_basics.txt | CHUNK: 2]
        #
        # Risk mitigation aims to reduce...
        context_part = (
            f"[SOURCE: {source} | CHUNK: {chunk_id}]\n"
            f"{text}"
        )

        # Add the formatted chunk to our temporary list.
        context_parts.append(context_part)

    # Combine all retrieved chunks into one large context.
    #
    # Two line breaks are inserted between chunks
    # to keep them clearly separated.
    context = "\n\n".join(context_parts)

    return context


# ---------------------------------------------------------
# FUNCTION 2 — FORMAT SOURCES FOR THE FINAL RESPONSE
# ---------------------------------------------------------

def build_sources(results: list[dict]) -> str:
    """
    Build a readable source list from retrieved chunks.

    Parameters
    ----------
    results : list[dict]
        Retrieved chunks containing metadata.

    Returns
    -------
    str
        Human-readable list of sources.
    """

    sources = []

    for result in results:

        source = result.get("source", "unknown")
        chunk_id = result.get("chunk_id", "unknown")
        score = result.get("score", 0.0)

        # Create one readable citation entry.
        #
        # Example:
        # - engineering_risk_basics.txt — Chunk 2
        #   (similarity: 0.6367)
        source_line = (
            f"- {source} — Chunk {chunk_id} "
            f"(similarity: {score:.4f})"
        )

        sources.append(source_line)

    # Join all source entries into one block.
    return "\n".join(sources)


# ---------------------------------------------------------
# FUNCTION 3 — COMPLETE RAG PIPELINE WITH SOURCES
# ---------------------------------------------------------

def answer_with_rag(
    question: str,
    stored_chunks: list[dict],
    client: OpenAI,
    model: str,
    top_k: int = 2,
) -> dict:
    """
    Answer a user question using Retrieval-Augmented Generation
    and return both the answer and its retrieved sources.

    RAG logic:

    Question
        ↓
    Create query embedding
        ↓
    Retrieve relevant chunks
        ↓
    Preserve source metadata
        ↓
    Build context
        ↓
    Augment prompt
        ↓
    Generate grounded answer
        ↓
    Return answer + sources

    Parameters
    ----------
    question : str
        User's natural-language question.

    stored_chunks : list[dict]
        Document chunks stored together with:
        - text
        - embedding
        - source
        - chunk_id

    client : OpenAI
        Authenticated OpenAI client.

    model : str
        Name of the LLM used for generation.

    top_k : int
        Number of most relevant chunks to retrieve.

    Returns
    -------
    dict
        Dictionary containing:

        - "answer":
            Generated LLM answer.

        - "sources":
            Retrieved source information.

        - "results":
            Raw retrieval results.
    """

    # -----------------------------------------------------
    # STEP 1 — EMBED THE USER QUESTION
    # -----------------------------------------------------

    # Convert the user's natural-language question
    # into a numerical embedding vector.
    #
    # This allows us to compare the meaning of the question
    # with the meanings represented by document embeddings.
    query_embedding = create_embedding(
        text=question,
        client=client,
    )


    # -----------------------------------------------------
    # STEP 2 — RETRIEVE RELEVANT CHUNKS
    # -----------------------------------------------------

    # Compare the query embedding against all stored
    # document embeddings.
    #
    # The retriever returns the top_k chunks with the
    # highest semantic similarity.
    results = retrieve_top_chunks(
        query_embedding=query_embedding,
        stored_chunks=stored_chunks,
        top_k=top_k,
    )


    # -----------------------------------------------------
    # STEP 3 — BUILD CONTEXT WITH METADATA
    # -----------------------------------------------------

    # Convert separate retrieval results into one context
    # block that includes:
    #
    # - source document
    # - chunk identifier
    # - retrieved text
    #
    # This means the LLM no longer receives anonymous text.
    context = build_context(results)


    # -----------------------------------------------------
    # STEP 4 — BUILD HUMAN-READABLE SOURCE LIST
    # -----------------------------------------------------

    # Prepare the source information separately.
    #
    # We will eventually display this alongside the answer.
    sources = build_sources(results)


    # -----------------------------------------------------
    # STEP 5 — AUGMENT THE PROMPT
    # -----------------------------------------------------

    # This remains the "A" in RAG.
    #
    # We supply:
    #
    #     INSTRUCTIONS
    #          +
    #     RETRIEVED CONTEXT
    #          +
    #     SOURCE METADATA
    #          +
    #     USER QUESTION
    #
    # The model is explicitly instructed not to use knowledge
    # outside the retrieved context.
    prompt = f"""
You are an engineering risk assistant.

Answer the question using only the context provided below.

Do not rely on outside knowledge.

If the available context does not contain enough information
to answer the question, explicitly say:

"The available context does not contain enough information
to answer this question."

Do not invent facts, values, standards, procedures, or sources.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    # -----------------------------------------------------
    # STEP 6 — GENERATE THE GROUNDED ANSWER
    # -----------------------------------------------------

    # Send the augmented prompt to the LLM.
    #
    # At this point, the model receives the user's question
    # together with the evidence retrieved from our corpus.
    response = client.responses.create(
        model=model,
        input=prompt,
    )


    # -----------------------------------------------------
    # STEP 7 — EXTRACT GENERATED TEXT
    # -----------------------------------------------------

    answer = response.output_text


    # -----------------------------------------------------
    # STEP 8 — RETURN ANSWER + SOURCES
    # -----------------------------------------------------

    # Previously, this function returned only:
    #
    #     response.output_text
    #
    # Now it returns a dictionary containing multiple pieces
    # of useful information.
    #
    # This is important because our future FastAPI endpoint
    # could eventually return a structured JSON response.
    return {
        "answer": answer,
        "sources": sources,
        "results": results,
    }