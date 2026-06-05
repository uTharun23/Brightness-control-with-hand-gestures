import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import screen_brightness_control as sbc
import time
import math
import tkinter as tk
import ctypes
import os
import urllib.request

# ----------------------------------------------------
# Configuration & Styling Constants
# ----------------------------------------------------
NEON_CYAN = (242, 255, 0)      # BGR for Neon Cyan (Greenish Cyan)
NEON_MAGENTA = (203, 0, 255)   # BGR for Neon Pink/Magenta
NEON_GREEN = (0, 255, 128)     # BGR for Glowing Green
NEON_RED = (50, 50, 255)       # BGR for Red-Orange
DARK_BG = (20, 20, 20)         # Sidebar backdrop
TEXT_WHITE = (245, 245, 245)
COLOR_MUTED = (160, 160, 160)

# Manual definition of hand skeleton connections (legacy mp.solutions fallback)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (9, 10), (10, 11), (11, 12),           # Middle
    (13, 14), (14, 15), (15, 16),          # Ring
    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
    (5, 9), (9, 13), (13, 17)              # Palm Knuckles
]

# Model download check
MODEL_PATH = 'hand_landmarker.task'
MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'

if not os.path.exists(MODEL_PATH):
    print("Downloading hand_landmarker.task model (approx. 5.6MB)...")
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete!")
    except Exception as e:
        print(f"Error downloading model: {e}")

# Initialize MediaPipe Tasks Hand Landmarker
print("Initializing MediaPipe Gesture Engine...")
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

# ----------------------------------------------------
# Helper Functions for Visual Effects
# ----------------------------------------------------
def draw_glow_line(img, pt1, pt2, color, base_thickness=2):
    """Draws a neon glow line by overlaying a thick transparent line and a bright white core."""
    overlay = img.copy()
    cv2.line(overlay, pt1, pt2, color, base_thickness * 5, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, 0.25, img, 0.75, 0, img)
    
    cv2.line(img, pt1, pt2, color, base_thickness * 2, lineType=cv2.LINE_AA)
    cv2.line(img, pt1, pt2, (255, 255, 255), base_thickness, lineType=cv2.LINE_AA)

def draw_glow_circle(img, center, radius, color, thickness=cv2.FILLED):
    """Draws a glowing neon circle with a soft transparent halo."""
    overlay = img.copy()
    if thickness == cv2.FILLED:
        cv2.circle(overlay, center, radius + 8, color, cv2.FILLED, lineType=cv2.LINE_AA)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
        cv2.circle(img, center, radius, color, cv2.FILLED, lineType=cv2.LINE_AA)
        cv2.circle(img, center, max(1, radius - 4), (255, 255, 255), cv2.FILLED, lineType=cv2.LINE_AA)
    else:
        cv2.circle(overlay, center, radius + 4, color, thickness + 3, lineType=cv2.LINE_AA)
        cv2.addWeighted(overlay, 0.25, img, 0.75, 0, img)
        cv2.circle(img, center, radius, color, thickness, lineType=cv2.LINE_AA)
        cv2.circle(img, center, radius, (255, 255, 255), max(1, thickness - 1), lineType=cv2.LINE_AA)

def get_glow_color(pct):
    """Interpolate BGR color from magenta (0%) to green/cyan (100%)."""
    r = int(NEON_MAGENTA[2] + (NEON_CYAN[2] - NEON_MAGENTA[2]) * (pct / 100.0))
    g = int(NEON_MAGENTA[1] + (NEON_CYAN[1] - NEON_MAGENTA[1]) * (pct / 100.0))
    b = int(NEON_MAGENTA[0] + (NEON_CYAN[0] - NEON_MAGENTA[0]) * (pct / 100.0))
    return (b, g, r)

# ----------------------------------------------------
# Software Dimmer Overlay Setup (Transparent, Click-Through Window)
# ----------------------------------------------------
root_overlay = None
overlay_enabled = False

