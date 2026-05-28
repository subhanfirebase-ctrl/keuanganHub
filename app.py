import os
from flask import Flask
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route('/')
def home():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "API Key belum terpasang di Vercel!"

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Bagaimana peluang Ekonomi Syariah digital di Indonesia?"
        )
        return f"<h1>📊 keuanganHub AI</h1><p>{response.text}</p>"
    except Exception as e:
        return f"Error: {str(e)}"
