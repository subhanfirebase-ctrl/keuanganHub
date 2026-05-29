import os
from flask import Flask, render_template_string, request
from google import genai
from google.genai import types
from openai import OpenAI  # Library untuk memanggil API cadangan

app = Flask(__name__)

# Tampilan halaman chat interaktif + Animasi Grafik Naik (Tanpa Logo)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>keuanganHub AI Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f0f4f8; margin: 0; padding: 10px; color: #333; }
        .chat-container { max-width: 600px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); overflow: hidden; display: flex; flex-direction: column; height: 93vh; }
        .header { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 18px; text-align: center; font-weight: bold; font-size: 1.2em; letter-spacing: 0.5px; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; background: #fdfdfd; display: flex; flex-direction: column; gap: 15px; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; word-wrap: break-word; line-height: 1.6; font-size: 15px; }
        .user-msg { background: #d1ecf1; color: #0c5460; align-self: flex-end; border-bottom-right-radius: 2px; }
        .ai-msg { background: #f8f9fa; color: #2c3e50; align-self: flex-start; border-bottom-left-radius: 2px; white-space: pre-wrap; border: 1px solid #eaeaea; }
        .form-container { padding: 15px; background: #fff; border-top: 1px solid #eee; }
        form { display: flex; gap: 10px; align-items: center; }
        input[type="text"] { flex: 1; padding: 14px; border: 1px solid #ccc; border-radius: 24px; font-size: 16px; outline: none; transition: 0.2s; }
        input[type="text"]:focus { border-color: #2a5298; box-shadow: 0 0 0 3px rgba(42,82,152,0.1); }
        button { background: #2a5298; color: white; border: none; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; padding: 0; flex-shrink: 0; }
        button:hover { background: #1e3c72; }
        button:active { transform: scale(0.95); }
        button svg { width: 22px; height: 22px; fill: currentColor; }
        
        /* Animasi Loading Grafik Keuangan */
        .loading-box { display: none; align-self: flex-start; background: #f8f9fa; padding: 15px 20px; border-radius: 12px; border: 1px solid #eaeaea; max-width: 85%; }
        .loading-text { font-size: 14px; color: #666; margin-bottom: 10px; font-style: italic; }
        .chart-animation { display: flex; align-items: flex-end; gap: 4px; height: 30px; width: 50px; padding-left: 5px; border-left: 2px solid #ccc; border-bottom: 2px solid #ccc; }
        .bar { width: 8px; background: #2a5298; border-top-left-radius: 2px; border-top-right-radius: 2px; animation: growUp 1s ease-in-out infinite alternate; transform-origin: bottom; }
        .bar1 { height: 30%; animation-delay: 0.1s; background: #4a76a8; }
        .bar2 { height: 60%; animation-delay: 0.3s; background: #3a6394; }
        .bar3 { height: 90%; animation-delay: 0.5s; background: #2a5298; }
        
        @keyframes growUp {
            0% { transform: scaleY(0.3); }
            100% { transform: scaleY(1); }
        }
        
        .error { color: #721c24; background: #f8d7da; padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; width: 100%; box-sizing: border-box; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">
        <div class="header-title">keuanganHub AI</div>
    </div>
    
    <div class="chat-box" id="chatBox">
        {% if user_input %}
            <div class="message user-msg">{{ user_input }}</div>
        {% endif %}
        
        {% if error_msg %}
            <div class="error">{{ error_msg }}</div>
        {% elif ai_response %}
            <div class="message ai-msg">{{ ai_response }}</div>
        {% else %}
            <div class="message ai-msg" style="background: #fff9db; color: #856404; border-color: #ffeeba;">
                👋 Selamat datang di ruangan chat keuanganHub! Saya AI Pakar Ekonomi Senior & Syariah. Ajukan pertanyaan seputar keuangan atau bisnis, lalu klik ikon pesawat untuk mengirim!
            </div>
        {% endif %}
        
        <div class="loading-box" id="loadingBox">
            <div class="loading-text">Menganalisis data ekonomi...</div>
            <div class="chart-animation">
                <div class="bar bar1"></div>
                <div class="bar bar2"></div>
                <div class="bar bar3"></div>
            </div>
        </div>
    </div>

    <div class="form-container">
        <form method="POST" id="chatForm" onsubmit="return tampilkanLoading()">
            <input type="text" name="pertanyaan" placeholder="Tanya sesuatu ke AI..." required autocomplete="off" id="inputSaja">
            
            <button type="submit" id="tombolKirim" title="Kirim Pesan">
                <svg viewBox="0 0 24 24">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
                </svg>
            </button>
        </form>
    </div>
</div>

<script>
    function tampilkanLoading() {
        var inputSaja = document.getElementById('inputSaja');
        if (inputSaja.value.trim() === "") {
            return false;
        }

        var loadingBox = document.getElementById('loadingBox');
        var chatBox = document.getElementById('chatBox');
        var tombolKirim = document.getElementById('tombolKirim');
        
        loadingBox.style.display = 'block';
        tombolKirim.style.background = '#ccc';
        tombolKirim.innerHTML = '<span style="font-size:12px; color:white;">...</span>';
        
        chatBox.scrollTop = chatBox.scrollHeight;
        return true; 
    }

    var cb = document.getElementById('chatBox');
    cb.scrollTop = cb.scrollHeight;
</script>

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
        
        if not user_input or user_input.strip() == "":
            error_msg = "Waduh! Pertanyaan tidak boleh kosong."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)
            
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            error_msg = "Waduh! API Key belum terpasang di Vercel."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

        # 1. MENCOBA JALUR UTAMA: GOOGLE GEMINI
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
            # 2. JIKA GEMINI LIMIT (429/503), OTOMATIS LEMPAR KE API CADANGAN (GROQ/OPENROUTER)
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e):
                api_key_cadangan = os.environ.get("CADANGAN_API_KEY") 
                
                if api_key_cadangan:
                    try:
                        # Menggunakan format OpenAI (kompatibel dengan Groq)
                        client_cadangan = OpenAI(
                            base_url="https://api.groq.com/openai/v1", 
                            api_key=api_key_cadangan
                        )
                        
                        response_alt = client_cadangan.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. Berikan analisis yang tajam, profesional, namun mudah dipahami awam. Fokus pada isu makro, UMKM, keuangan digital, dan Ekonomi Islam. Berikan contoh riil di Indonesia."
                                },
                                {"role": "user", "content": user_input}
                            ]
                        )
                        # Ditandai agar kamu tahu sistem fallback-nya bekerja
                        ai_response = "[Mode Cadangan Aktif]\n\n" + response_alt.choices[0].message.content
                    
                    except Exception as err_cadangan:
                        error_msg = f"Server utama sibuk, dan server cadangan mengalami kendala: {str(err_cadangan)}"
                else:
                    error_msg = "Kuota gratis harian Gemini habis, dan kamu belum memasang CADANGAN_API_KEY di Vercel kawan."
            else:
                error_msg = f"Terjadi kesalahan teknis: {str(e)}"

    return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
