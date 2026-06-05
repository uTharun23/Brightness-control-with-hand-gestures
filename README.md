# Brightness Control With Hand Gestures

This project is a high-tech, real-time hand gesture brightness controller built with Python, OpenCV, Google MediaPipe Hands, and the `screen-brightness-control` library. It features a custom glassmorphic HUD overlay and distance-invariant calculations.

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
- **Hardware Integration & Simulation Fallback**: Interacts directly with Windows Monitor API. Automatically falls back to a clean, visual-only simulation mode if the hardware display does not support DDC/CI or WMI.

## Technologies Used

- Python 3
- OpenCV (`opencv-python`)
- Google MediaPipe (`mediapipe`)
- NumPy
- Screen Brightness Control (`screen-brightness-control`)

## Installation

Install all required libraries via pip:

```bash
pip install -r requirements.txt
```

## How to Run

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
