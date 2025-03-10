from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Define the software version
SOFTWARE_VERSION = "1.0.2"

# Define the SenseBox ID and Sensor ID
SENSEBOX_ID = "65e8d93acbf5700007f920ca"
SENSOR_ID = "65e8d93acbf5700007f920cb"

# Function to fetch and calculate the average of measurements from the last hour
def get_average_last_hour():
    # Define the API endpoint
    url = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}/data/{SENSOR_ID}"
    
    # Define query parameters for the last hour
    now = datetime.utcnow()
    one_hour_ago = (now - timedelta(hours=1)).isoformat() + "Z"
    now_iso = now.isoformat() + "Z"
    
    params = {
        "from-date": one_hour_ago,  # Last hour
        "to-date": now_iso,  # Current time
        "format": "json",  # Default is JSON
        "download": "false"  # Set to true if you want to force download
    }
    
    try:
        # Fetch data from the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for errors
        data = response.json()
        
        # Calculate the average of the measurements
        if data and isinstance(data, list):
            values = [float(measurement["value"]) for measurement in data]
            average = sum(values) / len(values) if values else 0
            return {"average": round(average, 2)}  # Round to 2 decimal places
        else:
            return {"error": "No data found for the last hour"}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Home page
@app.route('/')
def home():
    average_data = get_average_last_hour()
    return render_template('home.html', version=SOFTWARE_VERSION, average=average_data)

# API endpoint to refresh average data
@app.route('/refresh_average')
def refresh_average():
    return jsonify(get_average_last_hour())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)