from flask import Flask, request, jsonify
import logging
import sys

# Configure logging to stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

app = Flask(__name__)

APP_VERSION = "1.0.0"
SERVICE_NAME = "NotificationApp"

@app.route('/')
def home():
    logger.info(f"{SERVICE_NAME} root endpoint was called.")
    return jsonify(service=SERVICE_NAME, version=APP_VERSION, message=f"Welcome to {SERVICE_NAME}")

@app.route('/send_notification', methods=['POST'])
def send_notification():
    if not request.is_json:
        logger.warning("Received non-JSON request for /send_notification")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    if not data:
        logger.warning("Received empty JSON payload for /send_notification")
        return jsonify({"status": "error", "message": "No data provided in JSON payload"}), 400
    
    # Simulate sending a notification
    logger.info(f"NotificationApp: Processing notification for data: {data}")
    # In a real app, you'd integrate with an email/SMS service, queue, etc.
    
    return jsonify({"status": "success", "message": "Notification processed", "data_received": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)