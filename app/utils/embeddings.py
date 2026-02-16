from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Adds embeddings to each chunk dict.
    """
    texts = [chunk["text"] for chunk in chunks]  # extract text
    embeddings = model.encode(texts, show_progress_bar=True)

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()  # ✅ lowercase 'tolist'

    return chunks
def embed_query(query: str) -> np.ndarray:
    """
    Convert a user query into an embedding vector
    """
    return model.encode([query], show_progress_bar=False)[0]

