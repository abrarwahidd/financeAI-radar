import os
import json
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# Muat Environment Variables
load_dotenv(override=True)

# Setup Client API
# Client Cloud (Gemini API) untuk ekstraksi JSON ringan
gemini_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Client Lokal (ollama) untuk analisis
local_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

# Fungsi Web Scraper Sederhana
def fetch_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text[:12000] 
    except Exception as e:
        return f"Error mengambil data: {e}"

# Agen Ekstraktor (Memaksa Mode JSON)
def extract_json_data(raw_text):
    system_prompt = """
    Anda adalah sistem ekstraksi data fundamental saham. Temukan metrik kunci dari teks.
    Keluarkan HANYA format JSON valid.
    
    Contoh Output:
    {
      "perusahaan": "Nama Perusahaan",
      "laba_bersih": "Angka laba/rugi",
      "pertumbuhan": "Persentase",
      "poin_krusial": ["Poin 1", "Poin 2"]
    }
    """
    try:
        response = gemini_client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ekstrak ini:\n\n{raw_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})

# Agen Analis (Generator dengan kata kunci 'yield' untuk Streaming)
def analyze_and_stream(url):
    # Tahap A: Scraping
    raw_html = fetch_article(url)
    if "Error" in raw_html:
        yield raw_html
        return
        
    yield "### Membaca data metrik keuangan (Gemini)..."
    
    # Tahap B: Ekstraksi JSON
    json_string = extract_json_data(raw_html)
    
    yield f"### Data Fundamental Terkumpul:\n```json\n{json_string}\n```\n\n### Menyusun Analisis Eksekutif (Llama 3.2)...\n"
    
    # Tahap C: Sintesis Lokal dengan Llama 3.2
    system_prompt = """
    Anda adalah analis fundamental saham senior. Baca data JSON yang diberikan.
    Berikan analisis tajam, objektif, dan profesional mengenai prospek perusahaan.
    Gunakan format Markdown yang rapi.
    """
    
    stream = local_client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analisis data berikut: {json_string}"}
        ],
        stream=True
    )
    
    # Menangkap potongan kata dari model lokal dan menampilkannya seketika
    final_output = f"### Data Fundamental Terkumpul:\n```json\n{json_string}\n```\n\n---\n\n"
    for chunk in stream:
        final_output += chunk.choices[0].delta.content or ""
        yield final_output

# 6. Desain Antarmuka Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# FinanceAI Radar")
    gr.Markdown("Masukkan tautan berita rilis laporan keuangan. Sistem akan menarik data via Cloud dan menganalisisnya secara lokal.")
    
    with gr.Row():
        url_input = gr.Textbox(label="URL Berita Keuangan", placeholder="Masukkan tautan di sini...")
        submit_btn = gr.Button("Analisis", variant="primary")
        
    output_markdown = gr.Markdown(label="Hasil Analisis")
    
    # Routing input dan output ke fungsi generator
    submit_btn.click(fn=analyze_and_stream, inputs=url_input, outputs=output_markdown)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)