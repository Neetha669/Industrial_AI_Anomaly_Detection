# AI-Based Real-Time Industrial Anomaly Detection

## 📌 Overview

The **AI-Based Real-Time Industrial Anomaly Detection** is an AI-powered safety monitoring system designed to detect abnormal and unsafe conditions in an industrial environment.

The system uses **Computer Vision, AI-based anomaly detection, pose detection, and simulated sensor data** to monitor workers and identify safety risks such as:

- Worker presence
- Worker fall detection
- Danger-zone violations
- Industrial anomalies
- High temperature
- High vibration
- Overall safety risk

When a critical safety condition is detected, the system generates an alert and produces a **buzzer-like beep sound** without requiring physical hardware.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect workers in an industrial environment.
2. Detect worker falls using pose estimation.
3. Identify workers entering predefined danger zones.
4. Detect abnormal worker activities.
5. Monitor temperature conditions using simulated sensor values.
6. Monitor vibration conditions using simulated sensor values.
7. Generate real-time safety alerts.
8. Produce an audible warning when a dangerous condition occurs.
9. Display all safety information through a desktop monitoring dashboard.
10. Store the latest monitoring status and incident information.

---

# 🏭 System Features

## 1. 👷 Worker Detection

The system uses **YOLOv8** to detect people/workers in the video.

The system displays:

```text
WORKER: DETECTED

when a worker is detected.

If no worker is present:

WORKER: NOT DETECTED
```
## 2. 🤕 Fall Detection
```text
Worker fall detection is performed using MediaPipe Pose.

The system analyzes body landmarks and identifies whether a worker has fallen.

When a fall is detected:

FALL: DETECTED
RISK LEVEL: HIGH

The system also:

Generates a critical alert
Updates the monitoring dashboard
Saves the detected frame
Produces an audible warning beep

Example:

Worker fall detected
Source: MediaPipe Fall Detection
Alert Type: CRITICAL
```
## 3. ⚠️ Danger Zone Detection
```text
The system supports predefined danger zones within the industrial environment.

The danger zone can be defined using normalized coordinates:

DANGER_ZONE = {
    "x1": 0.62,
    "y1": 0.64,
    "x2": 0.79,
    "y2": 0.86
}

The coordinates are converted into pixel coordinates according to the video resolution.

The system checks the worker's bottom-center/foot position against the danger-zone area.

This is useful because the danger zone represents an area on the factory floor.

When a worker enters the danger zone:

DANGER ZONE: DANGER
RISK LEVEL: HIGH

An alert and warning sound can be generated.
```
## 4. 🌡️ Temperature Monitoring
```text
A physical temperature sensor is not required for the current demonstration.

Instead, the project uses simulated temperature values.

Example:

temperature = 65.0

The temperature threshold is:

TEMPERATURE_THRESHOLD = 70.0

Therefore:

Temperature < 70°C → SAFE
Temperature >= 70°C → DANGER

Example:

TEMPERATURE: 65.0 °C

If the value becomes:

TEMPERATURE: 75.0 °C

the system generates a temperature warning.
```
## 5. 📳 Vibration Monitoring
```text
The project also supports simulated vibration monitoring.

Example:

vibration = 5.0

The vibration threshold is:

VIBRATION_THRESHOLD = 7.0

Therefore:

Vibration < 7 → SAFE
Vibration >= 7 → DANGER

For demonstration purposes, the value can be changed in the code.
```
## 🚨 Alert System
```text
The system generates alerts when one or more dangerous conditions are detected.

The supported alert conditions include:

- Worker fall
- Danger-zone violation
- Hand danger
- Body danger
- High temperature
- High vibration
- AI anomaly

Example alert:

CRITICAL
Worker fall detected
MediaPipe Fall Detection
```
## 🔊 Buzzer / Beep Sound
```text
The project does not require a physical buzzer.

The application uses Python's Windows sound functionality:

import winsound

The warning sound is generated using:

winsound.Beep()

This allows the computer itself to act as the warning device during the demonstration.

The sound can be triggered for:

- Fall
- Danger Zone
- High Temperature
- High Vibration
- AI Anomaly
```
## 🤖 AI Technologies Used
```text
YOLOv8

YOLOv8 is used for real-time person detection.

Purpose:

Video
  ↓
YOLOv8
  ↓
Worker Detection
MediaPipe Pose

MediaPipe Pose is used for detecting human body landmarks.

Purpose:

Worker
  ↓
Pose Landmarks
  ↓
Body Position Analysis
  ↓
Fall Detection
MediaPipe Hands

MediaPipe Hands can be used to analyze hand positions.

Purpose:

Hand Landmarks
       ↓
Danger Zone Analysis
       ↓
Hand Danger Detection
Isolation Forest

Isolation Forest is used for anomaly detection.

It identifies unusual patterns in the extracted activity/pose features.

Basic flow:

Pose Data
   ↓
Feature Extraction
   ↓
Isolation Forest
   ↓
Normal / Anomaly
```
## 🧠 System Architecture
```text
                    INDUSTRIAL VIDEO
                           │
                           ▼
                    ┌─────────────┐
                    │   YOLOv8    │
                    │   Detection │
                    └──────┬──────┘
                           │
                           ▼
                    Worker Detection
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       MediaPipe Pose             Danger Zone
             │                     Detection
             ▼                           │
       Fall Detection                    │
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                   Anomaly Detection
                           │
                           ▼
                    Isolation Forest
                           │
                           ▼
                 ┌────────────────────┐
                 │  Safety Decision    │
                 └─────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Temperature        Vibration       Person Anomaly
     Simulation        Simulation      / Fall / Danger
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    Risk Assessment
                           │
                    ┌──────┴──────┐
                    │             │
                   SAFE          HIGH
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
                 ALERT                    BEEP SOUND
```
## 🖥️ Dashboard
```text
The system provides a desktop-based monitoring dashboard.

The dashboard displays:

System status
Worker status
Danger-zone status
Fall status
Anomaly status
Temperature
Vibration
Risk level
Current event
Live industrial video

Example:

SYSTEM       ONLINE
WORKER       DETECTED
DANGER ZONE  SAFE
FALL         NOT DETECTED
ANOMALY      NORMAL
TEMPERATURE  65.0 °C
VIBRATION    5.0
RISK LEVEL   LOW

When a dangerous condition occurs:

SYSTEM       ONLINE
WORKER       DETECTED
DANGER ZONE  DANGER
FALL         DETECTED
ANOMALY      DETECTED
TEMPERATURE  75.0 °C
VIBRATION    8.0
RISK LEVEL   HIGH
```

