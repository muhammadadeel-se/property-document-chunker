# Property Document Chunker & Assistant Search Pipeline

This project implements a foundational data ingestion and retrieval pipeline for a property assistant workflow. It processes raw lease agreements, segments them using sentence-aware chunking, stores them in a structured JSON format, and provides a keyword-based search function to fetch the most relevant clauses.

---

## Project Structure

```text
property-chunker/
│
├── property_docs/                 # Directory containing raw lease documents
│   ├── property_1.txt
│   ├── property_2.txt
│   └── property_3.txt
│
├── chunk_documents.py             # Script for sentence-aware text chunking
├── search.py                      # Keyword search function for retrieving top chunks
├── property_chunks.json           # Generated JSON output containing text and source metadata
└── README.md                      # Project documentation