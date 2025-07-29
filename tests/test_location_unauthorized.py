from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

def test_location_unauthorized():
    email = f'user{uuid4().hex}@example.com'
    password = 'strongpassword'
    
    client.post('/auth/register', json={
        'email': email,
        'password': password
    })
    
    client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    
    unauthorized_response = client.post('/location', json={
        'latitude': 1.123,
        'longitude': 2.234,
        'timestamp': datetime.now().isoformat()
    })
    
    assert unauthorized_response.status_code == 401
    assert unauthorized_response.json()['detail'] == 'Not authenticated'