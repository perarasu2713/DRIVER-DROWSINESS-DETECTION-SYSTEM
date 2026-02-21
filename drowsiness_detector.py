import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import threading
import winsound
import matplotlib.pyplot as plt
from collections import deque
import csv
import time

# -----------------------------
# Initialize MediaPipe Face Mesh
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Eye & Mouth Landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]

# -----------------------------
# EAR Calculation
# -----------------------------
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# -----------------------------
# MAR Calculation
# -----------------------------
def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[0], mouth[1])
    C = dist.euclidean(mouth[2], mouth[3])
    return A / C

# -----------------------------
# Alarm Sound
# -----------------------------
def sound_alarm():
    for _ in range(6):
        winsound.Beep(1200, 400)

# -----------------------------
# Camera Setup
# -----------------------------
cap = None
for i in range(3):
    temp_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if temp_cap.isOpened():
        cap = temp_cap
        print(f"Camera opened at index {i}")
        break

if cap is None:
    print("❌ No camera detected!")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# -----------------------------
# CSV Setup
# -----------------------------
csv_file = open("session_data.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)

csv_writer.writerow(["Time", "EAR", "MAR", "Blinks", "Yawns", "Drowsy"])

# -----------------------------
# Thresholds
# -----------------------------
EAR_THRESHOLD = 0.21
FRAME_THRESHOLD = 25
BLINK_FRAME_THRESHOLD = 3

MAR_THRESHOLD = 0.6
YAWN_FRAME_THRESHOLD = 15

# -----------------------------
# Counters
# -----------------------------
COUNTER = 0
ALARM_ON = False

BLINK_COUNTER = 0
TOTAL_BLINKS = 0

YAWN_COUNTER = 0
TOTAL_YAWNS = 0

# -----------------------------
# EAR Graph Setup
# -----------------------------
ear_history = deque(maxlen=100)

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_ylim(0, 0.6)
ax.set_title("Live EAR Graph")
ax.set_xlabel("Frames")
ax.set_ylabel("EAR Value")
ax.axhline(y=EAR_THRESHOLD, linestyle='--')

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        cv2.putText(frame, "FACE DETECTED", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            # Extract Eyes
            left_eye = []
            right_eye = []

            for idx in LEFT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))

            for idx in RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))

            # Extract Mouth
            mouth = []
            for idx in MOUTH:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                mouth.append((x, y))

            # Calculate EAR & MAR
            ear = (eye_aspect_ratio(left_eye) +
                   eye_aspect_ratio(right_eye)) / 2.0
            mar = mouth_aspect_ratio(mouth)

            # Display
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, f"Blinks: {TOTAL_BLINKS}", (30, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            cv2.putText(frame, f"Yawns: {TOTAL_YAWNS}", (30, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            # Update Graph
            ear_history.append(ear)
            line.set_xdata(range(len(ear_history)))
            line.set_ydata(ear_history)
            ax.set_xlim(0, len(ear_history))
            plt.draw()
            plt.pause(0.001)

            # Blink + Drowsiness
            if ear < EAR_THRESHOLD:
                COUNTER += 1
                BLINK_COUNTER += 1
            else:
                if BLINK_FRAME_THRESHOLD <= BLINK_COUNTER < FRAME_THRESHOLD:
                    TOTAL_BLINKS += 1
                BLINK_COUNTER = 0
                COUNTER = 0
                ALARM_ON = False

            if COUNTER >= FRAME_THRESHOLD:
                cv2.putText(frame, "DROWSINESS ALERT!", (50, 210),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.2, (0, 0, 255), 3)

                if not ALARM_ON:
                    ALARM_ON = True
                    threading.Thread(target=sound_alarm, daemon=True).start()

            # Yawn Detection
            if mar > MAR_THRESHOLD:
                YAWN_COUNTER += 1
            else:
                if YAWN_COUNTER >= YAWN_FRAME_THRESHOLD:
                    TOTAL_YAWNS += 1
                YAWN_COUNTER = 0

            # -----------------------------
            # CSV Logging
            # -----------------------------
            current_time = round(time.time(), 2)
            drowsy_status = 1 if COUNTER >= FRAME_THRESHOLD else 0

            csv_writer.writerow([
                current_time,
                round(ear, 3),
                round(mar, 3),
                TOTAL_BLINKS,
                TOTAL_YAWNS,
                drowsy_status
            ])

    else:
        cv2.putText(frame, "NO FACE DETECTED", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Driver Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
plt.close()
