import pytest
import uuid


def test_sign_new_user(default_client) -> None:
    # Use a unique email for each test run
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@packt.com"
    payload = {
        "email": unique_email,
        "password": "testpassword",
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    test_response = {"message": "User created successfully"}

    response = default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


def test_sign_user_in(default_client) -> None:
    # First create a user for signin test
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@packt.com"
    
    # Create user first
    signup_payload = {
        "email": unique_email,
        "password": "testpassword",
    }
    signup_headers = {"accept": "application/json", "Content-Type": "application/json"}
    signup_response = default_client.post("/user/signup", json=signup_payload, headers=signup_headers)
    assert signup_response.status_code == 200
    
    # Now test signin
    payload = {"username": unique_email, "password": "testpassword"}

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = default_client.post("/user/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
