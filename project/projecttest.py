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

# I have decided to make my project relevant to my work - this means looking at the api last updated tables on PxStat for CSO data. 

# The postman AI helped me to begin! I needed to visualize the list of updated tables in a user-friendly format. converstation id: 4db2086d-6818-4ebc-add4-1884561d88b4

# https://faolanh-9982482.postman.co/workspace/Test~bd1ebf8e-9100-4514-9552-b41f9628ce22/request/54681240-02c1cfb8-be83-48e1-839d-3d4f3e7cb47f?historyId=54681240-d85a23b2-9080-47cb-b4da-ddb71916d4b8&utm_source=postman&utm_medium=response_tab&utm_campaign=core&utm_content=link

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Visualization Script
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Visualization Script

const template = `
<style>
  body { font-family: Arial, sans-serif; padding: 16px; background: #f9f9f9; }
  h2 { color: #333; margin-bottom: 12px; }
  table { border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden; }
  th { background: #4a90d9; color: #fff; padding: 10px 14px; text-align: left; font-size: 14px; }
  td { padding: 9px 14px; font-size: 13px; color: #444; border-bottom: 1px solid #eee; }
  tr:last-child td { border-bottom: none; }
  tr.even td { background: #f2f7fd; }
  tr.odd td { background: #ffffff; }
  .no-data { color: #888; font-style: italic; padding: 16px; }
</style>
<h2>CSO Dataset Overview</h2>
{{#if items.length}}
<table>
  <thead>
    <tr>
      <th>#</th>
      <th>Dataset Label</th>
      <th>Years Available</th>
      <th>Number of Data Points</th>
    </tr>
  </thead>
  <tbody>
    {{#each items}}
    <tr class="{{rowClass}}">
      <td>{{index}}</td>
      <td>{{label}}</td>
      <td>{{years}}</td>
      <td>{{dataPoints}}</td>
    </tr>
    {{/each}}
  </tbody>
</table>
{{else}}
<p class="no-data">No data available.</p>
{{/if}}
`;

function createPayload() {
  try {
    const json = pm.response.json();
    const rawItems = (json && json.link && Array.isArray(json.link.item)) ? json.link.item : [];

    if (rawItems.length === 0) {
      return { items: [] };
    }

    const items = rawItems.map(function(item, i) {
      const label = item.label || '(no label)';

      // Extract years from TLIST(A1) category index
      let years = 'N/A';
      try {
        const tlist = item.dimension && item.dimension['TLIST(A1)'];
        const idx = tlist && tlist.category && tlist.category.index;
        if (Array.isArray(idx) && idx.length > 0) {
          const sorted = idx.slice().sort();
          years = sorted[0] + ' – ' + sorted[sorted.length - 1] + ' (' + sorted.length + ' yrs)';
        }
      } catch (e) {}

      const dataPoints = Array.isArray(item.value) ? item.value.length : 0;

      return {
        index: i + 1,
        label: label,
        years: years,
        dataPoints: dataPoints,
        rowClass: i % 2 === 0 ? 'even' : 'odd'
      };
    });

    return { items: items };
  } catch (e) {
    return { items: [] };
  }
}

pm.visualizer.set(template, createPayload());