## 📁 Project Structure
```text
Industrial_AI_Anomaly_Detection/
│
├── backend/
│   ├── yolo_detector.py
│   ├── danger_zone.py
│   ├── anomaly_detector.py
│   ├── incident_manager.py
│   └── ...
│
├── data/
│   ├── videos/
│   │   ├── industrial_demo.mp4
│   │   └── industrial_danger.mp4
│   │
│   ├── latest_status.json
│   ├── latest_monitoring.jpg
│   ├── latest_anomaly.jpg
│   └── latest_danger.jpg
│
├── frontend/
│   └── ...
│
├── live_monitoring.py
│
├── requirements.txt
│
└── README.md
⚙️ Requirements

The project requires Python 3.x.

Main libraries used include:

Python
OpenCV
YOLOv8
Ultralytics
MediaPipe
NumPy
Pandas
Scikit-learn
Pillow
Tkinter

The project also uses:

winsound

for the computer-based warning sound on Windows.
```

## 📦 Installation
```text
1. Clone the Repository
git clone https://github.com/Neetha669/Industrial_AI_Anomaly_Detection.git

Go into the project directory:

cd Industrial_AI_Anomaly_Detection
2. Create Virtual Environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt

If required, install the main packages manually:

pip install ultralytics
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pandas
pip install scikit-learn
pip install pillow
```
## ▶️ Running the Project
```text
Activate the virtual environment:

venv\Scripts\activate

Then run the application:

python main.py

or run the appropriate project entry file if your project uses a different main file.
```

