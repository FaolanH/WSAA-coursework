# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python

from flask import Flask, render_template
import requests
from datetime import datetime

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

        # Format the updated date nicely
        try:
            dt = datetime.fromisoformat(raw_date)
            formatted_date = dt.strftime("%d %b %Y")
        except Exception:
            formatted_date = raw_date

        datasets.append({
            "label": item.get("label"),
            "updated": formatted_date
        })

    # Sort by updated date
    datasets.sort(key=lambda x: x["updated"], reverse=True)

    return render_template(
        'index.html',
        datasets=datasets
    )


if __name__ == "__main__":
    app.run()
