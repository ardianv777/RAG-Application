# Aplikasi Demo RAG

Sistem Retrieval-Augmented Generation (RAG) sederhana yang dibangun dengan FastAPI, LangGraph, dan Qdrant. Aplikasi ini memungkinkan user menyimpan dokumen dan memberikan pertanyaan dengan sistem mengambil informasi relevan untuk menghasilkan jawaban.

## Fitur

- 📄 Tambahkan dokumen ke sistem
- 🔍 Berikan pertanyaan dan dapatkan jawaban yang relevan
- 💾 2 Mode penyimpanan: database vektor Qdrant atau fallback in-memory
- ⚡ Respons cepat dengan pengelolaan alur kerja menggunakan LangGraph
- 🎯 Arsitektur bersih dengan pemisahan tugas yang jelas

## Struktur Proyek

```
RAG APPLICATION/
├── api/
│   ├── __pycache__/
│   └── endpoints.py          # Handler endpoint API RAG
├── services/
│   ├── __pycache__/
│   ├── embedding.py          # Pembuatan embedding teks
│   └── rag_system.py         # Logika alur kerja sistem RAG
├── storage/
│   ├── __pycache__/
│   └── document_store.py     # Manajemen penyimpanan dokumen
├── __pycache__/
├── assignment.md             # Instruksi / soal tugas
├── main.py                   # App Launcher
├── models.py                 # Model Pydantic / skema data
├── notes.md                  # Catatan & penjelasan
├── readme.md                 # Dokumentasi proyek
└── requirements.txt          # Daftar dependency
```

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- LangGraph
- Qdrant Client

## Instalasi

### 1. Instal Dependensi

```bash
pip install fastapi uvicorn pydantic langgraph qdrant-client
```

Atau instal dari requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. (Opsional) Jalankan Qdrant

Jika ingin menggunakan database vektor Qdrant daripada penyimpanan in-memory:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Catatan:** Jika Qdrant tidak tersedia, aplikasi akan secara otomatis menggunakan penyimpanan in-memory.

## Cara Menjalankan

Mulai aplikasi dengan Uvicorn:

```bash
uvicorn app.main:app --reload
```

API akan tersedia di: `http://localhost:8000`

**Dokumentasi API:**
- Swagger UI: `http://localhost:8000/docs` - Interface interaktif untuk menguji endpoint API secara langsung
- ReDoc: `http://localhost:8000/redoc` - Interface dokumentasi yang bersih

**Catatan:** User dapat menggunakan `/docs` atau `/redoc` untuk berinteraksi dengan API tanpa perintah curl. Cukup buka URL di browser user dan user dapat menguji semua endpoint secara interaktif.

## Endpoint API

### 1. Periksa Status Sistem

**GET** `/status`

Periksa apakah sistem siap dan mode penyimpanan mana yang aktif.

```bash
curl http://localhost:8000/status
```

**Respons:**
```json
{
  "qdrant_ready": true,
  "in_memory_docs_count": 0,
  "graph_ready": true
}
```

### 2. Tambah Dokumen

**POST** `/add`

Tambahkan dokumen baru ke sistem.

```bash
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"text": "Python adalah bahasa pemrograman tingkat tinggi yang terkenal karena kesederhanaan dan keterbacaannya."}'
```

**Respons:**
```json
{
  "id": 0,
  "status": "added"
}
```

### 3. Ajukan Pertanyaan

**POST** `/ask`

