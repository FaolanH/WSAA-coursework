# Project - CSO PXStat API - Tables last updated
# Using the CSO PXStat API to list recently updated tables.

#!flask/bin/python

from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    """
    Home page:
    - Calls the CSO 'ReadCollection' endpoint for a given date
    - Extracts label and last updated date
    - Passes a clean list of datasets to the template
    """

    api_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/2026-05-07/en"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(api_url, headers=headers, timeout=10)

    try:
        data = response.json()
    except Exception as e:
        return f"CSO API returned invalid JSON. Error: {e}"

    items = data.get("link", {}).get("item", [])

    datasets = []
    for item in items:
        raw_date = item.get("updated")

        # Parse ISO date into datetime object
        try:
            dt = datetime.fromisoformat(raw_date)
            formatted_date = dt.strftime("%d %b %Y")
        except Exception:
            dt = None
            formatted_date = raw_date

        datasets.append({
            "label": item.get("label"),
            "updated": formatted_date,
            "sort_date": dt
        })

    # Sort by real datetime (fallback to string if needed)
    datasets.sort(key=lambda x: x["sort_date"] or x["updated"], reverse=True)

    return render_template('index.html', datasets=datasets)


DB = "hpm08.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/hpm08")
def hpm08_list():
    conn = get_db()
    rows = conn.execute("SELECT * FROM hpm08 ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("hpm08_list.html", rows=rows)

@app.route("/hpm08/add", methods=["GET", "POST"])
def hpm08_add():
    if request.method == "POST":
        period = request.form["period"]
        geography = request.form["geography"]
        value = request.form["value"]

        conn = get_db()
        conn.execute(
            "INSERT INTO hpm08 (period, geography, value) VALUES (?, ?, ?)",
            (period, geography, value)
        )
        conn.commit()
        conn.close()

        return redirect("/hpm08")

    return render_template("hpm08_add.html")

@app.route("/hpm08/edit/<int:id>", methods=["GET", "POST"])
def hpm08_edit(id):
    conn = get_db()

    if request.method == "POST":
        period = request.form["period"]
        geography = request.form["geography"]
        value = request.form["value"]

        conn.execute(
            "UPDATE hpm08 SET period=?, geography=?, value=? WHERE id=?",
            (period, geography, value, id)
        )
        conn.commit()
        conn.close()
        return redirect("/hpm08")

    row = conn.execute("SELECT * FROM hpm08 WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("hpm08_edit.html", row=row)

@app.route("/hpm08/delete/<int:id>")
def hpm08_delete(id):
    conn = get_db()
    conn.execute("DELETE FROM hpm08 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/hpm08")




if __name__ == "__main__":
    app.run()
