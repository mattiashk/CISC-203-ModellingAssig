from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import parse_sat_test
import json

"""
Defines a Flask API for parsing requested SAT solver test cases.
Includes a route "/parse-test" that accepts POST requests with a JSON payload containing a
test case number.
The API then executes the SAT solver using the test case id.
"""

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/parse-test', methods=['POST'])
def handle_parse_test():
    data = request.get_json()
    print(f"data: {data}")
    if 'test_case' in data:
        test_number = data['test_case']
        response = parse_sat_test(int(test_number))
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "test_number not provided"}), 400

@app.route('/test-cases', methods=['GET'])
def handle_test_cases():
    # Read the test casew JSON file
    with open('tests.config.json', 'r') as file:
        data = json.load(file)

    # Transform data
    transformed_data = [{"Id": str(item["id"]), "Name": item["test"]} for item in data]

    return jsonify(transformed_data)

def run_app():
    app.run(debug=True, host='0.0.0.0', port=5000)