import sqlite3

conn = sqlite3.connect("hpm08.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS hpm08 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT NOT NULL,
    geography TEXT NOT NULL,
    value REAL
)
""")

conn.commit()
conn.close()

print("Database and table created.")
