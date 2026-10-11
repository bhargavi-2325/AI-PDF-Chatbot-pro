from flask import Flask, render_template, request, jsonify
import os

from pdf_reader import extract_text
from chunking import create_chunks
from embedding import create_embeddings, create_question_embedding
from vector_store import create_vector_store, search_vector_store
from gemini_chat import ask_gemini

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        if "pdf" not in request.files:
            return jsonify({
                "success": False,
                "message": "No PDF selected."
            })

        file = request.files["pdf"]

        if file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a PDF."
            })

        pdf_path = os.path.join(UPLOAD_FOLDER, "sample.pdf")

        file.save(pdf_path)

        print("📄 Reading PDF...")
        text = extract_text(pdf_path)

        print("✂️ Creating Chunks...")
        chunks = create_chunks(text)

        print("🧠 Creating Embeddings...")
        embeddings = create_embeddings(chunks)

        print("💾 Creating Vector Store...")
        create_vector_store(embeddings, chunks)

        print("✅ PDF Processing Completed")

        return jsonify({
            "success": True,
            "message": "✅ PDF Uploaded Successfully!"
        })

    except Exception as e:

        print("UPLOAD ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        question = data.get("question", "").strip()

        if question == "":
            return jsonify({
                "answer": "Please enter a question."
            })

        print("➡️ Question:", question)

        question_embedding = create_question_embedding(question)

        print("✅ Question Embedding Created")

        results = search_vector_store(question_embedding)

        print("✅ Context Retrieved")

        context = "\n\n".join(results)

        print("🤖 Asking Gemini...")

        answer = ask_gemini(question, context)

        print("✅ Gemini Response Received")

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ASK ERROR:", e)

        return jsonify({
            "answer": f"Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)