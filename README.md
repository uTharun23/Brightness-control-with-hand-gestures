# 👋 Smart Brightness Control Using Hand Gesture Recognition & Computer Vision 💡

A premium real-time computer vision application that enables users to control screen brightness using simple hand gestures. Built with Python, OpenCV, and MediaPipe, the system delivers a touchless, intuitive, and futuristic user experience with advanced gesture tracking, adaptive brightness mapping, and a modern glassmorphic interface.

---

## 🌟 Project Overview

Smart Brightness Control is an AI-powered desktop application that leverages Computer Vision and Hand Gesture Recognition to adjust display brightness without physical interaction.

Using a webcam, the system tracks hand landmarks in real time and translates finger movements into precise brightness adjustments. The application incorporates intelligent normalization techniques, ensuring consistent performance regardless of hand distance from the camera.

---

## 🚀 Live Demo

### 🌐 Web Version

**Live Demo:** https://brightness-control-with-hand-gestur.vercel.app/

> **Note:** Browser security restrictions prevent direct control of monitor brightness. The web version simulates brightness adjustment through a dynamic overlay, while the desktop application controls the actual display brightness.

---

## ✨ Key Features

### 👋 Real-Time Hand Tracking

* Detects and tracks 21 hand landmarks using Google MediaPipe.
* Accurate gesture recognition with minimal latency.
* Smooth and responsive interaction.

### 🎚️ Gesture-Based Brightness Control

* Adjust brightness using the distance between thumb and index finger.
* Real-time brightness mapping from 0% to 100%.
* Natural and intuitive touchless control.

### 🔒 Smart Lock Mechanism

* **Pinky Extended:** Adjustment Mode (ACTIVE)
* **Pinky Folded:** Lock Mode (LOCKED)

Prevents accidental brightness changes while keeping your hand visible to the camera.

### 📏 Distance-Invariant Brightness Mapping

* Brightness calculations are normalized using palm size.
* Consistent performance regardless of camera distance.
* Improved usability across different environments.

### 🎨 Premium Glassmorphic HUD

* Modern glass-effect control panel.
* Neon-inspired visual elements.
* Dynamic brightness indicators and status monitoring.

### 🌈 Dynamic Visual Feedback

* Animated brightness progress ring.
* Real-time gesture visualization.
* Color transitions based on brightness levels.

### ⚡ Performance Optimization

* Multi-threaded brightness updates.
* Reduced API call overhead.
* Smooth webcam rendering without frame drops.

### 🖥️ Hardware & Software Brightness Support

* Direct monitor brightness control using Windows APIs.
* Automatic fallback dimming overlay for unsupported displays.
* Compatible with laptops, external monitors, and virtual machines.

---

## 🛠️ Technology Stack

| Technology                | Purpose                    |
| ------------------------- | -------------------------- |
| Python 3                  | Core Application           |
| OpenCV                    | Computer Vision Processing |
| Google MediaPipe          | Hand Landmark Detection    |
| NumPy                     | Mathematical Operations    |
| Screen Brightness Control | Brightness Management      |
| HTML5                     | Web Demonstration          |
| CSS3                      | UI Styling                 |
| JavaScript                | Browser Interaction        |

---

## 📂 Project Architecture

```text
Smart-Brightness-Control/
│
├── brightnesscontrol.py
├── requirements.txt
├── assets/
├── screenshots/
├── README.md
│
└── web-demo/
    ├── index.html
    ├── style.css
    └── script.js
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/uTharun23/Smart-Brightness-Control.git
cd Smart-Brightness-Control
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python brightnesscontrol.py
```

---

## 🎮 Gesture Controls

| Gesture                   | Action                    |
| ------------------------- | ------------------------- |
| 🤏 Thumb + Index Distance | Adjust Brightness         |
| ☝️ Pinky Extended         | Unlock Brightness Control |
| ✊ Pinky Folded            | Lock Current Brightness   |
| ⌨️ ESC Key                | Exit Application          |

---

## 💡 Use Cases

* Touchless Computer Interaction
* Smart Workstations
* Accessibility Assistance
* AI & Computer Vision Learning
* Human-Computer Interaction Research
* Gesture-Controlled Smart Environments

---

## 📈 Future Enhancements

* Multi-Hand Support
* Volume Control Gestures
* Gesture-Based Media Controls
* Voice Assistant Integration
* AI Gesture Customization
* Cross-Platform Support (Linux & macOS)
* Smart Home Device Integration

---

## 🏆 Learning Outcomes

This project demonstrates practical implementation of:

* Computer Vision
* Hand Tracking Algorithms
* Human-Computer Interaction (HCI)
* Real-Time Image Processing
* Python Application Development
* UI/UX Design Principles
* Performance Optimization Techniques

---

## 👨‍💻 Author

### Ummadala Tharun

Aspiring Software Developer | Python Developer | Computer Vision Enthusiast

📧 Email: [tharunummadala@gmail.com](mailto:tharunummadala@gmail.com)

🔗 GitHub: https://github.com/uTharun23

🔗 LinkedIn: [www.linkedin.com/in/tharunummadala](http://www.linkedin.com/in/tharunummadala)

---

## 📜 License

This project is developed for educational, research, and portfolio purposes.

© 2026 Ummadala Tharun. All Rights Reserved.
