from flask import Flask, render_template, request
from search import search_property_chunks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    top_chunks = []
    answer = ""
    sources = []
    searched = False
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        searched = True
        if query:
            # Retrieve top chunks from search module
            top_chunks = search_property_chunks(query)
            
            # 1. Guard check for empty results
            if not top_chunks:
                answer = "No information found"
                sources = []
            else:
                # 2. Create combined text (limited to 350 chars) and unique sorted sources
                combined = " ".join(c['text'].strip() for c in top_chunks)[:350]
                sources = sorted({c['source'] for c in top_chunks})
                answer = f"Based on the documents, the answer is: {combined}."
            
    # 3. Pass answer and sources explicitly to the template
    return render_template(
        "index.html", 
        query=query, 
        results=top_chunks, 
        answer=answer, 
        sources=sources, 
        searched=searched
    )

if __name__ == "__main__":
    app.run(debug=True)