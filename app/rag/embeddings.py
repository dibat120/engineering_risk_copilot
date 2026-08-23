from openai import OpenAI


def create_embedding(
    text: str,
    client: OpenAI,
    model: str = "text-embedding-3-small",
) -> list[float]:
    """
    Convert text into a numerical embedding vector.

    Parameters
    ----------
    text : str
        Text to convert into an embedding.

    client : OpenAI
        Authenticated OpenAI client.

    model : str
        Embedding model to use.

    Returns
    -------
    list[float]
        Numerical vector representing the semantic meaning of the text.
    """

    # Send the text to the embedding model
    response = client.embeddings.create(
        model=model,
        input=text,
    )

    # Extract and return the embedding vector
    return response.data[0].embedding