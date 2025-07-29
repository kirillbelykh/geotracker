from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4 
from datetime import datetime
client = TestClient(app)

def test_latest_location():
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
    
    client.post('/location/', json={
        'latitude': 1.23,
        'longitude': 2.233,
        'timestamp': datetime.now().isoformat()
    }, headers=headers)
    
    latest_location_response = client.get('/location/latest', headers=headers)
    
    assert latest_location_response.status_code == 200
    