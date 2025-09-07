# 🚘 Driver Drowsiness Detection
<img width="962" height="805" alt="home" src="https://github.com/user-attachments/assets/8a4e075a-f1eb-452f-af65-fc6baddacc2f" />
<img width="955" height="887" alt="result" src="https://github.com/user-attachments/assets/63fc8666-24d7-4641-b895-2fd26ccdc8ee" />

A web-based app built with **Streamlit** to detect driver drowsiness from video files using **MediaPipe Face Mesh** and **OpenCV**. The system analyzes **eye aspect ratio (EAR)** and **mouth opening (yawn detection)** to identify signs of drowsiness.

# 🔍 Key Features
- 😴 **Drowsiness Detection**: Identifies drowsy behavior via eye blinking and yawning patterns.
- 📊 **Excel Report Export**: Automatically generates a downloadable report of detection results per video.
- 🎥 **Video Processing**: Handles multiple video uploads with per-frame face landmark detection.

# 🛠️ Technologies
- Python 3.x
- Streamlit
- OpenCV
- MediaPipe
- Pandas, NumPy
- Matplotlib, PIL

# 🚀 How to Set up the Project
1. Clone the repository
```
git clone https://github.com/username/drowsy-detection-app.git
cd drowsy-detection-app
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Create an output folder in the project root
```
mkdir output
```

4. Run the Streamlit app
```
streamlit run app.py
```

