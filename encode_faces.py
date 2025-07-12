import face_recognition
import os
import pickle

def encode_faces(dataset_dir="dataset", output_file="embeddings/faces.pkl"):
    print("[INFO] Encoding registered faces...")
    known_encodings = []
    known_names = []

    os.makedirs("embeddings", exist_ok=True)

    for file in os.listdir(dataset_dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            name = file.split(".")[0]
            image_path = os.path.join(dataset_dir, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
                print(f"[INFO] Encoded face for: {name}")
            else:
                print(f"[WARNING] No face found in {file}, skipping...")

    with open(output_file, "wb") as f:
        pickle.dump((known_encodings, known_names), f)
        print(f"[INFO] Encodings saved to: {output_file}")


if __name__ == "__main__":
    encode_faces()
