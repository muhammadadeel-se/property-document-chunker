from flask import Flask, render_template, request
from search import search_property_chunks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    answer = ""
    searched = False
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        searched = True
        if query:
            # 1. Retrieve top 3 relevant chunks
            results = search_property_chunks(query)
            
            if results:
                # 2. Combine key info from chunks using string processing
                combined_info = " ".join([r['text'].strip() for r in results])
                
                # 3. Extract unique source documents
                sources = list(set([r['source'] for r in results]))
                sources_str = ", ".join(sources)
                
                # 4. Format using the required template
                answer = f"Based on the documents, the answer is: {combined_info[:350]}... Sources: {sources_str}."
            else:
                answer = "No information found matching your query."
            
    return render_template("index.html", query=query, results=results, answer=answer, searched=searched)

if __name__ == "__main__":
    app.run(debug=True)