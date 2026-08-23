def chunk_text(
    text: str,
    chunk_size: int = 300,
    overlap: int = 50,
) -> list[str]:
    """
    Split a text into overlapping chunks.

    Parameters
    ----------
    text : str
        Full document text.

    chunk_size : int
        Maximum number of characters in each chunk.

    overlap : int
        Number of characters shared between consecutive chunks.

    Returns
    -------
    list[str]
        List containing the text chunks.
    """

    # Basic validation
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    # Remove unnecessary spaces at the beginning and end
    text = text.strip()

    # Store the generated chunks
    chunks = []

    # Starting position of the current chunk
    start = 0

    while start < len(text):

        # Determine where the current chunk ends
        end = start + chunk_size

        # Extract the chunk
        chunk = text[start:end]

        # Store it
        chunks.append(chunk)

        # Move forward while preserving some overlap
        start += chunk_size - overlap

    return chunks