# 🚘 Deteksi Kantuk Pengemudi 
Website ini dibuat menggunakan Streamlit, berfungsi untuk mendeteksi tanda-tanda kantuk pada video pengemudi. Deteksi dilakukan berdasarkan pergerakan mata dan mulut menggunakan MediaPipe Face Mesh dan OpenCV.

# 🔍 Fitur Utama
- 😪 Deteksi Kantuk: Menggunakan rasio EAR (Eye Aspect Ratio) dan jarak antar bibir
- 📁 Laporan Excel Otomatis: Hasil deteksi dapat diekspor

# 🛠️ Teknologi
- Python 3.x
- OpenCV
- MediaPipe
- Streamlit
- Pandas, NumPy

# 🚀 Cara Menjalankan
1. Clone repositori
```
git clone https://github.com/username/drowsy-detection-app.git
cd drowsy-detection-app
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Buat folder output di root proyek

4. Jalankan aplikasi Streamlit
```
streamlit run app.py
```

