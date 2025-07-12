import streamlit as st
import subprocess
from face_registration import register_face
from encode_faces import encode_faces
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Student Panel - Face Attendance", layout="centered")
st.title("🎓 Student Face Attendance Panel")

attendance_file = "attendance/attendance_log.csv"

# ------------------ Tabs ------------------
tabs = st.tabs(["📸 Register Face", "🧠 Encode Faces", "✅ Mark Attendance"])

# --------------- Tab 1: Register Face ---------------
with tabs[0]:
    st.subheader("📸 Face Registration")
    name = st.text_input("Enter your name:")

    if st.button("Register Face"):
        if not name.strip():
            st.warning("Please enter a valid name.")
        else:
            result = register_face(name.strip())
            if "Duplicate face" in result:
                st.error("❌ This face is already registered with another name.")
            elif "complete" in result.lower():
                st.success(result)
            else:
                st.warning(result)

# --------------- Tab 2: Encode Faces ---------------
with tabs[1]:
    st.subheader("🧠 Encode Faces")
    if st.button("Run Encoding"):
        result = encode_faces()
        st.success(result)

# --------------- Tab 3: Mark Attendance ---------------
with tabs[2]:
    st.subheader("✅ Mark Attendance")
    name_att = st.text_input("Enter your registered name:")

    if st.button("Start Attendance"):
        if not name_att.strip():
            st.warning("Please enter your registered name.")
        else:
            already_marked = False

            # Check if the student has already marked attendance today
            if os.path.exists(attendance_file):
                df = pd.read_csv(attendance_file)
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
                today = datetime.now().date()

                if not df.empty and any((df["Name"] == name_att) & (df["Timestamp"].dt.date == today)):
                    already_marked = True

            if already_marked:
                st.warning(f"⚠️ Attendance already marked today for '{name_att}'.")
            else:
                with st.spinner("Detecting faces and marking attendance..."):
                    result = subprocess.run(["python", "attendance_system.py"], capture_output=True, text=True)
                    output = result.stdout.strip()

                    if name_att in output:
                        st.success(f"✅ Attendance marked for {name_att}")
                    else:
                        st.error("❌ Face not detected or name mismatch.")
