<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ API key not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

# 📚 Load Knowledge Base
knowledge = ""
folder_path = "Knowledge_base"

if os.path.exists(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                knowledge += f.read() + "\n\n"
else:
    print("⚠️ Knowledge_base folder not found")

# 🌐 Home Route
@app.route("/")
def home():
    return render_template("index.html")

# 💬 Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    # ✅ FIX 1: Safely get message, handle None
    data = request.get_json()
    if not data or not data.get("message"):
        return jsonify({"reply": "⚠️ No message received.", "suggestions": []})

    user_message = data["message"].strip().lower()

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

    # 3️⃣ DOMAIN CHECK
    allowed_topics = [
        "nlp", "natural language", "language", "text", "tokenization",
        "stemming", "lemmatization", "pos", "part of speech",
        "ner", "named entity", "sentiment", "corpus",
        "chatbot", "translation", "summarization",
        "embedding", "word2vec", "machine learning", "deep learning",
        "bert", "gpt", "transformer", "attention", "parsing",
        "tagging", "classification", "model", "vector"
    ]

    if not any(topic in user_message for topic in allowed_topics):
        return jsonify({
            "reply": "🚫 I can only answer questions related to NLP (Natural Language Processing). Please ask about NLP topics!",
            "suggestions": [
                "What is NLP?",
                "What is tokenization?",
                "Applications of NLP"
            ]
        })

    # 4️⃣ AI RESPONSE
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an NLP Tutor. Rules:\n"
                        "- Keep answers simple and educational\n"
                        "- Stay within NLP domain only\n"
                        "- Be clear and beginner-friendly\n"
                        "- Use bullet points or short paragraphs\n"
                        "- Do not answer questions outside NLP"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Use this knowledge base if relevant:\n\n{knowledge}\n\n"
                        f"Question: {user_message}"
                    )
                }
            ],
            max_tokens=512,
            temperature=0.7
        )

        reply = completion.choices[0].message.content.strip()

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": "⚠️ Error connecting to AI. Please check your API key and try again.",
            "suggestions": []
        })

    # 🎯 Dynamic Suggestions
    suggestions = ["What is NLP?", "What is tokenization?", "What is stemming?"]

    if "token" in user_message:
        suggestions = [
            "Types of tokenization",
            "Why is tokenization important?",
            "Examples of tokenization"
        ]
    elif "stem" in user_message or "lemma" in user_message:
        suggestions = [
            "Difference between stemming and lemmatization",
            "Examples of stemming",
            "Why is lemmatization better than stemming?"
        ]
    elif "sentiment" in user_message:
        suggestions = [
            "Types of sentiment analysis",
            "Applications of sentiment analysis",
            "How does sentiment analysis work?"
        ]
    elif "chatbot" in user_message:
        suggestions = [
            "What is a chatbot?",
            "Types of chatbots",
            "How do chatbots use NLP?"
        ]
    elif "bert" in user_message or "gpt" in user_message or "transformer" in user_message:
        suggestions = [
            "What is BERT?",
            "What is GPT?",
            "What is a transformer model?"
        ]
    elif "ner" in user_message or "named entity" in user_message:
        suggestions = [
            "What is NER?",
            "Applications of NER",
            "How does NER work?"
        ]
    elif "pos" in user_message or "part of speech" in user_message:
        suggestions = [
            "What is POS tagging?",
            "Types of POS tags",
            "Why is POS tagging useful?"
        ]

    return jsonify({
        "reply": reply,
        "suggestions": suggestions
    })

# ▶️ Run App
if __name__ == "__main__":
=======
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
>>>>>>> 43d8320e54655d2b37a596814a771f35f17fca07
    app.run(debug=True, port=5500)