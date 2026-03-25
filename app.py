from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(__name__)

# 🔑 API KEY
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# 📚 Load Knowledge Base
knowledge = ""
folder_path = "Knowledge_base"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            knowledge += f.read() + "\n\n"


# 🌐 Home Route
@app.route("/")
def home():
    return render_template("index.html")


# 💬 Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()

    # 1️⃣ GREETINGS
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon"]

    if any(word in user_message for word in greetings):
        return jsonify({
            "reply": "👋 Hello! I'm your NLP Assistant 🤖\n\nAsk me anything about Natural Language Processing.",
            "suggestions": [
                "What is NLP?",
                "What is tokenization?",
                "What is sentiment analysis?"
            ]
        })

    # 2️⃣ INTRO
    if "who are you" in user_message or "what can you do" in user_message:
        return jsonify({
            "reply": "🤖 I am an NLP Assistant. I help you understand Natural Language Processing concepts.",
            "suggestions": [
                "What is NLP?",
                "Applications of NLP",
                "NLP techniques"
            ]
        })

    # 3️⃣ DOMAIN CHECK (NLP only)
    allowed_topics = [
        "nlp", "language", "text", "tokenization",
        "stemming", "lemmatization", "pos",
        "ner", "sentiment", "corpus",
        "chatbot", "translation", "summarization",
        "embedding", "machine learning", "deep learning",
        "bert", "gpt", "transformer"
    ]

    if not any(topic in user_message for topic in allowed_topics):
        return jsonify({
            "reply": "🚫 I can only answer questions related to NLP.",
            "suggestions": [
                "What is NLP?",
                "What is tokenization?",
                "Applications of NLP"
            ]
        })

    # 4️⃣ MAIN AI RESPONSE (WITH KNOWLEDGE BASE)
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an NLP Tutor.

Rules:
- Keep answers simple and educational
- Focus on defensive security
- Do NOT provide hacking steps
- Stay within ethical boundaries
- Answer only from given knowledge if possible
- Keep answers simple
- Focus on concepts of NLP
"""
                },
                {
                    "role": "user",
                    "content": f"""
Use this knowledge:

{knowledge}

Question: {user_message}
"""
                }
            ]
        )

        reply = completion.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": "⚠️ Error connecting to AI.",
            "suggestions": []
        })

    # 🎯 Dynamic Suggestions
    suggestions = [
        "What is tokenization?",
        "What is stemming?",
        "What is NLP?"
    ]

    if "token" in user_message:
        suggestions = [
            "Types of tokenization",
            "Why tokenization is important",
            "Examples of tokenization"
        ]

    elif "stem" in user_message or "lemma" in user_message:
        suggestions = [
            "Difference between stemming and lemmatization",
            "Examples of stemming",
            "Why lemmatization is better"
        ]

    elif "sentiment" in user_message:
        suggestions = [
            "Types of sentiment analysis",
            "Applications of sentiment analysis",
            "How sentiment analysis works"
        ]

    elif "chatbot" in user_message:
        suggestions = [
            "What is a chatbot?",
            "Types of chatbots",
            "Uses of chatbots"
        ]

    elif "bert" in user_message or "gpt" in user_message:
        suggestions = [
            "What is BERT?",
            "What is GPT?",
            "What is transformer?"
        ]

    return jsonify({
        "reply": reply,
        "suggestions": suggestions
    })


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True, port=5500)