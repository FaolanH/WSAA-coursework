import sqlite3
import csv

DB_NAME = "hpm08.db"
CSV_FILE = "HPM08.2025-2026.csv"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows_inserted = 0

    for row in reader:
        period = row["MONTH"]
        geography = row["GEOG"]
        value = row["VALUE"]

        cur.execute("""
            INSERT INTO hpm08 (period, geography, value)
            VALUES (?, ?, ?)
        """, (period, geography, value))

        rows_inserted += 1

conn.commit()
conn.close()

print(f"Inserted {rows_inserted} rows.")
