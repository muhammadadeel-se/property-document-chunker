import json
import os
import re

def search_property_chunks(query, json_path="property_chunks.json", top_n=3):
    """
    Takes a question string, scores each chunk by counting how many 
    question words appear in it, and returns the top N most relevant chunks.
    Handles empty or very short questions gracefully.
    """
    # 1. Handle empty or very short questions gracefully
    if not query or not isinstance(query, str) or len(query.strip()) < 2:
        print("Notice: Query is empty or too short.")
        return []
        
    # 2. Check if the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run chunk_documents.py first.")
        return []
        
    # Load chunks from JSON
    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    # 3. Clean and split the question into unique lowercase words
    query_words = set(re.findall(r'\b\w+\b', query.lower()))
    
    if not query_words:
        return []
        
    scored_chunks = []
    
    # 4. Score each chunk by counting keyword matches
    for chunk in chunks:
        text = chunk.get("text", "")
        text_words = re.findall(r'\b\w+\b', text.lower())
        
        # Count how many words from the question appear in this chunk
        match_score = sum(text_words.count(word) for word in query_words)
        
        scored_chunks.append({
            "score": match_score,
            "chunk": chunk
        })
        
    # Sort chunks by score in descending order
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    
    # 5. Return the top 3 chunks (as a list of dictionaries with text and source)
    top_results = [item["chunk"] for item in scored_chunks[:top_n] if item["score"] > 0]
    
    return top_results

# --- Test script block ---
if __name__ == "__main__":
    sample_queries = [
        "What is the monthly rent for Unit 4B?",
        "Are pets allowed and what is the fee?",
        "",  # Testing empty query handling
        "parking space guidelines"
    ]
    
    for q in sample_queries:
        print(f"\n================================")
        print(f"Query: '{q}'")
        print(f"================================")
        results = search_property_chunks(q)
        
        if not results:
            print("No relevant chunks found.")
        else:
            for idx, res in enumerate(results):
                print(f"\n[Rank {idx+1}] Source: {res['source']}")
                print(f"Text snippet: {res['text'][:150]}...")