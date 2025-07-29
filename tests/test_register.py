import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "testuser1@example.com",
        "password": "strongpassword"
    })
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["message"] == "User Created"