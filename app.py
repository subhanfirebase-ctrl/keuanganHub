import os
from flask import Flask, render_template_string, request
from google import import os
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
from google.genai import types

app = Flask(__name__)

# Tampilan halaman chat interaktif + Animasi Grafik Naik
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
        form { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 14px; border: 1px solid #ccc; border-radius: 24px; font-size: 16px; outline: none; transition: 0.2s; }
        input[type="text"]:focus { border-color: #2a5298; box-shadow: 0 0 0 3px rgba(42,82,152,0.1); }
        button { background: #2a5298; color: white; border: none; padding: 0 22px; border-radius: 24px; font-size: 15px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #1e3c72; }
        
        /* Gaya Animasi Loading Grafik Keuangan Naik */
        .loading-box { display: none; align-self: flex-start; background: #f8f9fa; padding: 15px 20px; border-radius: 12px; border: 1px solid #eaeaea; max-width: 85%; }
        .loading-text { font-size: 14px; color: #666; margin-bottom: 10px; font-style: italic; display: flex; align-items: center; gap: 5px; }
        
        .chart-animation { display: flex; align-items: flex-end; gap: 4px; height: 30px; width: 50px; padding-left: 5px; border-left: 2px solid #ccc; border-bottom: 2px solid #ccc; }
        .bar { width: 8px; background: #2a5298; border-top-left-radius: 2px; border-top-right-radius: 2px; animation: growUp 1s ease-in-out infinite alternate; transform-origin: bottom; }
        .bar1 { height: 30%; animation-delay: 0.1s; background: #4a76a8; }
        .bar2 { height: 60%; animation-delay: 0.3s; background: #3a6394; }
        .bar3 { height: 90%; animation-delay: 0.5s; background: #2a5298; }
        
        @keyframes growUp {
            0% { transform: scaleY(0.3); }
            100% { transform: scaleY(1); }
        }
        
        .error { color: #721c24; background: #f8d7da; padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">📊 keuanganHub AI Chat v2</div>
    
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
                👋 Selamat datang! Saya AI Pakar Ekonomi Senior. Silakan ketikkan pertanyaanmu di bawah (misal: "Tips UMKM bertahan saat inflasi") lalu amati grafik loadingnya bekerja!
            </div>
        {% endif %}
        
        <!-- Wadah Loading Grafik (Akan muncul via JS saat klik Kirim) -->
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
        <form method="POST" id="chatForm" onsubmit="tampilkanLoading()">
            <input type="text" name="pertanyaan" placeholder="Ketik pesan di sini..." required autocomplete="off" id="inputSaja">
            <button type="submit" id="tombolKirim">Kirim</button>
        </form>
    </div>
</div>

<script>
    // JavaScript untuk memicu animasi loading grafik naik saat form dikirim
    function tampilkanLoading() {
        var loadingBox = document.getElementById('loadingBox');
        var chatBox = document.getElementById('chatBox');
        var inputSaja = document.getElementById('inputSaja');
        var tombolKirim = document.getElementById('tombolKirim');
        
        // 1. Tampilkan animasi grafik keuangan
        loadingBox.style.display = 'block';
        
        // 2. Kunci input & tombol biar user tidak kirim berkali-kali saat proses
        inputSaja.disabled = true;
        tombolKirim.disabled = true;
        tombolKirim.innerText = "...";
        
        // 3. Gulirkan layar otomatis ke bawah agar animasi langsung terlihat di HP
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Menjaga posisi scroll tetap di bawah jika kontennya panjang
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
    app.run(host='0.0.0.0', port=port)ader-title">keuanganHub AI</div>
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
                👋 Selamat datang di ruangan chat keuanganHub! Saya AI Pakar Ekonomi. Ajukan pertanyaan seputar keuangan atau bisnis, lalu klik ikon pesawat di pojok kanan bawah untuk mengirim!
            </div>
        {% endif %}
        
        <!-- Wadah Loading Grafik -->
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
        
        // Cek dulu apakah input kosong atau hanya berisi spasi
        if (inputSaja.value.trim() === "") {
            return false;
        }

        var loadingBox = document.getElementById('loadingBox');
        var chatBox = document.getElementById('chatBox');
        var tombolKirim = document.getElementById('tombolKirim');
        
        // Memunculkan kotak animasi grafik
        loadingBox.style.display = 'block';
        
        // Memodifikasi visual tombol kirim saat memproses data
        tombolKirim.style.background = '#ccc';
        tombolKirim.innerHTML = '<span style="font-size:12px;">...</span>';
        
        // Menggulung layar otomatis ke bawah
        chatBox.scrollTop = chatBox.scrollHeight;
        
        // PERBAIKAN UTAMA: Biarkan form mengirimkan data terlebih dahulu, jangan dikunci di sini.
        return true; 
    }

    // Memastikan scroll berada di posisi paling bawah saat halaman selesai dimuat
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
        
        # Pengaman jika data string yang masuk ternyata kosong
        if not user_input or user_input.strip() == "":
            error_msg = "Waduh! Pertanyaan tidak boleh kosong."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)
            
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
    app.run(host='0.0.0.0', port=port)        button:active { transform: scale(0.95); }
        button svg { width: 22px; height: 22px; fill: currentColor; margin-left: 2px; }
        
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
        
        .error { color: #721c24; background: #f8d7da; padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; }
    </style>
</head>
<body>

<div class="chat-container">
    <!-- Header dengan Logomu yang otomatis memanggil file dari repositori -->
    <div class="header">
        <img src="https://raw.githubusercontent.com/subhanfirebase-ctrl/keuanganHub/main/194606-removebg-preview.png" alt="Logo" onerror="this.src='https://cdn-icons-png.flaticon.com/512/2942/2942946.png';">
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
                👋 Selamat datang di ruangan chat keuanganHub! Saya AI Pakar Ekonomi. Ajukan pertanyaan seputar keuangan atau bisnis, lalu klik ikon pesawat di pojok kanan bawah untuk mengirim!
            </div>
        {% endif %}
        
        <!-- Wadah Loading Grafik -->
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
        <form method="POST" id="chatForm" onsubmit="tampilkanLoading()">
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
        var loadingBox = document.getElementById('loadingBox');
        var chatBox = document.getElementById('chatBox');
        var inputSaja = document.getElementById('inputSaja');
        var tombolKirim = document.getElementById('tombolKirim');
        
        loadingBox.style.display = 'block';
        inputSaja.disabled = true;
        tombolKirim.disabled = true;
        
        tombolKirim.style.background = '#ccc';
        tombolKirim.innerHTML = '<span style="font-size:12px;">...</span>';
        
        chatBox.scrollTop = chatBox.scrollHeight;
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
