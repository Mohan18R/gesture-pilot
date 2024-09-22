import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Get screen size and initialize cursor control variables
screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0               

# Initialize audio utilities
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

last_volume_change = 0
last_action_time = 0

# Function to get hand landmarks
def hand_landmarks(image):
    results = hands.process(image)
    landmark_list = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmark_list.append([(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])) for landmark in hand_landmarks.landmark])
    return landmark_list

# Function to handle actions based on gestures
def perform_actions(finger_status, current_time):
    global last_action_time
    if current_time - last_action_time < 0.2:  # Adjust to prevent gesture spamming
        return
    
    action_performed = True
    if all(finger_status):  # All fingers up
        pyautogui.press('space')
    elif finger_status == [0, 1, 0, 0, 1]:  # Index and pinky up (right swipe)
        pyautogui.press('right')
    elif finger_status == [0, 1, 1, 0, 1]:  # Index, middle, pinky (left swipe)
        pyautogui.press('left')
    elif finger_status == [0, 1, 1, 1, 1]:  # Index, middle, ring, pinky (volume up)
        pyautogui.press('up')
    elif finger_status == [0, 1, 1, 1, 0]:  # Index, middle, ring (volume down)
        pyautogui.press('down')
    elif finger_status == [0, 1, 1, 0, 0]:  # Index and middle (screenshot)
        pyautogui.screenshot('screenshot.png')
    else:
        action_performed = False

    if action_performed:
        last_action_time = current_time

# Function to get finger status (whether each finger is up or down)
def get_finger_status(landmarks):
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, index, middle, ring, pinky
    return [int(landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0])] + \
           [int(landmarks[tip_id][1] < landmarks[tip_id - 2][1]) for tip_id in tip_ids[1:]]

# Function to calculate the distance between two hands for volume control
def get_average_finger_distance(landmarks):
    if len(landmarks) >= 2:
        return (math.hypot(*(np.array(landmarks[0][20]) - np.array(landmarks[1][20]))) +
                math.hypot(*(np.array(landmarks[0][16]) - np.array(landmarks[1][16])))) / 2
    return None

# Create a named window for displaying the webcam feed
cv2.namedWindow("Hand Gesture Control")

running = True
frame_count = 0  # To process every few frames for optimization
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if frame_count % 2 == 0:  # Process every 2nd frame to reduce load
        landmarks = hand_landmarks(frame_rgb)

    current_time = time.time()

    if landmarks:
        distance = get_average_finger_distance(landmarks)
        
        if distance is not None and (current_time - last_volume_change) > 0.1:
            vol = np.interp(distance, [50, 300], [minVol, maxVol])
            volPercentage = np.interp(vol, [minVol, maxVol], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            last_volume_change = current_time

            volBar = int(np.interp(volPercentage, [0, 100], [720, 150]))
            cv2.rectangle(frame, (50, 150), (85, 720), (0, 255, 0), 3)
            cv2.rectangle(frame, (50, volBar), (85, 720), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(volPercentage)}%', (40, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        if landmarks[0]:
            finger_status = get_finger_status(landmarks[0])
            perform_actions(finger_status, current_time)

            # Cursor control for index finger movement
            if finger_status[1] == 1 and finger_status[2] == 0:
                x1, y1 = landmarks[0][8]  # Index fingertip coordinates
                x3 = np.interp(x1, (75, 1205), (0, screen_width))
                y3 = np.interp(y1, (75, 645), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x) / 8  # Smooth the cursor movement
                curr_y = prev_y + (y3 - prev_y) / 8

                pyautogui.moveTo(screen_width - curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

            # Left click for thumb (gesture detection for clicking)
            if finger_status[1] == 0 and finger_status[0] == 1:
                pyautogui.click()
                time.sleep(0.2)  # Reduced sleep to make it more responsive

    cv2.imshow("Hand Gesture Control", frame)
    frame_count += 1  # Increment frame count for optimized processing

    # Exit on pressing 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False

# Clean up
cap.release()
cv2.destroyAllWindows()
print("Program terminated.")
