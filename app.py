import os
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')
@app.route('/', methods=['GET', 'POST'])
def chat():
    user_input = None
    ai_response = None
    error_msg = None

    if request.method == 'POST':
        user_input = request.form.get('pertanyaan')
        
        if not user_input or user_input.strip() == "":
            error_msg = "Pertanyaan tidak boleh kosong, kawan."
            return render_template('index.html', user_input=user_input, ai_response=ai_response, error_msg=error_msg)
            
        api_key = os.environ.get("CADANGAN_API_KEY")
        
        if not api_key:
            error_msg = "Kunci Akses API (CADANGAN_API_KEY) belum dikonfigurasi di Vercel kawan."
            return render_template('index.html', user_input=user_input, ai_response=ai_response, error_msg=error_msg)

        try:
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
                    {"role": "system", "content": "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. Berikan analisis yang tajam, profesional, rapi, dan mudah dipahami."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message.content

        except Exception as e:
            error_msg = f"Terjadi gangguan pada transmisi data AI: {str(e)}"

    # Menggunakan render_template (bukan render_template_string lagi)
    return render_template('index.html', user_input=user_input, ai_response=ai_response, error_msg=error_msg)

app = app
