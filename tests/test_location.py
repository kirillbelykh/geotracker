from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_location():
    email = f'user{uuid4().hex}@example.com'
    password = 'strongpassword'
    client.post('/auth/register', json={
        'email': email,
        'password': password
    })
    
    latitude = 1.123
    longitude = 2.234
    timestamp = str(datetime.now())
    
    login_response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    
    token = login_response.json()['jwt_token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = client.post('/location', json={
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    }, headers=headers)
    
    assert res.status_code == 201
    assert res.json()['message'] == 'Location saved successfully'
    