from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime, timedelta

client = TestClient(app)

def test_location_history():
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
    latitude = 3.214
    longitude = 5.213
    
    client.post('/location', json={
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': datetime.now().isoformat()
    }, headers=headers)
    
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    
    loc_history_response = client.get('/location/history', params={
        'start_date': start_date,
        'end_date': end_date
    }, headers=headers)
    
    assert loc_history_response.status_code == 200
    