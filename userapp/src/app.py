from flask import Flask, jsonify
import logging
import sys

# Configure logging to stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

app = Flask(__name__)

APP_VERSION = "1.0.0"
SERVICE_NAME = "UserApp"

@app.route('/')
def home():
    logger.info(f"{SERVICE_NAME} root endpoint was called.")
    return jsonify(service=SERVICE_NAME, version=APP_VERSION, message=f"Welcome to {SERVICE_NAME}")

@app.route('/users/<user_id>')
def get_user(user_id):
    logger.info(f"Request received for user_id: {user_id}")
    # Dummy user data
    user_data = {
        "user_id": user_id,
        "name": f"Test User {user_id}",
        "email": f"testuser{user_id}@example.com",
        "status": "active"
    }
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)