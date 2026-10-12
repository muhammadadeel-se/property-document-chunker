from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a lightweight, high-performance embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_property_chunks(query, chunks, top_k=3):
    """
    Performs true semantic search using sentence-transformers and cosine similarity.
    """
    if not query or not query.strip():
        return []
    
    chunk_texts = [chunk.get('text', '') for chunk in chunks]
    if not chunk_texts:
        return []
    
    # Encode chunks and query into vector space
    chunk_embeddings = model.encode(chunk_texts)
    query_embedding = model.encode([query])
    
    # Calculate cosine similarity between query and all chunks
    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
    
    # Sort indices by highest similarity score
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        # Guard clause: only include results with meaningful semantic match
        if score > 0.15:
            chunk_copy = chunks[idx].copy()
            chunk_copy['score'] = score
            results.append(chunk_copy)
            
    return results