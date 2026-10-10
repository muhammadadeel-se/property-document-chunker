# Property Document Chunking Pipeline

This repository contains a Python script designed to ingest raw property lease documents, split them into manageable text chunks of approximately 200 words, and export them into a structured JSON file for downstream assistant/RAG applications.

## Project Structure
- `property_docs/`: Directory containing raw text files (`property_1.txt`, `property_2.txt`, `property_3.txt`).
- `chunk_documents.py`: Python script to read, chunk, and export data.
- `property_chunks.json`: Generated output containing text chunks and source mappings.

## Prerequisites
- Python 3.7 or higher installed on your system.

## How to Run
1. Clone the repository and navigate to the project folder.
2. Ensure your sample documents are placed inside the `property_docs` directory.
3. Run the script using your terminal or VS Code:
   ```bash
   python chunk_documents.py