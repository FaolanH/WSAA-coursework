# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    api_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/JSON-stat/2.0/en"
    data = requests.get(api_url).json()

    # Extract the list of datasets
    items = data.get("link", {}).get("item", [])

    # Build a clean list of only the fields you want
    datasets = []
    for item in items:
        datasets.append({
            "label": item.get("label"),
            "updated": item.get("updated"),
            "id": item.get("id")
        })

    # Sort newest → oldest
    datasets.sort(key=lambda x: x["updated"], reverse=True)

    return render_template(
        'index.html',
        welcome_text="Welcome to the PxStat Updates API!",
        last_updated="May 2026",
        datasets=datasets
    )


@app.route('/updated_tables')
def updated_tables():
    return "Here are the tables that have been updated:"