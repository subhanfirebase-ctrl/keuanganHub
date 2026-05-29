import os
from flask import Flask, render_template_string, request
from openai import OpenAI

app = Flask(__name__)

# UI Premium & Profesional Full Screen (Tanpa Jendela Mengambang)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>keuanganHub AI — Ruang Analisis Finansial & Syariah</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-canvas: #ffffff;
            --primary: #1e3a8a;
            --primary-light: #eff6ff;
            --accent: #10b981;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Top Navigation Bar */
        .navbar {
            background-color: var(--bg-canvas);
            border-bottom: 1px solid var(--border);
            padding: 0 24px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--primary);
            letter-spacing: -0.5px;
        }

        .brand span {
            color: var(--accent);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            color: var(--text-muted);
            background: #f1f5f9;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 500;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent);
            border-radius: 50%;
        }

        /* Main Workspace - Full Screen Container */
        .workspace {
            flex: 1;
            display: flex;
            flex-direction: column;
            background-color: var(--bg-canvas);
            position: relative;
            height: calc(100vh - 64px);
        }

        /* Chat Stream Area */
        .chat-stream {
            flex: 1;
            overflow-y: auto;
            padding: 40px 24px;
            display: flex;
            flex-direction: column;
            gap: 32px;
        }

        /* Row Base Layout (ChatGPT Style) */
        .message-row {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            gap: 20px;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
            flex-shrink: 0;
        }

        .user-row .avatar {
            background-color: #dbeafe;
            color: #1e40af;
        }

        .ai-row .avatar {
            background-color: var(--primary-light);
            color: var(--primary);
            border: 1px solid #bfdbfe;
        }

        .message-content {
            flex: 1;
            line-height: 1.7;
            font-size: 1.05rem;
            word-wrap: break-word;
        }

        .user-row .message-content {
            color: var(--text-main);
            font-weight: 500;
        }

        .ai-row .message-content {
            color: #1e293b;
            white-space: pre-wrap;
        }

        /* Formatting Bullet Points & Lists */
        .ai-row .message-content ul, .ai-row .message-content ol {
            margin-left: 20px;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        /* Quick Suggestions Area */
        .suggestions-container {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px;
            margin-top: auto;
            padding: 20px 0 0 0;
        }

        .suggestion-card {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            padding: 16px;
            border-radius: 12px;
            cursor: pointer;
            text-align: left;
            font-size: 0.95rem;
            font-weight: 500;
            color: #334155;
            transition: all 0.2s ease;
        }

        .suggestion-card:hover {
            border-color: var(--primary);
            background-color: var(--primary-light);
            transform: translateY(-2px);
        }

        /* Footer Input Panel */
        .input-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 25%);
            padding: 24px;
            flex-shrink: 0;
        }

        .input-container-wrapper {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            position: relative;
        }

        .input-bar-form {
            display: flex;
            background: var(--bg-canvas);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 10px 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.04);
            align-items: center;
            gap: 12px;
            transition: border-color 0.2s;
        }

        .input-bar-form:focus-within {
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(30,58,138,0.08);
        }

        .input-bar-form input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 1.05rem;
            padding: 8px 4px;
            color: var(--text-main);
            background: transparent;
        }

        .send-button {
            background-color: var(--primary);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background 0.2s;
            flex-shrink: 0;
        }

        .send-button:hover { background-color: #172554; }
        .send-button svg { width: 18px; height: 18px; fill: currentColor; }

        /* Modern Loading Bar Indicator */
        .loading-row {
            display: none;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            gap: 20px;
            align-items: center;
        }

        .loading-pulse {
            display: flex;
            gap: 6px;
        }

        .pulse-dot {
            width: 10px;
            height: 10px;
            background-color: var(--primary);
            border-radius: 50%;
            animation: pulse 1.4s infinite ease-in-out both;
        }

        .pulse-dot:nth-child(1) { animation-delay: -0.32s; }
        .pulse-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes pulse {
            0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
            40% { transform: scale(1); opacity: 1; }
        }

        .error-banner {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            background-color: #fef2f2;
            border: 1px solid #fee2e2;
            color: #991b1b;
            padding: 16px;
            border-radius: 12px;
            font-size: 0.95rem;
        }

        @media (max-width: 768px) {
            .suggestions-container { grid-template-columns: 1fr; }
            .chat-stream { padding: 20px 16px; }
            .message-row { gap: 12px; }
        }
    </style>
</head>
<body>

    <!-- Top Navigation Bar -->
    <nav class="navbar">
        <div class="brand">
            keuangan<span>Hub</span> <small style="font-weight:400; font-size:0.8rem; color:var(--text-muted);">Console v2.0</small>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            Llama 3.3 Engine Active
        </div>
    </nav>

    <!-- Full Screen Workspace -->
    <div class="workspace">
        <div class="chat-stream" id="chatStream">
            
            {% if not user_input and not ai_response and not error_msg %}
                <!-- Welcome State -->
                <div class="message-row ai-row" style="margin-top: 40px;">
                    <div class="avatar">AI</div>
                    <div class="message-content">
                        <h2 style="margin-bottom: 8px; font-size: 1.5rem; color: var(--primary);">Selamat Datang di Ruang Analisis Premium</h2>
                        Halo kawan! Saya adalah AI Pakar Ekonomi Senior dan Spesialis Keuangan Syariah. Sistem layar penuh siap membantu kamu melakukan riset pasar, penyusunan strategi bisnis UMKM, manajemen portofolio, hingga kepatuhan finansial syariah. Silakan ajukan pertanyaanmu di bawah.
                    </div>
                </div>

                <!-- Quick Prompts Suggestions -->
                <div class="suggestions-container" id="suggestBox">
                    <button class="suggestion-card" onclick="isiPertanyaan('Bagaimana strategi mengelola arus kas (cashflow) bagi UMKM yang baru mulai?')">
                        <strong>📊 Manajemen UMKM</strong>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">Strategi arus kas bagi usaha mikro berkembang.</p>
                    </button>
                    <button class="suggestion-card" onclick="isiPertanyaan('Apa saja syarat mutlak sebuah transaksi bisnis dikategorikan sah dan halal dalam Ekonomi Syariah?')">
                        <strong>🌙 Prinsip Syariah</strong>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">Syarat mutlak kehalalan akad transaksi komersial.</p>
                    </button>
                    <button class="suggestion-card" onclick="isiPertanyaan('Berikan analisis dampak inflasi global terhadap instrumen investasi lokal di Indonesia.')">
                        <strong>📈 Makro Ekonomi</strong>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">Dampak inflasi pada pasar reksadana dan obligasi.</p>
                    </button>
                </div>
            {% endif %}

            <!-- Dynamic Conversation Stream -->
            {% if user_input %}
                <div class="message-row user-row">
                    <div class="avatar">Kamu</div>
                    <div class="message-content">{{ user_input }}</div>
                </div>
            {% endif %}
            
            {% if error_msg %}
                <div class="error-banner">⚠️ {{ error_msg }}</div>
            {% elif ai_response %}
                <div class="message-row ai-row">
                    <div class="avatar">AI</div>
                    <div class="message-content" id="aiReplyArea">{{ ai_response }}</div>
                </div>
            {% endif %}
            
            <!-- Loading Row Tracker -->
            <div class="message-row loading-row" id="loadingRow">
                <div class="avatar" style="background:#f1f5f9; color:#94a3b8;">...</div>
                <div class="loading-pulse">
                    <div class="pulse-dot"></div>
                    <div class="pulse-dot"></div>
                    <div class="pulse-dot"></div>
                </div>
            </div>

        </div>

        <!-- Sticky Bottom Input Form Panel -->
        <div class="input-panel">
            <div class="input-container-wrapper">
                <form method="POST" id="coreForm" class="input-bar-form" onsubmit="return triggerLoading()">
                    <input type="text" name="pertanyaan" id="mainInputField" placeholder="Ketik instruksi analisis keuangan atau bisnis di sini..." required autocomplete="off">
                    <button type="submit" class="send-button" id="sendBtn" title="Kirim Analisis">
                        <svg viewBox="0 0 24 24">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script>
        // Fungsi untuk memasukkan teks rekomendasi instan ke dalam form
        function isiPertanyaan(teks) {
            document.getElementById('mainInputField').value = teks;
            document.getElementById('coreForm').submit();
            triggerLoading();
        }

        // Efek loading animasi modern saat submit data
        function triggerLoading() {
            var input = document.getElementById('mainInputField');
            if (input.value.trim() === "") return false;

            document.getElementById('loadingRow').style.display = 'flex';
            var sBox = document.getElementById('suggestBox');
            if(sBox) sBox.style.display = 'none';

            var btn = document.getElementById('sendBtn');
            btn.style.backgroundColor = '#94a3b8';
            btn.disabled = true;

            var stream = document.getElementById('chatStream');
            stream.scrollTop = stream.scrollHeight;
            return true;
        }

        // Paksa scrollbar otomatis berada di paling bawah jawaban terbaru
        var streamContainer = document.getElementById('chatStream');
        streamContainer.scrollTop = streamContainer.scrollHeight;
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
            error_msg = "Pertanyaan tidak boleh kosong, kawan."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)
            
        api_key = os.environ.get("CADANGAN_API_KEY")
        
        if not api_key:
            error_msg = "Kunci Akses API (CADANGAN_API_KEY) belum terkonfigurasi di Vercel kawan."
            return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

        try:
            # Bypass setelan proxy lingkungan serverless Vercel
            import httpx
            http_client = httpx.Client(proxies={})

            client = OpenAI(
                base_url="https://api.groq.com/openai/v1", 
                api_key=api_key,
                http_client=http_client
            )
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. Berikan analisis yang tajam, profesional, menggunakan format poin-poin yang rapi, dan mudah dipahami awam. Berikan contoh riil di Indonesia."
                    },
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message.content

        except Exception as e:
            error_msg = f"Terjadi gangguan pada jalur transmisi data AI: {str(e)}"

    return render_template_string(HTML_TEMPLATE, user_input=user_input, ai_response=ai_response, error_msg=error_msg)

app = app
