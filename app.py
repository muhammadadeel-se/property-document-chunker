import os
from flask import Flask, render_template, request
from search import search_property_chunks

try:
    from google import genai
except ImportError:
    genai = None

app = Flask(__name__)

api_key = os.getenv("GOOGLE_API_KEY")
client = None
if genai and api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None


def fallback_answer(query, results):
    if not results:
        return "No relevant lease documents found to answer your question."

    normalized_query = query.lower()
    for result in results:
        text = result.get("text", "")
        if normalized_query in text.lower():
            return text.strip()

    best_match = results[0].get("text", "").strip()
    if len(best_match) > 800:
        return best_match[:800].rstrip() + "..."
    return best_match


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
            results = search_property_chunks(query)

            if results:
                context_text = "\n\n".join([f"Source ({r['source']}): {r['text']}" for r in results])
                prompt = f"""
                You are a professional property assistant. Answer the user's question accurately using ONLY the provided context below. If the answer cannot be found in the context, state that clearly.

                Context:
                {context_text}

                Question: {query}

                Answer:
                """

                if client:
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt,
                        )
                        answer = getattr(response, "text", None) or "Unable to generate a response from the Gemini API."
                    except Exception as exc:
                        answer = f"AI answer unavailable: {exc}.\n\n{fallback_answer(query, results)}"
                else:
                    answer = fallback_answer(query, results)
            else:
                answer = "No relevant lease documents found to answer your question."

    return render_template("index.html", query=query, results=results, answer=answer, searched=searched)


if __name__ == "__main__":
    app.run(debug=True)