def init_software_dimmer():
    global root_overlay, overlay_enabled
    try:
        print("Initializing Universal Software Dimmer overlay...")
        root_overlay = tk.Tk()
        root_overlay.overrideredirect(True)
        root_overlay.attributes('-topmost', True)
        root_overlay.config(bg='black')
        
        # Geometry to cover full virtual screen size
        screen_w = root_overlay.winfo_screenwidth()
        screen_h = root_overlay.winfo_screenheight()
        root_overlay.geometry(f"{screen_w}x{screen_h}+0+0")
        
        # Apply click-through and layered window styles via Windows API
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        
        hwnd = root_overlay.winfo_id()
        ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        new_style = ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
        
        # Start completely transparent
        root_overlay.attributes('-alpha', 0.0)
        root_overlay.update()
        overlay_enabled = True
        print("Software Dimmer overlay initialized successfully.")
    except Exception as e:
        print(f"Error setting up software overlay: {e}")
        overlay_enabled = False

# ----------------------------------------------------
# Main Program Init
# ----------------------------------------------------
print("Initializing Camera...")
cap = cv2.VideoCapture(0)

# Check if screen brightness control is supported
simulation_mode = False
current_system_brightness = 50

try:
    current_system_brightness = sbc.get_brightness(display=0)
    if isinstance(current_system_brightness, list):
        current_system_brightness = current_system_brightness[0]
    print(f"System brightness detected: {current_system_brightness}%")
except Exception as e:
    print(f"Warning: Hardware brightness control not supported ({e}). Using Software Dimmer.")
    simulation_mode = True

# Initialize Software Dimmer Overlay
init_software_dimmer()

# Smoothing state variables (Exponential Moving Average)
smooth_brightness_hud = float(current_system_brightness)
smooth_brightness_sys = float(current_system_brightness)
target_brightness = float(current_system_brightness)

# State for gesture control mode
control_active = False
last_sys_update_time = time.time()
last_set_brightness = int(current_system_brightness)

