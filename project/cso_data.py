# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python
from flask import Flask, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():

    print("DEBUG CWD:", os.getcwd())
    print("DEBUG FILE:", __file__)


    api_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/JSON-stat/2.0/en"

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
        datasets.append({
            "label": item.get("label"),
            "updated": item.get("updated"),
            "id": item.get("id")
        })

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