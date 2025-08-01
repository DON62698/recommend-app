import pandas as pd
from datetime import datetime
import os

CSV_FILE = "recommendations.csv"

def init_data():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["date", "employee", "method"])
        df.to_csv(CSV_FILE, index=False)

def add_record(employee, method, count=1):
    date_today = datetime.today().strftime("%Y-%m-%d")
    new_rows = pd.DataFrame([{"date": date_today, "employee": employee, "method": method}] * count)
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, new_rows], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def get_all_records():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["date", "employee", "method"])
    return pd.read_csv(CSV_FILE)

