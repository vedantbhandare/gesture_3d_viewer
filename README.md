<h1 align="center">Gesture-Controlled 3D Viewer</h1>

<p align="center">
  Real-time 3D interaction using MediaPipe, WebSockets, and Three.js
</p>

---
# ✋ Gesture-Controlled 3D Viewer  
A real-time 3D interaction system using hand-tracking, MediaPipe, WebSockets, and Three.js.

---

## 🎯 Overview  
This project demonstrates a real-time system that allows users to interact with a 3D model using hand gestures.  

It uses:  
- **MediaPipe Hands (Python)** → gesture detection  
- **WebSockets** → sends gesture data to browser  
- **Three.js** → renders & controls a 3D cube  
- **Custom gestures** → zoom, rotation, and more  

---

## 🚀 Features  
- ✔️ Real-time hand tracking  
- ✔️ Gesture-based zoom and rotation  
- ✔️ Lightweight WebSocket communication  
- ✔️ Three.js 3D rendering  
- ✔️ Python server (no frameworks required)  
- ✔️ Works with any webcam  

---

📁 **Project Structure** <br>
gesture_3d_viewer/ <br>
│── server.py — Python WebSocket + MediaPipe server <br>
│── static/ <br>
│   └── index.html — 3D viewer <br>
│── assets/ — images used in README <br>
│── Project Report.docx <br>
│── venv/ (ignored)

---

## 🔧 Requirements  
- Python **3.9+**  
- pip  
- Webcam  
- Modern browser  
- Three.js (loaded via CDN)

---

▶️ How to Run the Project
1. Activate virtual environment (optional)
.\venv\Scripts\activate
2. Install dependencies
pip install mediapipe opencv-python websockets
3. Run the Python gesture server
python server.py
4. Open the 3D viewer

Navigate in the browser to:
👉 http://localhost:8080

---

🖐️ Gesture Controls
Gesture	Action
Pinch	Zoom in/out
Index finger pointing	Rotate model
Hand open	Stop interaction

---

## 📸 Demo & Screenshots

### 🖥️ 3D Viewer Interface  
This is the main Three.js viewer where gestures control zoom and rotation.

<img src="assets/viewer.png" width="700"/>

---

### ✋ Real-Time Gesture Detection (MediaPipe)  
The Python server tracks hand landmarks, detects pinch & rotation, and sends gestures to the browser via WebSockets.

<img src="assets/gestures.png" width="700"/>

---

### 🧪 WebSocket + Server Output  
The Python backend logs camera startup, WebSocket connections, and real-time gesture events.

<img src="assets/Terminal.png" width="700"/>

---

📜 License
MIT License

Copyright (c) 2025 Vedant Bhandare

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

👤 Author
Vedant Bhandare
Gesture-controlled 3D systems • Computer Vision • Interactive UI
