import streamlit as st
import tempfile
import os
import pandas as pd
from io import BytesIO
from datetime import datetime
from utils import process_video  

# --- Konfigurasi halaman ---
st.set_page_config(page_title="🚗 Deteksi Kantuk Pengemudi", layout="wide")

# --- Header dengan gaya HTML ---
st.markdown("""
    <h1 style='text-align: center; color: navy;'>🚘 Deteksi Kantuk Pengemudi</h1>
    <p style='text-align: center; font-size:18px'>
        Unggah satu atau beberapa video untuk mendeteksi kantuk berdasarkan analisis mata dan mulut.
    </p>
    <hr style='border:1px solid #bbb'/>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("📌 Tentang Aplikasi")
    st.info("Aplikasi ini menggunakan MediaPipe & OpenCV untuk mendeteksi tanda kantuk dengan parameter seperti kedipan mata dan menguap.")
    st.markdown("**Pengembang:** Kelly Chan")
    st.markdown("**Kelas:** 4 TI A")

# --- Inisialisasi session state ---
if "results" not in st.session_state:
    st.session_state.results = []

# --- Upload video ---
uploaded_files = st.file_uploader("📤 Silakan Upload Video (.mp4)", type=["mp4"], accept_multiple_files=True)

# --- Tombol Deteksi ---
if uploaded_files and st.button("🚦 Deteksi Sekarang"):
    st.info("⏳ Harap menunggu, video sedang diproses...")

    results = []
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for file in uploaded_files:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        output_path = os.path.join(output_dir, f"detected_{file.name}")

        drowsy_count, drowsy_duration = process_video(tfile.name, output_path)

        results.append({
            "nama_file": file.name,
            "jumlah_kantuk": drowsy_count,
            "durasi_kantuk": drowsy_duration,
            "output_video": output_path
        })

    st.session_state.results = results
    st.success("✅ Deteksi Kantuk Selesai!")

# --- Tampilkan hasil deteksi jika ada ---
if st.session_state.results:
    today = datetime.today().strftime("%Y-%m-%d")

    # Data untuk Excel
    df = pd.DataFrame([
        {
            "Tanggal Deteksi": today,
            "Nama File": r["nama_file"],
            "Durasi Kantuk (detik)": r["durasi_kantuk"],
            "Jumlah Kantuk Terdeteksi": r["jumlah_kantuk"]
        }
        for r in st.session_state.results
    ])

    # Buffer Excel
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, sheet_name="Hasil Deteksi")
    excel_buffer.seek(0)

    # Tampilkan tombol download di atas hasil
    st.markdown("### 📥 Download Laporan")
    st.download_button(
        label="Download Hasil sebagai Excel",
        data=excel_buffer,
        file_name=f"hasil_deteksi_{today}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")

    # Statistik ringkas
    st.markdown("### 📊 Ringkasan Deteksi")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Video", len(st.session_state.results))
    col2.metric("Total Kantuk", sum([r["jumlah_kantuk"] for r in st.session_state.results]))
    col3.metric("Durasi Kantuk", sum([r["durasi_kantuk"] for r in st.session_state.results]))

    # Detail video per file
    st.markdown("### 🎥 Hasil Deteksi per Video")
    for res in st.session_state.results:
        with st.expander(f"📄 {res['nama_file']}"):
            col1, col2, col3 = st.columns([2, 2, 4])
            col1.metric("Jumlah Kantuk Terdeteksi", res["jumlah_kantuk"])
            col2.metric("Durasi Kantuk", f"{res['durasi_kantuk']} detik")
            with open(res["output_video"], 'rb') as video_file:
                video_bytes = video_file.read()
                col3.video(video_bytes)
