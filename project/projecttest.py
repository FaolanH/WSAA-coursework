# Author: Faolán Hamilton
# Project - CSO PXStat API - Tables last updated 
# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

#!flask/bin/python

from flask import Flask
import requests

# API for last updated tables pxstat
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/2026-05-07/en"

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the PxStat Updates API!"

@app.route('/updated_tables')
def updates_tables ():
    return "Here are the tables that have been updated:"

# The postman AI helped me to begin! I needed to visualize the list of updated tables in a user-friendly format. converstation id: 4db2086d-6818-4ebc-add4-1884561d88b4
# When I asked 'Help me add a visualization script', it gave me back the below output
# https://faolanh-9982482.postman.co/workspace/Test~bd1ebf8e-9100-4514-9552-b41f9628ce22/request/54681240-02c1cfb8-be83-48e1-839d-3d4f3e7cb47f?historyId=54681240-d85a23b2-9080-47cb-b4da-ddb71916d4b8&utm_source=postman&utm_medium=response_tab&utm_campaign=core&utm_content=link
