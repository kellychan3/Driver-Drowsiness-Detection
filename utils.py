import cv2
import mediapipe as mp
import numpy as np
import time

# EAR dan landmark
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH = [13, 14]

def calculate_ear(landmarks, eye_indices):
    eye = np.array([landmarks[i] for i in eye_indices])
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    original_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Resize output to 50% for compression
    new_w = original_w // 2
    new_h = original_h // 2

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_w, new_h))

    EAR_THRESHOLD = 0.25
    YAWN_THRESHOLD = 25
    FRAME_THRESHOLD = 15

    drowsy_count = 0
    drowsy_duration = 0
    closed_eyes_frame = 0
    start_drowsy_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for faster processing and smaller output
        frame = cv2.resize(frame, (new_w, new_h))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h_img, w_img, _ = frame.shape
                landmarks = [(int(p.x * w_img), int(p.y * h_img)) for p in face_landmarks.landmark]

                left_ear = calculate_ear(landmarks, LEFT_EYE)
                right_ear = calculate_ear(landmarks, RIGHT_EYE)
                avg_ear = (left_ear + right_ear) / 2.0

                mouth_open = abs(landmarks[MOUTH[0]][1] - landmarks[MOUTH[1]][1])
                is_drowsy = avg_ear < EAR_THRESHOLD or mouth_open > YAWN_THRESHOLD

                if is_drowsy:
                    closed_eyes_frame += 1
                    if closed_eyes_frame >= FRAME_THRESHOLD:
                        cv2.putText(frame, "DROWSY ALERT!", (30, 80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                        if start_drowsy_time is None:
                            start_drowsy_time = time.time()
                else:
                    if start_drowsy_time:
                        drowsy_duration += time.time() - start_drowsy_time
                        drowsy_count += 1
                        start_drowsy_time = None
                    closed_eyes_frame = 0

        out.write(frame)

    cap.release()
    out.release()
    return drowsy_count, round(drowsy_duration, 2)
