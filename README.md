# 📸 Face Recognition Attendance System

A real-time, intelligent face recognition-based attendance management system built using **Python**, **OpenCV**, **face_recognition**, and **Streamlit**. This system enables both **students** and **admins** to interact through separate panels, securely register faces, mark attendance, and view attendance logs—all stored and filtered through a connected **SQLite database**.

---

## 🚀 Features

### 👨‍🎓 Student Panel (`Student_UI.py`)
- 📸 Register face with countdown timer.
- 🧠 Encode facial embeddings and store securely.
- ✅ Mark attendance via webcam in real-time.
- 🔁 Prevents multiple attendance marks in a day.
- ❌ Duplicate face detection during registration.

### 🔐 Admin Panel (`admin_UI.py`)
- 🔑 Secure admin login with password.
- 📄 View complete attendance logs.
- 🔍 Filter by student name and date.
- 🧠 Backend powered by SQLite (`attendance.db`).

---

## 🗂️ Project Structure

```plaintext
Attendance-management-system/
│
├── attendance/           # Stores CSV logs (if used)
├── database/             # SQLite DB and helpers
├── dataset/              # Registered face images
├── embeddings/           # Pickle file of face encodings
│
├── Student_UI.py         # Streamlit app for students
├── admin_UI.py           # Streamlit app for admin
├── face_registration.py  # Face capture & validation
├── encode_faces.py       # Generate face embeddings
├── attendance_system.py  # Attendance recognition script
├── database.py           # SQLite connection & logic
│
├── README.md             # Project overview and instructions
├── requirements.txt      # Python dependencies
└── .gitignore
