🚗💤 AI Driver Drowsiness Detection System
<p align="center"> <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv"> <img src="https://img.shields.io/badge/MediaPipe-FaceMesh-orange?style=for-the-badge"> <img src="https://img.shields.io/badge/Status-Real--Time%20Detection-success?style=for-the-badge"> </p>
📌 Project Overview

The AI Driver Drowsiness Detection System is a real-time computer vision application that detects:

👁️ Eye Closure (EAR - Eye Aspect Ratio)

😮 Yawning (MAR - Mouth Aspect Ratio)

😴 Drowsiness State

🔔 Real-time Alarm Alerts

📊 Live EAR Graph Visualization

📁 CSV Session Logging

This system can be used in:

🚘 Smart Vehicles

🛣️ Driver Safety Systems

🏭 Industrial Machine Monitoring

🎓 Research Projects

🎯 Key Features

✨ Real-Time Face Detection using MediaPipe FaceMesh
✨ Blink Detection Counter
✨ Yawn Detection Counter
✨ Drowsiness Alert with Sound Alarm
✨ Live EAR Graph using Matplotlib
✨ Automatic CSV Logging for Analysis
✨ Threshold-Based Intelligent Detection

🧠 How It Works
👁️ Eye Aspect Ratio (EAR)

The system calculates EAR using facial landmarks:

When EAR drops below threshold → Eyes are closed.

If eyes remain closed for defined frames → 🚨 Drowsiness Alert triggered.

😮 Mouth Aspect Ratio (MAR)

MAR increases when mouth opens wide.

If MAR stays above threshold for certain frames → Yawn detected.

📊 Live Graph Monitoring

Displays EAR variation across frames.

Shows threshold line for visual debugging.

Helps in analyzing blinking patterns.

📂 Project Structure
📁 Driver-Drowsiness-Detection
│
├── drowsiness_detector.py      # Main Application File
├── requirements.txt            # Dependencies
├── session_data.csv            # Auto-generated session log
└── README.md                   # Project Documentation
⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/yourusername/Driver-Drowsiness-Detection.git
cd Driver-Drowsiness-Detection
2️⃣ Install Dependencies

From requirements file:

📄 Dependencies used: 

requirements

pip install -r requirements.txt
3️⃣ Run the Application
python drowsiness_detector.py

Press Q to exit.

🔧 Technical Stack
Technology	Purpose
🐍 Python	Core Programming
📷 OpenCV	Video Processing
🧠 MediaPipe	Face Landmark Detection
📊 Matplotlib	Live Graph Visualization
📐 SciPy	Distance Calculations
📁 CSV	Data Logging
📈 Detection Logic
Parameter	Threshold	Purpose
EAR_THRESHOLD	0.21	Eye closure detection
FRAME_THRESHOLD	25 frames	Drowsiness detection
MAR_THRESHOLD	0.6	Yawn detection
BLINK_FRAME_THRESHOLD	3 frames	Blink counting
📁 Output

The system generates:

📄 session_data.csv including:

Timestamp

EAR Value

MAR Value

Total Blinks

Total Yawns

Drowsiness Status (0 / 1)

Main application file: 

drowsiness_detector

🚨 Alert System

When prolonged eye closure is detected:

🔴 “DROWSINESS ALERT!” appears

🔔 Beep sound triggers (Windows)

🛠 Customization

You can modify thresholds inside:

EAR_THRESHOLD = 0.21
FRAME_THRESHOLD = 25
MAR_THRESHOLD = 0.6

For different lighting conditions or face shapes.

📊 Future Improvements

🚀 Add Deep Learning Drowsiness Classification
🚀 Deploy on Raspberry Pi / Jetson Nano
🚀 Add Driver Identity Recognition
🚀 Build Web Dashboard for Fleet Monitoring
🚀 Store Data in Cloud Database

🎥 Demo Output

Real-time camera feed

Live EAR graph

Blink & Yawn counters

Drowsiness alert message

🧪 Ideal For

Final Year Engineering Projects

AI / ML Portfolio Projects

Computer Vision Practice

Hackathons

Driver Safety Research

🏆 Why This Project Stands Out

✔ Real-time Processing
✔ Multiple Behavioral Signals
✔ Data Logging for ML Training
✔ Clean Modular Logic
✔ Scalable Architecture

📜 License

This project is open-source and free to use for educational purposes.

👨‍💻 Author

Perarasu M
AI & Full Stack Developer
Building Real-World Intelligent Systems 🚀
