"""
Integration tests for the Users API
Run with: pytest tests/usuarios/test_api_integration.py
"""
import pytest
import requests

BASE_URL = "http://127.0.0.1:5001"

# Test data
users = [
    {
        "firstName": "Juan",
        "middleName": "Carlos",
        "surName1": "Pérez",
        "surName2": "Gómez",
        "bornDate": "1990-05-10",
        "department": "Cundinamarca",
        "municipality": "Bogotá",
        "trail": "urbano",
        "email": "juan.perez@hotmail.com",
        "typeDocument": "CC",
        "numberDocument": "100000001",
        "phoneNumber": "3001234567",
        "hashPassword": "password123",
        "username": "juanperez"
    },
    {
        "firstName": "Ana",
        "middleName": "María",
        "surName1": "Rodríguez",
        "surName2": "López",
        "bornDate": "1985-08-20",
        "department": "Antioquia",
        "municipality": "Medellín",
        "trail": "rural",
        "email": "ana.rodriguez@hotmail.com",
        "typeDocument": "CC",
        "numberDocument": "100000002",
        "phoneNumber": "3012345678",
        "hashPassword": "password456",
        "username": "anarodriguez"
    }
]

@pytest.mark.parametrize("user", users)
def test_register_user(user):
    resp = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp.status_code == 200 or resp.status_code == 201
    data = resp.json()
    assert "_id" in data
    user["_id"] = data["_id"]

@pytest.mark.parametrize("user", users)
def test_get_user_by_id(user):
    # Register user first
    reg = requests.post(f"{BASE_URL}/users/register", json=user)
    user_id = reg.json().get("_id")
    resp = requests.get(f"{BASE_URL}/users/getById/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == user["email"]

@pytest.mark.parametrize("user", users)
def test_get_user_by_email(user):
    # Register user first
    reg = requests.post(f"{BASE_URL}/users/register", json=user)
    email = user["email"]
    resp = requests.get(f"{BASE_URL}/users/getByEmail/{email}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == user["username"]

@pytest.mark.parametrize("user", users)
def test_authenticate_user(user):
    # Register user first
    reg = requests.post(f"{BASE_URL}/users/register", json=user)
    data = {"email": user["email"], "hashPassword": user["hashPassword"]}
    resp = requests.post(f"{BASE_URL}/users/autenticate/", json=data)
    assert resp.status_code == 200
    auth_data = resp.json()
    assert auth_data["username"] == user["username"]

@pytest.mark.parametrize("user", users)
def test_authenticate_wrong_password(user):
    # Register user first
    reg = requests.post(f"{BASE_URL}/users/register", json=user)
    data = {"email": user["email"], "hashPassword": "wrongpass"}
    resp = requests.post(f"{BASE_URL}/users/autenticate/", json=data)
    assert resp.status_code == 401 or resp.status_code == 400

# Add more tests for edge cases as needed


def test_duplicate_registration():
    """Should not allow duplicate registration by email or document"""
    user = {
        "firstName": "Test",
        "middleName": "Dup",
        "surName1": "User",
        "surName2": "Case",
        "bornDate": "1995-01-01",
        "department": "TestDept",
        "municipality": "TestCity",
        "trail": "urbano",
        "email": "duplicate@example.com",
        "typeDocument": "CC",
        "numberDocument": "999999999",
        "phoneNumber": "3000000000",
        "hashPassword": "testpass",
        "username": "testdup"
    }
    # Register once
    resp1 = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp1.status_code in (200, 201)
    # Register again (should fail)
    resp2 = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp2.status_code in (400, 409)


@pytest.mark.parametrize("field", [
    "email", "hashPassword", "username", "numberDocument"
])
def test_registration_missing_required_field(field):
    """Should fail if required field is missing"""
    user = users[0].copy()
    user.pop(field)
    resp = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp.status_code in (400, 422)


def test_registration_invalid_email():
    user = users[0].copy()
    user["email"] = "not-an-email"
    resp = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp.status_code in (400, 422)


def test_registration_empty_fields():
    user = users[0].copy()
    user["email"] = ""
    user["username"] = ""
    resp = requests.post(f"{BASE_URL}/users/register", json=user)
    assert resp.status_code in (400, 422)


def test_registration_extra_fields():
    user = users[0].copy()
    user["extraField"] = "shouldBeIgnoredOrRejected"
    resp = requests.post(f"{BASE_URL}/users/register", json=user)
    # Accept 200/201 if extra fields are ignored, 400/422 if rejected
    assert resp.status_code in (200, 201, 400, 422)


def test_authenticate_missing_fields():
    data = {"email": users[0]["email"]}  # missing password
    resp = requests.post(f"{BASE_URL}/users/autenticate/", json=data)
    assert resp.status_code in (400, 422)
    data = {"hashPassword": users[0]["hashPassword"]}  # missing email
    resp = requests.post(f"{BASE_URL}/users/autenticate/", json=data)
    assert resp.status_code in (400, 422)


def test_invalid_http_methods():
    # GET on register (should not be allowed)
    resp = requests.get(f"{BASE_URL}/users/register")
    assert resp.status_code in (404, 405)
    # POST on getById (should not be allowed)
    resp = requests.post(f"{BASE_URL}/users/getById/{users[0]['numberDocument']}")
    assert resp.status_code in (404, 405)
