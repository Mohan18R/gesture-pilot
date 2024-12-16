# Gesture Pilot

This project is a **real-time hand gesture control system** that uses a webcam to detect hand gestures and perform various actions like controlling the mouse cursor, taking screenshots, controlling volume, and navigating media files. The application utilizes **MediaPipe**, **OpenCV**, and **PyAutoGUI** to achieve gesture recognition and device control.

## Features

- **Cursor Control**: Move the cursor using the index finger with smooth Kalman Filter-based movement.
- **Media Control**: Navigate media files using specific hand gestures.
  - `Next (Right Arrow)` - Gesture: Index finger and pinky up.
  - `Previous (Left Arrow)` - Gesture: Index, middle finger, and pinky up.
  - `Play/Pause (Space)` - Gesture: All fingers up.
- **Volume Control**: Adjust volume by measuring the distance between fingertips of two hands.
- **Screenshot**: Take a screenshot with a specific gesture.
- **Click**: Perform a left-click using thumb gestures.

## Technologies Used

- **Python**: Programming language.
- **OpenCV**: For real-time webcam feed and image processing.
- **MediaPipe**: For hand landmark detection.
- **PyAutoGUI**: For controlling mouse and keyboard inputs.
- **PyCaw**: For system audio volume control.
- **FilterPy**: For Kalman Filter-based cursor smoothing.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries (install them using the command below):

```bash
pip install opencv-python mediapipe pyautogui filterpy pycaw numpy
