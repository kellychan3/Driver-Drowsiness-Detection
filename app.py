import streamlit as st
import cv2
import tempfile
import time
import mediapipe as mp
import numpy as np

# Inisialisasi Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Fungsi EAR sederhana (versi ilustrasi)
def calculate_ear(landmarks, eye_indices):
    eye = np.array([landmarks[i] for i in eye_indices])
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Indeks landmark untuk mata dan mulut (Mediapipe)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

st.title("Drowsiness Detection")
st.markdown("Pendeteksian kantuk dengan indikator berupa **kedipan mata** dan **menguap**.")

uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()

    drowsy_count = 0
    drowsy_total_duration = 0
    start_drowsy_time = None

    EAR_THRESHOLD = 0.25
    YAWN_THRESHOLD = 25  # Jarak antar bibir
    FRAME_THRESHOLD = 15
    closed_eyes_frame = 0
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                landmarks = [(int(l.x * w), int(l.y * h)) for l in face_landmarks.landmark]

                left_ear = calculate_ear(landmarks, LEFT_EYE)
                right_ear = calculate_ear(landmarks, RIGHT_EYE)
                avg_ear = (left_ear + right_ear) / 2.0

                top_lip = landmarks[13][1]
                bottom_lip = landmarks[14][1]
                mouth_open = abs(top_lip - bottom_lip)

                is_drowsy = avg_ear < EAR_THRESHOLD or mouth_open > YAWN_THRESHOLD

                if is_drowsy:
                    closed_eyes_frame += 1
                    if closed_eyes_frame >= FRAME_THRESHOLD:
                        text = "DROWSY ALERT!"
                        font_scale = 2.0
                        thickness = 3
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        padding = 10

                        # Ukur ukuran teks
                        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

                        # Hitung posisi kotak dengan padding
                        top_left = (50, 50)
                        bottom_right = (
                            top_left[0] + text_width + 2 * padding,
                            top_left[1] + text_height + 2 * padding
                        )

                        # Gambar kotak putih dengan padding
                        cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), -1)

                        # Gambar teks di atas kotak, digeser agar sesuai padding
                        text_position = (top_left[0] + padding, top_left[1] + text_height + padding)
                        cv2.putText(frame, text, text_position, font, font_scale, (0, 0, 255), thickness)

                        if start_drowsy_time is None:
                            start_drowsy_time = time.time()

                else:
                    if start_drowsy_time:
                        drowsy_duration = time.time() - start_drowsy_time
                        drowsy_total_duration += drowsy_duration
                        drowsy_count += 1
                        start_drowsy_time = None
                    closed_eyes_frame = 0

        # Tampilkan frame
        stframe.image(frame, channels="BGR")

    cap.release()
    st.success(f"Deteksi selesai.")
    st.write(f"Jumlah Kantuk Terdeteksi: **{drowsy_count} kali**")
    st.write(f"Total Durasi Kantuk: **{drowsy_total_duration:.2f} detik**")