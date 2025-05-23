
from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import logging
import os
import sys # For stdout logging

# Configure logging to stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Define the software version
SOFTWARE_VERSION = os.environ.get("SOFTWARE_VERSION")

# Define the SenseBox ID and Sensor ID
SENSEBOX_ID = os.environ.get("SENSEBOX_ID")
SENSOR_ID = os.environ.get("SENSOR_ID")

print("SOFTWARE_VERSION:", SOFTWARE_VERSION)
print("SENSEBOX_ID:", SENSEBOX_ID)
print("SENSOR_ID:", SENSOR_ID)
print("---------------------------------------")


# Configuration for NotificationApp and Temperature Threshold
NOTIFICATION_APP_URL = os.environ.get("NOTIFICATION_APP_URL", "http://notificationapp:5002/send_notification")
# Default threshold set to 2.0 for easier testing if data values are around 5.0
TEMPERATURE_THRESHOLD = float(os.environ.get("TEMPERATURE_THRESHOLD", "2.0"))


def trigger_notification(data_for_notification):
    try:
        headers = {'Content-Type': 'application/json'}
        logger.info(f"Attempting to send notification to {NOTIFICATION_APP_URL} with payload: {data_for_notification}")
        response = requests.post(NOTIFICATION_APP_URL, json=data_for_notification, headers=headers, timeout=10) # Increased timeout
        response.raise_for_status()
        logger.info(f"Successfully sent notification: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error calling NotificationApp at {NOTIFICATION_APP_URL}")
        return False
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error calling NotificationApp at {NOTIFICATION_APP_URL}. Ensure NotificationApp is running and accessible.")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling NotificationApp: {e}")
        return False

def get_average_last_hour():
    url = f"https://api.opensensemap.org/boxes/{SENSEBOX_ID}/data/{SENSOR_ID}"
    now = datetime.utcnow()
    one_hour_ago = (now - timedelta(hours=1)).isoformat() + "Z"
    now_iso = now.isoformat() + "Z"
    params = {"from-date": one_hour_ago, "to-date": now_iso, "format": "json", "download": "false"}

    try:
        response = requests.get(url, params=params, timeout=10) # Added timeout
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list):
            values = [float(measurement["value"]) for measurement in data if "value" in measurement]
            if not values: # Handles if all measurements lack 'value' or list is empty after filtering
                 logger.warning("No valid measurement values found in the data.")
                 return {"error": "No valid measurement values found for the last hour"}

            average = sum(values) / len(values)
            average_rounded = round(average, 2)

            logger.info(f"Calculated average temperature: {average_rounded}°C")

            if average_rounded > TEMPERATURE_THRESHOLD:
                logger.info(f"Temperature {average_rounded}°C exceeded threshold of {TEMPERATURE_THRESHOLD}°C. Triggering notification.")
                notification_payload = {
                    "sensor_id": SENSOR_ID,
                    "box_id": SENSEBOX_ID,
                    "average_temperature": average_rounded,
                    "threshold": TEMPERATURE_THRESHOLD,
                    "timestamp": now_iso,
                    "message": f"Alert: Average temperature {average_rounded}°C is above the threshold of {TEMPERATURE_THRESHOLD}°C."
                }
                trigger_notification(notification_payload)
            
            return {"average": average_rounded}
        else:
            logger.info("No data found from OpenSenseMap for the last hour or data is not in expected list format.")
            return {"error": "No data found for the last hour"}

    except requests.exceptions.Timeout:
        logger.error("Timeout error fetching data from OpenSenseMap API.", exc_info=True)
        return {"error": "Timeout fetching sensor data. Please try again later."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from OpenSenseMap API: {e}", exc_info=True)
        return {"error": "An internal error has occurred while fetching sensor data. Please try again later."}
    except ValueError as e:
        logger.error(f"Error converting measurement value to float: {e}", exc_info=True)
        return {"error": "Error processing sensor data values."}
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_average_last_hour: {e}", exc_info=True)
        return {"error": "An unexpected error occurred."}


@app.route('/')
def home():
    average_data = get_average_last_hour()
    return render_template('home.html', version=SOFTWARE_VERSION, average=average_data, threshold=TEMPERATURE_THRESHOLD)

@app.route('/refresh_average')
def refresh_average():
    return jsonify(get_average_last_hour())

if __name__ == '__main__':
    # For local development, you might want debug=True, but False for production/K8s prep
    app.run(host='0.0.0.0', port=5000, debug=False)