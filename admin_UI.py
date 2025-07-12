import streamlit as st
import pandas as pd
import os

# Configuration
ADMIN_PASSWORD = "admin123"  # You may store this in an environment variable
attendance_file = "attendance/attendance_log.csv"

st.set_page_config(page_title="Admin - Attendance System", layout="centered")
st.title("🔐 Admin Panel - Face Attendance System")

# -------------------- Password Auth --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔑 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login successful.")
            st.rerun()
        else:
            st.error("❌ Incorrect password.")

# -------------------- Main Interface After Login --------------------
if st.session_state.authenticated:
    tab = st.tabs(["📄 View Logs"])[0]  # Only one tab

    with tab:
        st.subheader("📄 Attendance Logs")

        if os.path.exists(attendance_file):
            df = pd.read_csv(attendance_file)
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Date"] = df["Timestamp"].dt.date

            st.markdown("### 🔍 Filter Logs")
            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                names = df["Name"].unique()
                selected_name = st.selectbox("Select Student", options=["All"] + list(names))

            with filter_col2:
                dates = df["Date"].unique()
                selected_date = st.selectbox("Select Date", options=["All"] + sorted(dates, reverse=True))

            # Apply Filters
            filtered_df = df.copy()
            if selected_name != "All":
                filtered_df = filtered_df[filtered_df["Name"] == selected_name]
            if selected_date != "All":
                filtered_df = filtered_df[filtered_df["Date"] == selected_date]

            st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
            st.success(f"✅ Showing {len(filtered_df)} records")

        else:
            st.warning("📁 No attendance logs found.")

    # ---------- Logout ----------
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.rerun()
