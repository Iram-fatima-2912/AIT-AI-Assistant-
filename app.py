
import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return "AIT AI Application is Running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "AIT AI Assistant"
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400

    if not client:
        return jsonify({
            "error": "Groq API key is missing"
        }), 500

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception:
        app.logger.exception("AI response generation failed")
        return jsonify({
            "error": "Unable to generate AI response"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
