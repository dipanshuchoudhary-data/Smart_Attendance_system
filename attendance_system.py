import cv2
import face_recognition
import pickle
from datetime import datetime, date
import pandas as pd
import os
from database import log_attendance_to_db
import sqlite3

# ----------------- CONFIG -----------------
ATTENDANCE_FILE = "attendance/attendance_log.csv"
DB_PATH = "database/attendance.db"
os.makedirs("attendance", exist_ok=True)

# ----------------- Load Encodings -----------------
try:
    with open("embeddings/faces.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)
except FileNotFoundError:
    print("[ERROR] embeddings/faces.pkl not found. Please register faces first.")
    exit()

# ----------------- DB Check Helper -----------------
def is_already_marked_today(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, today))
    result = cur.fetchone()
    conn.close()
    return result is not None

# ----------------- Webcam & Recognition -----------------
attendance_log = set()
cap = cv2.VideoCapture(0)
print("[INFO] Starting webcam for attendance... Press 'k' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

            if name not in attendance_log and not is_already_marked_today(name):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                attendance_log.add(name)

                # Save to CSV
                row = {"Name": name, "Timestamp": timestamp}
                df = pd.DataFrame([row])
                if os.path.exists(ATTENDANCE_FILE):
                    df.to_csv(ATTENDANCE_FILE, mode='a', header=False, index=False)
                else:
                    df.to_csv(ATTENDANCE_FILE, mode='w', header=True, index=False)

                # Save to DB
                log_attendance_to_db(name)

                print(f"[✅] Marked attendance: {name} at {timestamp}")
            else:
                print(f"[⚠️] {name} already marked today.")

        # Draw box
        top, right, bottom, left = box
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("k"):
        break

cap.release()
cv2.destroyAllWindows()
