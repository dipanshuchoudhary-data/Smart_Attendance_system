import cv2
import face_recognition
import os
import time
import pickle
from database import add_user_to_db

def duplicate_face(new_encoding, known_encodings, tolerance=0.5):
    results = face_recognition.compare_faces(known_encodings, new_encoding, tolerance=tolerance)
    return any(results)

def register_face(name):
    cap = cv2.VideoCapture(0)
    print("[INFO] Starting face registration...")

    os.makedirs("dataset", exist_ok=True)
    os.makedirs("embeddings", exist_ok=True)
    encoding_file = "embeddings/faces.pkl"

    # Load known encodings
    known_encodings = []
    known_names = []
    if os.path.exists(encoding_file):
        with open(encoding_file, "rb") as f:
            known_encodings, known_names = pickle.load(f)

    filename = f"dataset/{name}.jpg"
    captured = False
    countdown_started = False
    countdown_start_time = None
    countdown_duration = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects = face_recognition.face_locations(rgb)
        display_frame = cv2.flip(frame, 1)

        if rects and not captured:
            if not countdown_started:
                countdown_started = True
                countdown_start_time = time.time()
        else:
            countdown_started = False
            countdown_start_time = None

        if countdown_started:
            elapsed = int(time.time() - countdown_start_time)
            remaining = countdown_duration - elapsed

            if remaining > 0:
                cv2.putText(display_frame, f"Capturing in {remaining}...", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            else:
                try:
                    encoding = face_recognition.face_encodings(rgb, rects)[0]
                except IndexError:
                    print("[WARNING] Face not found at capture moment.")
                    continue

                if duplicate_face(encoding, known_encodings):
                    print("[❌] This face is already registered.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "[❌] Duplicate face detected. Registration blocked."

                cv2.imwrite(filename, frame)
                known_encodings.append(encoding)
                known_names.append(name)

                with open(encoding_file, "wb") as f:
                    pickle.dump((known_encodings, known_names), f)

                    add_user_to_db(name)

                print(f"[✅] Image saved and encoding added for {name}")
                captured = True
                countdown_started = False

        else:
            cv2.putText(display_frame, "Align your face in the frame", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Face Registration", display_frame)

        if captured:
            time.sleep(1)
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Face registration complete.")
    return "[✅] Registration complete."

if __name__ == "__main__":
    name = input("Enter your name for face registration: ").strip()

    if not name:
        print("[ERROR] Name cannot be empty.")
    elif any(char in name for char in r"\/:*?\"<>|"):
        print("[ERROR] Name contains invalid characters.")
    else:
        register_face(name)
