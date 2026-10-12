import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search_property_chunks(query, chunks=None, top_k=3):
    """
    Performs vector-based semantic/similarity search using TF-IDF and cosine similarity.
    Automatically loads chunks from property_chunks.json or generates them from .txt files if needed.
    """
    if not chunks:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, 'property_chunks.json')
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
        except Exception:
            pass

    # Fallback: read property txt files directly if json is missing or empty
    if not chunks:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            chunks = []
            for i in range(1, 4):
                txt_path = os.path.join(base_dir, f'property_{i}.txt')
                if os.path.exists(txt_path):
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                        if not paragraphs:
                            paragraphs = [content.strip()]
                        for p in paragraphs:
                            chunks.append({"source": f"property_{i}.txt", "text": p})
        except Exception:
            pass

    if not query or not query.strip() or not chunks:
        return []
    
    chunk_texts = [chunk.get('text', '') for chunk in chunks]
    if not chunk_texts:
        return []
    
    documents = chunk_texts + [query]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    query_vector = tfidf_matrix[-1]
    chunk_vectors = tfidf_matrix[:-1]
    
    similarities = cosine_similarity(query_vector, chunk_vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score > 0.001:
            chunk_copy = chunks[idx].copy()
            chunk_copy['score'] = score
            results.append(chunk_copy)
            
    return results