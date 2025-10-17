# 🚘 Driver Drowsiness Detection


**Table of Contents**

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Scope & Limitations](#scope--limitations)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [How-It-Works](#how-it-works)
- [Conclusion](#conclusion)


## Project Overview

This project is a web-based application built with **Streamlit** that analyzes driver drowsiness from recorded video files. Using **MediaPipe Face Mesh** and **OpenCV**, the system calculates Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) to identify drowsiness indicators such as blinking and yawning.

The system processes post-trip driver videos to produce quantitative results  including the number and duration of drowsiness events. These results are compiled into structured datasets that can be used for further research and behavioral analysis.

<img width="962" height="805" alt="home" src="https://github.com/user-attachments/assets/8a4e075a-f1eb-452f-af65-fc6baddacc2f" />
<img width="955" height="887" alt="result" src="https://github.com/user-attachments/assets/63fc8666-24d7-4641-b895-2fd26ccdc8ee" />

## Problem Statement

Driver drowsiness is a major factor in traffic accidents worldwide. According to the World Health Organization (WHO), approximately **1.35 million people die annually** in road accidents, with fatigue contributing significantly. In Indonesia, around **10% of traffic accidents involve sleepy drivers** (Korlantas Polri).

Frequent yawning and slower blinking are common signs of driver fatigue. By analyzing these behaviors from recorded driving videos, this system provides objective evaluations of drowsiness patterns to support data-driven research on driver alertness.

## Scope & Limitations
**Scope**:
- Detects drowsiness indicators based on eye blinking and yawning patterns.
- Analyzes pre-recorded videos with front-facing views of the driver.
- Processes manually uploaded video files

**Limitations**:
- Only two facial features (eyes and mouth) are analyzed.
- Accuracy may decrease in low lighting, partial occlusions, or extreme head angles.

## Features
- 😴 **Drowsiness Detection**: Identifies drowsiness indicators based on eye and mouth movement.
- 📊 **Report Generation**: Exports analysis results per video to Excel.
- 🎥 **Batch Video Processing**: Supports multiple video uploads and frame-by-frame facial landmark analysis.
- 💾 **Result Dashboard**: Displays summary metrics and video previews directly in the app.

## Tech Stack
- **Frontend**: Streamlit
- **Computer Vision**: OpenCV
- **Facial Landmark Detection**: MediaPipe Face Mesh
- **Data Processing & Storage**: Pandas, openpyxl
- **Utilities**: tempfile, os, datetime, io (for file handling and export

## How It Works
- Upload recorded driving videos through the Streamlit web interface.
- Each uploaded video is processed using the process_video() function, which analyzes facial landmarks to detect eye closure and yawning patterns.
- The application calculates the number and duration of drowsiness events for each video and displays the summarized results in an interactive dashboard.
- Users can preview detection results per video and download the full analysis report in Excel format for further research or dataset compilation.

## Conclusion
This project delivers a post-trip Driver Drowsiness Detection system designed to quantify drowsiness indicators from recorded videos.
By generating structured datasets through computer vision and facial landmark analysis, it provides a solid foundation for research and the future development of advanced driver monitoring systems.
