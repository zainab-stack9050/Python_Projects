import sqlite3
import os
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_records.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
from datetime import datetime

def save_record(name, weight, height, bmi, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO records (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, weight, height, bmi, category, date_now))
    conn.commit()
    conn.close()

def get_user_history(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bmi, date FROM records
        WHERE name = ?
        ORDER BY date ASC
    """, (name,))
    results = cursor.fetchall()
    conn.close()
    return results