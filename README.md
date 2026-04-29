# Bike Sharing Dashboard ✨

## Deskripsi Proyek
Proyek ini merupakan analisis data dari dataset Bike Sharing untuk memahami pola peminjaman sepeda berdasarkan tipe hari, waktu, serta kondisi lingkungan. Hasil analisis disajikan dashboard interaktif.

## Struktur Folder
- `/dashboard`: Berisi file dashboard Streamlit dan dataset.
- `notebook.ipynb`: Analisis data lengkap.
- `README.md`: Dokumentasi proyek.
- `requirements.txt`: Daftar library python yang dibutuhkan.

## Persiapan Lingkungan
### 1. Masuk ke Direktori Proyek
Buka terminal lalu masuk ke folder project ini:
```bash
cd Analisis-Data
```

### 2. Menggunakan Anaconda
```bash
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

### 2. Menggunakan Virtual Environment (venv)
```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate     # Untuk Windows
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit
jalankan perintah berikut di direktori utama:
```bash
streamlit run dashboard/dashboard.py