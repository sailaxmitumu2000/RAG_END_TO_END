from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits a long string into smaller overlapping chunks.
    Returns a list of text chunks.
    """
    if not isinstance(text, str):
        text = str(text)

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap for context

    return chunks  # ✅ make sure we return the list, not its length
