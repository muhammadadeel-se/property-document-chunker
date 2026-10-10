import os
import json

def chunk_text(text, source_name, target_words=100):
    """Splits text into chunks of approximately target_words by words."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), target_words):
        chunk_words = words[i:i + target_words]
        chunk_string = " ".join(chunk_words)
        chunks.append({
            "text": chunk_string,
            "source": source_name
        })
        
    return chunks

def main():
    input_folder = "property_docs"
    output_file = "property_chunks.json"
    
    all_chunks = []
    
    if not os.path.exists(input_folder):
        print(f"Error: Directory '{input_folder}' not found.")
        return

    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    
    if not files:
        print(f"No text files found in '{input_folder}'.")
        return

    for filename in sorted(files):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            
            file_chunks = chunk_text(content, filename, target_words=100)
            all_chunks.extend(file_chunks)

    with open(output_file, "w", encoding="utf-8") as json_out:
        json.dump(all_chunks, json_out, indent=4)
        
    print(f"Successfully processed {len(files)} documents.")
    print(f"Generated {len(all_chunks)} chunks saved to '{output_file}'.")
    
    print("\n--- Validation Check ---")
    print(f"Total Chunks: {len(all_chunks)} (Requirement: >= 10)")
    for idx, c in enumerate(all_chunks):
        word_count = len(c["text"].split())
        print(f"Chunk {idx+1}: {word_count} words (Source: {c['source']})")

if __name__ == "__main__":
    main()