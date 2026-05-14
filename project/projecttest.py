# Author: Faolán Hamilton
# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python
from flask import Flask, jsonify, render_template
import requests


    return render_template(
        'index.html',
        label=data.get("label"),
        updated=data.get("updated"),
        ids=data.get("id")
    )


app = Flask(__name__)

@app.route('/')
def index():
    api_url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/PEA01/JSON-stat/2.0/en"

    data = requests.get(api_url).json()

    return render_template(
        'index.html',
        welcome_text="Welcome to the PxStat Updates API!",
        last_updated="May 2026",
        label=data.get("label"),
        updated=data.get("updated"),
        ids=data.get("id")
    )

@app.route('/updated_tables')
def updated_tables():
    return "Here are the tables that have been updated:"