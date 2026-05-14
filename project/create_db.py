import requests
import sqlite3

DB_NAME = "hpm08.db"
TABLE_NAME = "hpm08"

API_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HPM08/JSON-stat/2.0/en"

def fetch_hpm08():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(API_URL, headers=headers, timeout=10)
    data = response.json()

    dimension = data["dimension"]
    values = data["value"]

    periods = list(dimension["TIME_PERIOD"]["category"]["index"].keys())
    geographies = list(dimension["GEOG"]["category"]["index"].keys())

    rows = []
    idx = 0

    for geo in geographies:
        for period in periods:
            value = values[idx]
            idx += 1

            if value is None:
                continue

            rows.append((period, geo, value))

    return rows


def insert_into_db(rows):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    inserted = 0

    for period, geo, value in rows:
        cur.execute("""
            INSERT INTO hpm08 (period, geography, value)
            VALUES (?, ?, ?)
        """, (period, geo, value))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted


if __name__ == "__main__":
    print("Fetching HPM08 data from CSO...")
    rows = fetch_hpm08()
    print(f"Fetched {len(rows)} rows.")

    print("Inserting into SQLite database...")
    count = insert_into_db(rows)
    print(f"Inserted {count} rows into hpm08 table.")
