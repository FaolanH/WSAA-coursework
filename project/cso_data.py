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
    - Extracts label, last updated date, and dataset ID
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

        # Some APIs return id as ["FIQ01"], others as "FIQ01"
        dataset_id = item.get("id")[0] if isinstance(item.get("id"), list) else item.get("id")

        datasets.append({
            "label": item.get("label"),
            "updated": formatted_date,
            "id": dataset_id
        })

    # Sort by updated date
    datasets.sort(key=lambda x: x["updated"], reverse=True)

    return render_template(
        'index.html',
        welcome_text="Welcome to the PxStat Updates API!",
        last_updated="May 2026",
        datasets=datasets
    )


@app.route('/dataset/<dataset_id>')
def dataset_detail(dataset_id):
    """
    Detail page for a single dataset:
    - Calls the CSO 'ReadDataset' endpoint
    - Shows raw metadata and basic info
    """

    url = f"https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/{dataset_id}/JSON-stat/2.0/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)

    try:
        meta = r.json()
    except Exception:
        meta = {}

    label = meta.get("label", dataset_id)

    return render_template(
        'dataset_detail.html',
        dataset_id=dataset_id,
        label=label,
        metadata=meta
    )


if __name__ == "__main__":
    app.run()