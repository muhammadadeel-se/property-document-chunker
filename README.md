## 🚀 Live Demo
You can access the live deployed application here: 
👉 **[https://112233.pythonanywhere.com](https://112233.pythonanywhere.com)**
# Property Assistant RAG Web Application

A lightweight, Flask-based Retrieval-Augmented Generation (RAG) web application designed to search through property documents using semantic vector embeddings and generate source-attributed summaries.

---

## Features
- **Semantic Search:** Uses vector embeddings and cosine similarity to find relevant text based on meaning, not just exact keyword matches.
- **Source Attribution:** Displays the original source document filenames alongside generated summaries.
- **Robust Guardrails:** Handles empty results gracefully with a clean fallback message.
- **Pre-computed Embeddings:** Optimizes startup and response times by serializing document embeddings.

---

## Project Structure
```text
property-assistant/
│
├── app.py                   # Main Flask web application route & logic
├── search.py                # Semantic retrieval & cosine similarity logic
├── generate_embeddings.py   # Script to pre-compute vector embeddings
├── property_chunks.json     # Raw text data source files/chunks
├── embeddings.pkl           # Serialized pre-computed vector cache
├── requirements.txt         # Python package dependencies
├── Procfile                 # Deployment process instructions for Render
└── templates/
    └── index.html           # Frontend UI template