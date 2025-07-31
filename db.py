import sqlite3
import pandas as pd  # ← 必要
from datetime import datetime

DB_NAME = "recommendation.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            employee TEXT,
            method TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_record(employee, method):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recommendations (date, employee, method) VALUES (?, ?, ?)",
                   (datetime.today().strftime("%Y-%m-%d"), employee, method))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM recommendations", conn)
    conn.close()
    return df