Ajukan pertanyaan dan dapatkan jawaban berdasarkan dokumen yang disimpan.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Apa itu Python?"}'
```

**Respons:**
```json
{
  "question": "Apa itu Python?",
  "answer": "I found this: 'Python adalah bahasa pemrograman tingkat tinggi yang terkenal karena kesederhanaan dan keterbacaannya....'",
  "context_used": [
    "Python adalah bahasa pemrograman tingkat tinggi yang terkenal karena kesederhanaan dan keterbacaannya."
  ],
  "latency_sec": 0.045
}
```

## Contoh Penggunaan

### Metode 1: Menggunakan Dokumentasi Interaktif (Rekomendasi untuk Pemula)

1. **Mulai aplikasi:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Buka Swagger UI di browser:**
   ```
   http://localhost:8000/docs
   ```

3. **Uji endpoint secara interaktif:**
   - Klik pada endpoint apa pun (misalnya, `/add`)
   - Klik "Try it out"
   - Isi badan permintaan
   - Klik "Execute"
   - Lihat respons segera

**Atau gunakan ReDoc untuk tampilan yang lebih bersih:**
   ```
   http://localhost:8000/redoc
   ```

### Metode 2: Menggunakan Perintah cURL

Jika lebih suka command line:

1. **Mulai aplikasi:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Tambahkan beberapa dokumen:**
   ```bash
   # Tambah dokumen tentang Python
   curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"text": "Python adalah bahasa pemrograman yang dibuat oleh Guido van Rossum pada tahun 1991."}'
   
   # Tambah dokumen tentang FastAPI
   curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"text": "FastAPI adalah framework web modern untuk membangun API dengan Python."}'
   ```

3. **Ajukan pertanyaan:**
   ```bash
   # Tanya tentang Python
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Siapa yang membuat Python?"}'
   
   # Tanya tentang FastAPI
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Apa itu FastAPI?"}'
   ```

4. **Periksa status:**
   ```bash
   curl http://localhost:8000/status
   ```

## Arsitektur

Aplikasi mengikuti pola arsitektur bersih dengan pemisahan tanggung jawab yang jelas:

- **Folder API** (`api/`): Menangani permintaan dan respons HTTP
- **Folder Layanan** (`services/`): Berisi logika bisnis (embedding, alur kerja RAG)
- **Folder Penyimpanan** (`storage/`): Mengelola penyimpanan data
- **Model** (`models.py`): Mendefinisikan struktur data dan validasi

## Cara Kerjanya

1. **Penyimpanan Dokumen:** Ketika user menambahkan dokumen, dokumen dikonversi menjadi vektor numerik (embedding) dan disimpan di Qdrant atau penyimpanan in-memory.

2. **Pemrosesan Pertanyaan:** Ketika user memberikan pertanyaan:
   - Pertanyaan dikonversi menjadi vektor
   - Sistem mencari dokumen serupa
   - Dokumen relevan diambil sebagai konteks
   - Jawaban dihasilkan berdasarkan konteks yang diambil

3. **Alur Kerja:** LangGraph mengelola alur kerja retrieve → answer untuk memastikan pemrosesan yang konsisten.

## Pengembangan

### Menjalankan Tes

Saat ini tidak ada tes otomatis. Struktur dirancang untuk mudah diuji, setiap komponen dapat diuji secara independen.

### Menambah Fitur Baru

- **Endpoint baru:** Tambahkan ke `api/endpoints.py`
- **Services baru:** Buat di `services/`
- **Backend storage baru:** Perluas `storage/document_store.py`

## Catatan

- Ini adalah aplikasi demo menggunakan fungsi embedding palsu untuk kesederhanaan
- Untuk penggunaan produksi, ganti `fake_embed()` dengan model embedding yang ada (misalnya, Sentence Transformers, OpenAI embeddings)
- Aplikasi menggunakan pembuatan jawaban sederhana dalam produksi, integrasikan dengan LLM untuk respons yang lebih baik

## Pemecahan Masalah

**Masalah:** Kesalahan koneksi Qdrant

**Solusi:** Pastikan Qdrant berjalan di port 6333, atau biarkan aplikasi menggunakan fallback in-memory.

**Masalah:** Kesalahan modul tidak ditemukan

**Solusi:** Pastikan semua dependensi diinstal: `pip install -r requirements.txt`

**Masalah:** Port 8000 sudah digunakan

**Solusi:** Gunakan port berbeda: `uvicorn app.main:app --port 8001`