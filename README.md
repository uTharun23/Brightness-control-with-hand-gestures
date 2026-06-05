# Hyperion: Premium Gesture-Based Brightness Control

This project is a high-tech, real-time hand gesture brightness controller built with Python, OpenCV, Google MediaPipe Hands, and the `screen-brightness-control` library. It features a custom glassmorphic HUD overlay and distance-invariant calculations.

## 🚀 Live Demo (Browser Version)

Try the web-based gesture controller immediately in your browser:
- **[GitHub Pages Live Demo](https://utharun23.github.io/Brightness-control-with-hand-gestures/)**
- **[Vercel Live Demo](https://brightness-control-with-hand-gestures.vercel.app/)**

*(Note: The browser version adjusts the brightness of the web page itself using a transparent overlay, as browser sandboxes are secure and cannot change your physical monitor's backlight directly. To control your physical screen, use the Desktop version below.)*

---

## Premium Features

- **Real-Time Hand Tracking**: Precision detection of 21 hand joints using MediaPipe.
- **Lock Gesture Toggle**: Keep your hand in front of the camera without constantly shifting brightness. 
  - **Raise Pinky**: Adjust mode `ACTIVE` (updates brightness).
  - **Fold Pinky**: Adjust mode `LOCKED` (locks brightness at current level).
- **Distance-Invariant Mapping**: Distance between thumb and index is normalized by palm size, ensuring brightness controls remain consistent whether your hand is close to the lens or far away.
- **Glassmorphism Side-Panel HUD**: Semi-transparent backing panel with neon-cyan boarder.
- **Neon-Glow Landmarks & Lines**: Custom-colored, glowing finger points and connecting line that changes color from neon pink (0%) to neon green/cyan (100%) dynamically.
- **Animated Circular Dial**: High-tech progress dial that matches your brightness and pulsates gently to signify system activity.
- **Webcam-Safe Anti-Lag Optimization**: System brightness API calls are throttled and run on a separate filter to prevent camera feed stutter, ensuring a smooth, high-framerate feed.
- **Hardware Integration & Software Fallback**: Interacts directly with Windows Monitor API. Automatically falls back to a transparent, click-through black window overlay (Software Dimmer) if the hardware display does not support DDC/CI or WMI, ensuring physical dimming works on all setups (including external monitors or VMs).

## Technologies Used

- HTML5 / CSS3 / JavaScript (Web Demo)
- Python 3 (Desktop Version)
- OpenCV (`opencv-python`)
- Google MediaPipe (`mediapipe`)
- NumPy
- Screen Brightness Control (`screen-brightness-control`)

## Installation (Desktop Version)

Install all required libraries via pip:

```bash
pip install -r requirements.txt
```

## How to Run (Desktop Version)

Execute the main controller script:

```bash
python brightnesscontrol.py
```

## Controls & Gestures

- **Pinch Index and Thumb**: Control the brightness level (0% - 100%).
- **Extend Pinky Finger**: Start adjusting/Unlocks brightness tracking (`STATUS: ACTIVE`).
- **Fold Pinky Finger**: Lock the current brightness value (`STATUS: LOCKED`).
- **Press ESC**: Close the application.

## Author
Ummadala Tharun
