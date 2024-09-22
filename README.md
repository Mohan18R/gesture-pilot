# Gesture Pilot


This project is a hand gesture-based control system that allows you to interact with your computer using simple hand gestures. It uses a webcam to capture hand movements and mediapipe to detect hand landmarks, which are then mapped to various actions like controlling the mouse cursor, adjusting volume, and taking screenshots.

## Features
- **Control mouse movement** using your index finger.
- **Click actions** are performed by making a fist.
- **Adjust system volume** by bringing two hands close together or apart.
- **Press media keys** like play/pause, next, and previous using predefined finger gestures.
- **Take screenshots** by using a specific gesture.
- Works in **real-time** with accurate hand tracking.
  
## How It Works
This system uses a webcam feed to capture hand movements and then detects hand landmarks using the `mediapipe` library. Based on the position of the hand landmarks, various actions are performed such as:
- Moving the mouse cursor.
- Adjusting system volume by measuring the distance between hands.
- Taking screenshots or navigating through media using specific gestures.

## Gesture Controls
| Gesture                | Action          |
|------------------------|-----------------|
| All fingers up          | Play/Pause      |
| Thumb and Pinky Up      | Next Track      |
| Thumb, Index, and Pinky Up | Previous Track |
| All fingers except Thumb up | Increase Volume |
| All fingers except Thumb and Pinky up | Decrease Volume |
| Thumb and Index Outstretched | Mouse Move |
| Thumb curled and Index finger pointed | Mouse Click |
| Victory Sign (Index & Middle Fingers Up) | Take Screenshot |

## Project Setup
To run this project, you need Python 3.8.2 and the following libraries:
```bash
pip install mediapipe
pip install opencv-python 
pip install pyautogui 
pip install numpy
pip install comtypes
pip install pycaw
