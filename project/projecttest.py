#Author: Faolán Hamilton

#!flask/bin/python

from flask import Flask
import requests

# API for last updated tables pxstat
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadCollection/2026-05-04/en"

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the PxStat Updates API!"

@app.route('/updated_tables')
def updates_tables ():
    return "Here are the tables that have been updated:"

if __name__ == '__main__':
    app.run(debug=True)

response = requests.get(url)
list_of_updated_tables = response.json()
print (response.status_code)

print (list_of_updated_tables['class'])