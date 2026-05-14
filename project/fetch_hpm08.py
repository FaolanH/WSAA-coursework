import requests
import sqlite3

DB_NAME = "hpm08.db"

API_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HPM08/JSON-stat/2.0/en"

def fetch_hpm08():
    data = requests.get(API_URL).json()

    dims = data["dimension"]
    values = data["value"]

    # Identify dimension keys (excluding metadata keys)
    dim_keys = [k for k in dims.keys() if k not in ["id", "size"]]

    # First dimension = geography
    geo_dim = dim_keys[1]

    # Second dimension = time period
    time_dim = dim_keys[0]

    geographies = list(dims[geo_dim]["category"]["index"].keys())
    periods = list(dims[time_dim]["category"]["index"].keys())

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

    for period, geo, value in rows:
        cur.execute("""
            INSERT INTO hpm08 (period, geography, value)
            VALUES (?, ?, ?)
        """, (period, geo, value))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Fetching HPM08 data...")
    rows = fetch_hpm08()
    print(f"Fetched {len(rows)} rows.")

    print("Inserting into database...")
    insert_into_db(rows)
    print("Done.")