# Sidebar width
SIDEBAR_WIDTH = 240

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        break

    # Mirror the frame horizontally for natural hand interaction
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    sidebar_x = width - SIDEBAR_WIDTH

    # 1. Draw Glassmorphic Sidebar Backdrop
    overlay = frame.copy()
    cv2.rectangle(overlay, (sidebar_x, 0), (width, height), DARK_BG, cv2.FILLED)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    # Glowing separator line
    cv2.line(frame, (sidebar_x, 0), (sidebar_x, height), NEON_CYAN, 2, lineType=cv2.LINE_AA)

    # Convert to MediaPipe Image object
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = detector.detect(mp_image)

    hand_detected = False
    
    if results.hand_landmarks:
        hand_detected = True
        for hand_landmarks in results.hand_landmarks:
            # Extract landmark pixel positions
            lm_list = []
            for lm in hand_landmarks:
                lm_list.append([int(lm.x * width), int(lm.y * height)])

            if len(lm_list) >= 21:
                # Get coordinates for calculation
                wrist = np.array(lm_list[0])
                thumb_tip = np.array(lm_list[4])
                index_tip = np.array(lm_list[8])
                middle_knuckle = np.array(lm_list[9])
                pinky_knuckle = np.array(lm_list[17])
                pinky_tip = np.array(lm_list[20])

                # A. Lock Gesture detection (Is Pinky finger extended?)
                dist_pinky_tip = np.linalg.norm(pinky_tip - wrist)
                dist_pinky_knuckle = np.linalg.norm(pinky_knuckle - wrist)
                control_active = dist_pinky_tip > (dist_pinky_knuckle * 1.15)

                # B. Palm distance normalization (Invariant to hand distance from camera)
                palm_size = np.linalg.norm(middle_knuckle - wrist)
                if palm_size == 0:
                    palm_size = 1.0

                # C. Compute Pinch Distance and Ratio
                pinch_dist = np.linalg.norm(index_tip - thumb_tip)
                ratio = pinch_dist / palm_size

                # Map normalized ratio [approx 0.22 (closed) to 1.0 (open)] to brightness [0, 100]
                new_target = np.interp(ratio, [0.22, 1.0], [0.0, 100.0])
                new_target = np.clip(new_target, 0.0, 100.0)

                # Update target only if control mode is active
                if control_active:
                    target_brightness = new_target

                # D. Draw Holographic Hand Skeletal Overlay
                # Custom connecting lines (drawn thin and subtle)
                for conn in HAND_CONNECTIONS:
                    pt1 = lm_list[conn[0]]
                    pt2 = lm_list[conn[1]]
                    cv2.line(frame, tuple(pt1), tuple(pt2), (180, 180, 180), 1, lineType=cv2.LINE_AA)

                # Draw ordinary joint dots
                for pt in lm_list:
                    cv2.circle(frame, tuple(pt), 3, (220, 220, 220), cv2.FILLED, lineType=cv2.LINE_AA)

                # Highlight control joints: Thumb Tip and Index Tip
                glow_color = get_glow_color(smooth_brightness_hud)
                draw_glow_circle(frame, tuple(thumb_tip), 8, glow_color, cv2.FILLED)
                draw_glow_circle(frame, tuple(index_tip), 8, glow_color, cv2.FILLED)

                # Draw glowing connection line between pinch points
                draw_glow_line(frame, tuple(thumb_tip), tuple(index_tip), glow_color, 2)

                # Add particle effect sliding on the connecting line
                t_val = (time.time() * 2.5) % 1.0
                px = int(thumb_tip[0] + t_val * (index_tip[0] - thumb_tip[0]))
                py = int(thumb_tip[1] + t_val * (index_tip[1] - thumb_tip[1]))
                cv2.circle(frame, (px, py), 4, (255, 255, 255), cv2.FILLED, lineType=cv2.LINE_AA)

                # Highlight pinky tip to show active/locked state
                pinky_color = NEON_GREEN if control_active else NEON_RED
                draw_glow_circle(frame, tuple(pinky_tip), 6, pinky_color, cv2.FILLED)

    # 2. Smooth Animations (EMA filter)
    smooth_brightness_hud += 0.20 * (target_brightness - smooth_brightness_hud)
    smooth_brightness_sys += 0.08 * (target_brightness - smooth_brightness_sys)

    # 3. Apply System Brightness changes (Throttled & Error-controlled)
    target_int = int(round(smooth_brightness_sys))
    current_time = time.time()
    
    if control_active:
        if simulation_mode:
            # If hardware control is unsupported, the Software Overlay handles dimming
            pass
        else:
            # Hardware adjustment
            if target_int != last_set_brightness and (current_time - last_sys_update_time) > 0.15:
                try:
                    sbc.set_brightness(target_int)
                    last_set_brightness = target_int
                    last_sys_update_time = current_time
                except Exception as e:
                    print(f"Error adjusting hardware brightness: {e}. Switching to software dimmer fallback.")
                    simulation_mode = True

    # 4. Update Software Overlay opacity dynamically (dimming window)
    if overlay_enabled and root_overlay:
        try:
            # Map brightness level 0-100 to transparent overlay opacity 0.82 to 0.0
            # 100% Brightness -> 0.0 (Fully transparent)
            # 0% Brightness -> 0.82 (Max dim black overlay)
            opacity = (100.0 - smooth_brightness_sys) / 100.0 * 0.82
            root_overlay.attributes('-alpha', opacity)
            root_overlay.update()
        except Exception as e:
            print(f"Overlay update error: {e}")
            overlay_enabled = False

    # ----------------------------------------------------
    # Draw Premium HUD Elements (Sidebar contents)
    # ----------------------------------------------------
    
    # Header Title
    cv2.putText(frame, "HYPERION v2.1", (sidebar_x + 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, NEON_CYAN, 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, "GESTURE ENGINE", (sidebar_x + 20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_MUTED, 1, lineType=cv2.LINE_AA)

    # Status indicator box
    status_y = 100
    status_text = "ACTIVE" if control_active else "LOCKED"
    status_color = NEON_GREEN if control_active else NEON_RED
    
    cv2.rectangle(frame, (sidebar_x + 20, status_y), (width - 20, status_y + 30), (35, 35, 35), cv2.FILLED)
    cv2.rectangle(frame, (sidebar_x + 20, status_y), (width - 20, status_y + 30), status_color, 1, lineType=cv2.LINE_AA)
    cv2.putText(frame, f"STATUS: {status_text}", (sidebar_x + 35, status_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, status_color, 1, lineType=cv2.LINE_AA)

    # Draw circular glowing HUD progress meter
    dial_center = (sidebar_x + SIDEBAR_WIDTH // 2, 230)
    dial_radius = 55
    
    # Background Track Ring
    cv2.circle(frame, dial_center, dial_radius, (45, 45, 45), 8, lineType=cv2.LINE_AA)
    
    # Active Glowing Progress Arc
    angle_sweep = int(360 * (smooth_brightness_hud / 100.0))
    glow_color = get_glow_color(smooth_brightness_hud)
    cv2.ellipse(frame, dial_center, (dial_radius, dial_radius), -90, 0, angle_sweep, glow_color, 8, lineType=cv2.LINE_AA)

    # Subtle pulsating radius effect
    pulse = int(math.sin(time.time() * 5) * 2)
    cv2.circle(frame, dial_center, dial_radius + pulse, glow_color, 1, lineType=cv2.LINE_AA)

    # Numeric value in center of dial
    val_str = f"{int(round(smooth_brightness_hud))}%"
    (text_w, text_h), _ = cv2.getTextSize(val_str, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    cv2.putText(frame, val_str, (dial_center[0] - text_w // 2, dial_center[1] + text_h // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_WHITE, 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, "BRIGHTNESS", (sidebar_x + 20, 315),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_MUTED, 1, lineType=cv2.LINE_AA)

    # Hardware / Simulation Mode Notice
    info_y = 350
    if simulation_mode:
        cv2.rectangle(frame, (sidebar_x + 20, info_y), (width - 20, info_y + 25), (40, 10, 80), cv2.FILLED)
        cv2.putText(frame, "SOFTWARE DIMMER", (sidebar_x + 35, info_y + 17),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, NEON_CYAN, 1, lineType=cv2.LINE_AA)
    else:
        cv2.putText(frame, "HARDWARE LINKED", (sidebar_x + 30, info_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, NEON_GREEN, 1, lineType=cv2.LINE_AA)

    # Instructions box at bottom
    instr_y = height - 100
    cv2.line(frame, (sidebar_x + 15, instr_y - 10), (width - 15, instr_y - 10), (50, 50, 50), 1)
    
    cv2.putText(frame, "GESTURE SCHEMATIC", (sidebar_x + 20, instr_y + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, NEON_CYAN, 1, lineType=cv2.LINE_AA)
    cv2.putText(frame, "- Raise pinky to Adjust", (sidebar_x + 20, instr_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, TEXT_WHITE, 1, lineType=cv2.LINE_AA)
    cv2.putText(frame, "- Fold pinky to Lock value", (sidebar_x + 20, instr_y + 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, TEXT_WHITE, 1, lineType=cv2.LINE_AA)
    cv2.putText(frame, "- Pinch index/thumb to set", (sidebar_x + 20, instr_y + 66),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, TEXT_WHITE, 1, lineType=cv2.LINE_AA)
    cv2.putText(frame, "Press ESC to Quit", (sidebar_x + 20, instr_y + 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_MUTED, 1, lineType=cv2.LINE_AA)

    # Render frame
    cv2.imshow("Hyperion Gesture Controller", frame)

    # Break loop on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
print("Terminating Gesture Engine...")
cap.release()
cv2.destroyAllWindows()
detector.close()
if root_overlay:
    try:
        root_overlay.destroy()
    except:
        pass