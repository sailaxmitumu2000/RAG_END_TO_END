import faiss
import numpy as np
from typing import List,Dict

embedding_dim=384
index = faiss.IndexFlatL2(embedding_dim)
metadata_store = []
def add_chunks_to_index(chunks:List[Dict]):
    vectors = np.array([chunk["embedding"] for chunk in chunks]).astype("float32")
    index.add(vectors)
    metadata_store.extend(chunks)
def query_index(query_embedding, top_k=5):
    indices, distances = index.search(query_embedding, top_k)
    print("FAISS indices:", indices)
    print("FAISS distances:", distances)
    
    if len(indices) == 0 or len(indices[0]) == 0:
        return []
    
    indices = indices.astype(int)
    results = [metadata_store[i] for i in indices[0] if i < len(metadata_store)]
    print("Retrieved results:", results)
    
    return results


