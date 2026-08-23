import math


# ---------------------------------------------------------
# FUNCTION 1 — COSINE SIMILARITY
# ---------------------------------------------------------

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Measure semantic similarity between two embedding vectors.

    A score closer to 1 means the vectors point in more similar
    directions and therefore represent more semantically similar text.
    """

    # Both vectors must contain the same number of dimensions.
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions.")

    # Dot product: A · B
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    # Magnitude of vector A
    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    # Magnitude of vector B
    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    # Avoid division by zero.
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    # Cosine similarity formula
    return dot_product / (magnitude_a * magnitude_b)


# ---------------------------------------------------------
# FUNCTION 2 — RETRIEVE TOP CHUNKS
# ---------------------------------------------------------

def retrieve_top_chunks(
    query_embedding: list[float],
    stored_chunks: list[dict],
    top_k: int = 2,
) -> list[dict]:
    """
    Retrieve the chunks whose embeddings are most semantically
    similar to the query embedding.

    Important:
    In this version, metadata such as source and chunk_id
    is preserved during retrieval.

    Parameters
    ----------
    query_embedding : list[float]
        Embedding vector representing the user's question.

    stored_chunks : list[dict]
        Stored knowledge units.

        Each item is expected to contain:

        - "text"
        - "embedding"
        - "source"
        - "chunk_id"

    top_k : int
        Number of most relevant chunks to return.

    Returns
    -------
    list[dict]
        Ranked retrieval results containing:

        - text
        - score
        - source
        - chunk_id
    """

    results = []

    # -----------------------------------------------------
    # STEP 1 — COMPARE QUERY WITH EVERY STORED CHUNK
    # -----------------------------------------------------

    for item in stored_chunks:

        # Calculate semantic similarity between:
        #
        # query embedding
        #       VS
        # document chunk embedding
        score = cosine_similarity(
            query_embedding,
            item["embedding"],
        )


        # -------------------------------------------------
        # STEP 2 — PRESERVE TEXT + METADATA
        # -------------------------------------------------

        # Previously, we stored only:
        #
        # {
        #     "text": ...,
        #     "score": ...
        # }
        #
        # Now we also preserve:
        #
        # source
        # chunk_id
        #
        # This allows provenance information to survive
        # the retrieval stage.
        results.append(
            {
                "text": item["text"],
                "score": score,
                "source": item.get("source", "unknown"),
                "chunk_id": item.get("chunk_id", "unknown"),
            }
        )


    # -----------------------------------------------------
    # STEP 3 — SORT BY SEMANTIC SIMILARITY
    # -----------------------------------------------------

    # Highest score first.
    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )


    # -----------------------------------------------------
    # STEP 4 — RETURN TOP K RESULTS
    # -----------------------------------------------------

    return results[:top_k]