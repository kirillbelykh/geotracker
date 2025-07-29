from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)

def test_register():
    email = f"user{uuid.uuid4().hex}@example.com"
    password = 'strongpassword'
    client.post('/auth/register', json={
        'email': email,
        'password': password
    })
    
    res = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    
    assert res.status_code == 200
    assert res.json()['message'] == 'Login successful'