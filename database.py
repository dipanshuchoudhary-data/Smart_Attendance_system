import sqlite3
from datetime import datetime, date
import os

# Ensure the database directory exists
os.makedirs("database", exist_ok=True)
DB_PATH = "database/attendance.db"

# ---------- Initialization ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        registered_on TEXT NOT NULL
    )
    """)

    # Attendance Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# ---------- Face Registration ----------
def add_user_to_db(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if name already exists
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    result = cur.fetchone()

    if not result:
        registered_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO users (name, registered_on) VALUES (?, ?)", (name, registered_on))
        conn.commit()
        print(f"[DB ✅] User '{name}' registered in database.")
    else:
        print(f"[DB ⚠️] User '{name}' already exists in database.")

    conn.close()

# ---------- Attendance Logging ----------
def log_attendance_to_db(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if already marked today
    today = date.today().isoformat()
    cur.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, today))
    exists = cur.fetchone()

    if not exists:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO attendance (name, timestamp, date) VALUES (?, ?, ?)", (name, timestamp, today))
        conn.commit()
        print(f"[DB ✅] Attendance logged for {name} at {timestamp}")
    else:
        print(f"[DB ⚠️] {name} already marked attendance today in DB.")

    conn.close()

# ---------- Run once to initialize ----------
if __name__ == "__main__":
    init_db()
    print("[INFO] SQLite database initialized.")
