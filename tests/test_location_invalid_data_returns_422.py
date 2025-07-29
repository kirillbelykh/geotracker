from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_location_invalid_data_returns_422():
    email = f'user{uuid4().hex}@example.com'
    password = 'strongpassword'
    
    client.post('/auth/register', json={
        'email': email,
        'password': password
    })
    
    login_response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    
    token = login_response.json()['jwt_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    invalid_data_response = client.post('/location', json={
        'latitude': 'not_a_float',
        'longitude': 2.234,
        'timestamp': datetime.now().isoformat()
    }, headers=headers)
    
    assert invalid_data_response.status_code == 422
   