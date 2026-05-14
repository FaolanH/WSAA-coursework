# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python

# import modules needed
from flask import Flask, jsonify, render_template
import requests
import os
from datetime import datetime

app = Flask(__name__)

def get_categories(dataset_id):
    url = f"https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/{dataset_id}/JSON-stat/2.0/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)

    try:
        meta = r.json()
    except:
        return {}

    dims = meta.get("dimension", {})
    categories = {}

    for dim_key, dim_data in dims.items():
        label = dim_data.get("label", dim_key)
        cat_labels = list(dim_data.get("category", {}).get("label", {}).values())
        categories[label] = cat_labels

    return categories


@app.route('/')
def index():

    print("DEBUG CWD:", os.getcwd())
    print("DEBUG FILE:", __file__)

    api_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/2026-05-07/en"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(api_url, headers=headers, timeout=10)

    print("STATUS:", response.status_code)
    print("TEXT:", response.text[:200])

    try:
        data = response.json()
    except Exception as e:
        return f"CSO API returned invalid JSON. Error: {e}"

    items = data.get("link", {}).get("item", [])

    datasets = []
    for item in items:
        raw_date = item.get("updated")

        try:
            dt = datetime.fromisoformat(raw_date)
            formatted_date = dt.strftime("%d %b %Y")
        except:
            formatted_date = raw_date

        dataset_id = item.get("id")[0] if isinstance(item.get("id"), list) else item.get("id")

        categories = get_categories(dataset_id)

        datasets.append({
            "label": item.get("label"),
            "updated": formatted_date,
            "id": dataset_id,
        })

    datasets.sort(key=lambda x: x["updated"], reverse=True)

    return render_template(
        'index.html',
        welcome_text="Welcome to the PxStat Updates API!",
        last_updated="May 2026",
        datasets=datasets
    )

@app.route('/dataset/<dataset_id>')
def dataset_detail(dataset_id):
    categories = get_categories(dataset_id)
    
    # Fetch full dataset metadata
    url = f"https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/{dataset_id}/JSON-stat/2.0/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)

    try:
        meta = r.json()
    except:
        meta = {}

    # Extract dataset label
    label = meta.get("label", dataset_id)

    return render_template(
        'dataset_detail.html',
        dataset_id=dataset_id,
        label=label,
        categories=categories,
        metadata=meta
    )

@app.route('/updated_tables')
def updated_tables():
    return "Here are the tables that have been updated:"
