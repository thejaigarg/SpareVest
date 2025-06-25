# Auth tests
import pytest
from fastapi.testclient import TestClient
from app.main import app    

def test_user_login_and_get_current_user(client):
    # 1. Register a new user (or create one in the DB beforehand!)
    response = client.post("/users/", json={
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "test1234"
    })
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "testuser@example.com"

    # 2. Login to get JWT token
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",   # OAuth2 uses 'username' param even if you use email
        "password": "test1234"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. Call /users/me with this JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "testuser@example.com"

def test_login_wrong_password(client):
    # The user should already exist from the previous test, or create again as needed.
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"