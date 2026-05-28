import os
from flask import Flask
from google import genai
from google.genai import types

# Mengaktifkan Flask untuk membuat server web gratis
app = Flask(__name__)

@app.route('/')
def home():
    # Mengambil API Key secara aman dari brankas rahasia Render
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return "<h1>Waduh!</h1><p>API Key belum terpasang di Environment Variables Render.</p>"

    try:
        # Menghubungkan program ke AI Google Gemini resmi
        client = genai.Client(api_key=api_key)
        
        # Didik AI agar menjadi Pakar Ekonomi Senior
        konfigurasi_ai = types.GenerateContentConfig(
            system_instruction=(
                "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. "
                "Tugasmu adalah memberikan analisis yang tajam, profesional, namun mudah dipahami masyarakat awam. "
                "Fokuslah pada isu makroekonomi Indonesia, perkembangan UMKM, keuangan digital, serta integrasi "
                "sistem Ekonomi Islam/Syariah di Indonesia. Selalu berikan contoh atau data riil di Indonesia jika memungkinkan."
            ),
            temperature=0.7,
        )
        
        # Pertanyaan otomatis saat website diakses
        pertanyaan = "Bagaimana peluang dan tantangan pengembangan Ekonomi Syariah digital di Indonesia saat ini?"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=pertanyaan,
            config=konfigurasi_ai
        )
        
        # Menampilkan hasil analisis langsung di layar browser HP
        tampilan_html = f"""
        <html>
            <head>
                <title>keuanganHub - AI Pakar Ekonomi</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
                    .prompt {{ background: #f8f9fa; padding: 10px 15px; border-left: 4px solid #3498db; margin-bottom: 20px; font-style: italic; }}
                    .hasil {{ white-space: pre-wrap; background: #fff; padding: 10px; }}
                </style>
            </head>
            <body>
                <h1>📊 keuanganHub: Analisis Pakar AI Ekonomi</h1>
                <div class="prompt"><strong>Pertanyaan Sistem:</strong> {pertanyaan}</div>
                <div class="hasil">{response.text}</div>
            </body>
        </html>
        """
        return tampilan_html

    except Exception as e:
        return f"<h1>Terjadi Kesalahan Teknis</h1><p>Detail error: {str(e)}</p>"

if __name__ == '__main__':
    # Memastikan aplikasi berjalan menggunakan port yang disediakan oleh Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)print("--- ANALISIS PAKAR AI ---")
print(response.text)
