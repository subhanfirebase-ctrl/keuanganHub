import os
from flask import Flask, render_template_string, request
from google import genai
from google.genai import types

app = Flask(__name__)

# Tampilan halaman chat interaktif (HTML & CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>keuanganHub AI Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f5f7fb; margin: 0; padding: 15px; color: #333; }
        .chat-container { max-width: 600px; margin: 0 auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; display: flex; flex-direction: column; height: 90vh; }
        .header { background: #2c3e50; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 1.1em; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; background: #fdfdfd; display: flex; flex-direction: column; gap: 15px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 85%; word-wrap: break-word; line-height: 1.5; }
        .user-msg { background: #e1f5fe; color: #0277bd; align-self: flex-end; font-weight: 500; }
        .ai-msg { background: #f1f1f1; color: #2c3e50; align-self: flex-start; white-space: pre-wrap; }
        .form-container { padding: 12px; background: #fff; border-top: 1px solid #eee; }
        form { display: flex; gap: 8px; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; outline: none; }
        input[type="text"]:focus { border-color: #3498db; }
        button { background: #3498db; color: white; border: none; padding: 0 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button:active { background: #2980b9; }
        .error { color: #c0392b; background: #f9d5d5; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">📊 keuanganHub AI Chat Pakar</div>
    
    <div class="chat-box">
        {% if user_input %}
            <div class="message user-msg">{{ user_input }}</div>
        {% endif %}
        
        {% if error_msg %}
            <div class="error">{{ error_msg }}</div>
        {% elif ai_response %}
            <div class="message ai-msg">{{ ai_response }}</div>
        {% else %}
            <div class="message ai-msg" style="background: #fff8e1; color: #b78103;">
                👋 Halo! Saya Pakar Ekonomi Senior & Syariah. Silakan ketik pertanyaan seputar ekonomi, keuangan, atau UMKM di bawah ini, lalu klik Kirim!
            </div>
        {% endif %}
    </div>

    <div class="form-container">
        <form method="POST">
            <input type="text" name="pertanyaan" placeholder="Tanya sesuatu ke AI..." required autocomplete="off">
            <button type="submit">Kirim</button>
        </form>
    </div>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    user_input = None
    ai_response = None
    error_msg = None

    if request.method == 'POST':
        user_input = request.form.get('pertanyaan')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            error_msg = "Waduh! API Key belum terpasang di Vercel."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

        try:
            client = genai.Client(api_key=api_key)
            konfigurasi_ai = types.GenerateContentConfig(
                system_instruction=(
                    "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. "
                    "Berikan analisis yang tajam, profesional, namun mudah dipahami awam. Fokus pada isu makro, "
                    "UMKM, keuangan digital, dan Ekonomi Islam. Berikan contoh riil di Indonesia."
                ),
                temperature=0.7,
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
                config=konfigurasi_ai
            )
            ai_response = response.text

        except Exception as e:
            error_msg = f"Terjadi kesalahan teknis: {str(e)}"

    return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
