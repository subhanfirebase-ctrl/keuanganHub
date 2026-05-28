import os
from google import genai
from google.genai import types

# Mengambil API Key dari sistem server (Cara paling aman)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Waduh, API Key belum terpasang di sistem server!")
    exit()

# Menghubungkan program ke AI Google Gemini
client = genai.Client(api_key=api_key)

# Didik AI agar menjadi Pakar Ekonomi Indonesia & Syariah
konfigurasi_ai = types.GenerateContentConfig(
    system_instruction=(
        "Kamu adalah seorang Ekonom Senior spesialisasi Ekonomi Indonesia dan Ahli Ekonomi Syariah. "
        "Tugasmu adalah memberikan analisis tajam, profesional, namun mudah dipahami masyarakat awam. "
        "Fokuslah pada isu makroekonomi Indonesia, perkembangan UMKM, keuangan digital, serta integrasi "
        "sistem Ekonomi Islam/Syariah di Indonesia. Selalu berikan contoh atau data riil di Indonesia jika memungkinkan."
    ),
    temperature=0.7,
)

# Pertanyaan uji coba otomatis saat pertama kali dinyalakan
pertanyaan = "Bagaimana peluang dan tantangan pengembangan Ekonomi Syariah digital di Indonesia saat ini?"

print(f"Mengajukan Pertanyaan: {pertanyaan}\n")

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=pertanyaan,
    config=konfigurasi_ai
)

print("--- ANALISIS PAKAR AI ---")
print(response.text)
