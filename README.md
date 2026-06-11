# 📈 Financial Radar AI Analyzer

Sebuah aplikasi berbasis *Agentic Workflow* untuk mengekstrak, memfilter, dan menganalisis metrik fundamental saham dari artikel berita atau rilis pers keuangan. Proyek ini mendemonstrasikan orkestrasi antara Cloud AI dan Local LLM untuk efisiensi biaya dan privasi data.

## Alur Kerja Sistem (*Agentic Workflow*)
1. **Data Scraper:** Menarik teks mentah (HTML kotor) dari URL berita keuangan.
2. **Cloud Extractor (Gemini):** Memanfaatkan kecepatan API Cloud dengan teknik *One-Shot Prompting* dan *JSON Mode* untuk menyaring teks kotor menjadi struktur data JSON murni (Laba Bersih, Pertumbuhan, dll).
3. **Local Synthesizer (Llama 3.2):** Menjalankan penalaran analitis secara lokal dan privat menggunakan GPU *host*, menyajikan ringkasan eksekutif dengan efek *streaming typewriter*.

## 🛠️ Tech Stack
* **Bahasa:** Python 3.12+
* **Package Manager:** `uv` 
* **AI Integration:** `openai` Python SDK (API Wrapper Trick)
* **Cloud Model:** Google Gemini 3.1 Flash-lite
* **Local Model:** Llama 3.2 (via Ollama)
* **Antarmuka (UI):** Gradio Web Interface

## ⚙️ *Prerequisites*
* Sistem operasi Windows/Linux/WSL.
* Terinstal `uv` package manager.
* Terinstal **Ollama** dengan model `llama3.2` yang sudah diunduh (`ollama pull llama3.2`) dan berjalan di latar belakang.
* Kunci API Google AI Studio.

## 💻 Cara Instalasi & Menjalankan

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/abrarwahidd/financeAI-radar.git]
   cd financeAI-radar
2. **Aktifkan Virtual Environment dengan menjalankan:**
    ```bash
    uv sync
3. **Konfigurasi .env**  
    Buat file .env di root folder, dan masukkan GEMINI_API_KEY  
    ```bash
    GOOGLE_API_KEY=Masukkan_Kunci_API_Gemini_Disini
4. **Jalankan semua cell nya**
5. **Akses url yang dihasilkan cell terakhir, misal:**  
    ```Plaintext
    http://localhost:0000

