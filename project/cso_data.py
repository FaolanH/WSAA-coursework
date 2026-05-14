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

if __name__ == "__main__":
    app.run()
