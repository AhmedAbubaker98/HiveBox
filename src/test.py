import pytest
import json
from app import app, get_sensor_data

# Flask provides a test client for simulating requests
@pytest.fixture
def client():
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as client:
        yield client

# 1️⃣ **Unit Test**: Test the get_sensor_data function (Mocking API Call)
def test_get_sensor_data(mocker):
    mock_response = {
        "sensors": [
            {
                "_id": "12345",
                "title": "Temperature",
                "lastMeasurement": {"value": "22.5", "createdAt": "2025-03-04T12:00:00Z"}
            }
        ]
    }
    
    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response, status_code=200))
    
    data = get_sensor_data()
    assert "sensors" in data
    assert data["sensors"][0]["title"] == "Temperature"

# 2️⃣ **Endpoint Test**: Test the Home Page (`/`)
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sensor Data" in response.data  # Ensure page has expected content

# 3️⃣ **Endpoint Test**: Test the `/refresh_sensors` API
def test_refresh_sensors(client, mocker):
    mock_response = {
        "sensors": [
            {
                "_id": "12345",
                "title": "Temperature",
                "lastMeasurement": {"value": "22.5", "createdAt": "2025-03-04T12:00:00Z"}
            }
        ]
    }
    
    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response, status_code=200))

    response = client.get("/refresh_sensors")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "sensors" in data
    assert data["sensors"][0]["title"] == "Temperature"