## 🎥 Demo Videos
```text
The project currently supports two demonstration videos.

Video 1 – Fall Detection
industrial_demo.mp4

Used mainly for:

- Worker detection
- Pose detection
- Fall detection
- AI anomaly detection

Video 2 – Industrial Danger Zone
industrial_danger.mp4

Used for:

- Worker detection
- Industrial environment monitoring
- Danger-zone analysis
```
## 🌡️ Simulated Sensor Demonstration
```text
Because physical sensors are not currently required for the software demonstration, temperature and vibration values are simulated.

Inside the monitoring code:

def get_simulated_sensor_values(self):

    temperature = 65.0
    vibration = 5.0

    return temperature, vibration

To demonstrate a temperature warning:

temperature = 75.0

To demonstrate a vibration warning:

vibration = 8.0

The system will then classify the corresponding sensor condition as dangerous.
```
## 🚨 Risk Level
```text
The overall risk level becomes HIGH when any major unsafe condition is detected.

The system considers:

- Fall
- Danger Zone
- AI Anomaly
- High Temperature
- High Vibration

The basic decision logic is:

If any dangerous condition is detected
             ↓
        RISK = HIGH
             ↓
       Generate Alert
             ↓
        Play Warning
          Sound

Otherwise:

No dangerous condition
          ↓
      RISK = LOW
          ↓
         SAFE
```
## 💾 Monitoring Data
```text
The latest monitoring information is stored in:

data/latest_status.json

Example:

{
    "system": "ONLINE",
    "worker": true,
    "danger": false,
    "fall": false,
    "anomaly": false,
    "temperature": 65.0,
    "vibration": 5.0,
    "risk_level": "LOW"
}

This information can be used by other dashboard modules.
```
## 🖼️ Captured Images
```text
The system can save important detection frames.

Latest monitoring frame
data/latest_monitoring.jpg
Latest anomaly frame
data/latest_anomaly.jpg
Latest danger-zone frame
data/latest_danger.jpg

These images can be used for incident analysis and reporting.
```

## 🔔 Incident Management
```text
The system can send detected events to the incident management module.

Examples:

- Worker fall detected
- Danger-zone violation
- High temperature detected
- High vibration detected
- Industrial anomaly detected

Each event can contain:

- Alert Type
- Message
- Detection Source
- Time
```
## 🔐 Safety Logic
```text
The system follows a simple safety decision process:

                 Worker Detected?
                       │
              ┌────────┴────────┐
             NO                 YES
             │                   │
        System Safe        Analyze Worker
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                Fall       Danger Zone       Anomaly
                  │              │              │
                  └──────────────┼──────────────┘
                                 │
                          Sensor Monitoring
                                 │
                    ┌────────────┴────────────┐
                    │                         │
              Temperature                Vibration
                    │                         │
                    └────────────┬────────────┘
                                 │
                         Risk Assessment
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                   LOW                      HIGH
                    │                         │
                  SAFE                 ALERT + BEEP
```

## 🛠️ Technologies
```text
Technology	                Purpose
Python	            Main programming language
OpenCV	            Video processing
YOLOv8	            Worker/person detection
MediaPipe Pose	    Human pose detection
MediaPipe Hands	    Hand detection
Isolation Forest	Anomaly detection
NumPy	            Numerical processing
Pandas	            Data processing
Scikit-learn	    Machine learning
Tkinter	Desktop     dashboard
Pillow	            Image display
Windows Winsound	Warning beep
JSON	            Monitoring status storage
```
## 📊 Current Implementation
```text
The current software demonstration includes:

✅ YOLOv8 worker detection
✅ MediaPipe pose detection
✅ Fall detection
✅ Simulated temperature monitoring
✅ Simulated vibration monitoring
✅ Risk-level calculation
✅ Alert generation
✅ Computer-based warning sound
✅ Monitoring dashboard
✅ JSON status storage
✅ Incident image saving
🔄 Danger-zone detection can be further calibrated for different camera/video views
🔄 Physical temperature sensor integration can be added
🔄 Physical vibration sensor integration can be added
🔄 Hardware buzzer can be added
```