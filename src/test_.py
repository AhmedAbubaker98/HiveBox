import pytest
import json
from app import app, get_average_last_hour

# Flask provides a test client for simulating requests
@pytest.fixture
def client():
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as client:
        yield client

# 1️⃣ **Unit Test**: Test the get_average_last_hour function (Mocking API Call)
def test_get_average_last_hour(mocker):
    mock_response = [
        {"createdAt": "2025-03-06T06:36:25.489Z", "value": "5.40"},
        {"createdAt": "2025-03-06T06:36:35.489Z", "value": "6.50"},
        {"createdAt": "2025-03-06T06:36:45.489Z", "value": "4.90"},
    ]
    
    # Create a mock response object
    mock_requests_get = mocker.Mock()
    mock_requests_get.json.return_value = mock_response
    mock_requests_get.status_code = 200

    # Mock requests.get to return the mock response object
    mocker.patch("requests.get", return_value=mock_requests_get)
    
    data = get_average_last_hour()
    assert "average" in data
    assert data["average"] == 5.27  # (5.40 + 6.50 + 4.90) / 3 = 5.27

# 2️⃣ **Endpoint Test**: Test the Home Page (`/`)
def test_home_page(client, mocker):
    mock_response = [
        {"createdAt": "2025-03-06T06:36:25.489Z", "value": "5.40"},
        {"createdAt": "2025-03-06T06:36:35.489Z", "value": "6.50"},
        {"createdAt": "2025-03-06T06:36:45.489Z", "value": "4.90"},
    ]
    
    # Mock the get_average_last_hour to return our mock data
    mocker.patch("app.get_average_last_hour", return_value={"average": 5.27})
    
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sensor Data" in response.data  # Ensure page has expected content
    assert b"Average: 5.27" in response.data  # Ensure the average value is shown

# 3️⃣ **Endpoint Test**: Test the `/refresh_average` API
def test_refresh_average(client, mocker):
    mock_response = [
        {"createdAt": "2025-03-06T06:36:25.489Z", "value": "5.40"},
        {"createdAt": "2025-03-06T06:36:35.489Z", "value": "6.50"},
        {"createdAt": "2025-03-06T06:36:45.489Z", "value": "4.90"},
    ]
    
    # Mock the get_average_last_hour to return our mock data
    mocker.patch("app.get_average_last_hour", return_value={"average": 5.27})

    response = client.get("/refresh_average")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "average" in data
    assert data["average"] == 5.27
