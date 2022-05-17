import os
import json

from flask import Flask, request, jsonify
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()

# The function is used to fetch sales data in a specific date.
def fetch_sales_data(date):
    query = datastore_client.query(kind="sales_data")
    query.add_filter("date", "=", date)
    results = list(query.fetch())
    return results
    
# index page shows how to use this API to acquire data.
@app.route('/')
def index():
    return 'Please send a GET request to "/json_data/<date>" to acquire data. Format of "date": "YYYY-MM-DD."' 


# Received a get request and response sales data in that date. 
@app.route('/json_data/<date>', methods=['GET'])
def get_sales_data_by_date(date):
    # Call function to fetch sales data in a specific date.
    res = fetch_sales_data(date)
    if len(res) != 0:
        # There is a sales data exists on that date. 
        return jsonify(res), 200  
    else:
        # No sales data was found.
        error = {"Error": "There is no sales data in the date."}
        return jsonify(error), 404


# Customization way to hand a 405 error.
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'Error': "This endpoint only allowed GET method."}), 405

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)