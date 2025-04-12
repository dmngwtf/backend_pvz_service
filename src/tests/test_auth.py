from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db

client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users;")

def test_dummy_login_employee():
    response = client.post("/auth/dummyLogin", json={"role": "employee"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_dummy_login_moderator():
    response = client.post("/auth/dummyLogin", json={"role": "moderator"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_dummy_login_invalid_role():
    response = client.post("/auth/dummyLogin", json={"role": "invalid"})
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid role. Must be 'employee' or 'moderator'"

def test_register():
    setup_database()  # Очищаем базу перед тестом
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password", "role": "employee"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "employee"

def test_register_duplicate_email():
    setup_database()
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password", "role": "employee"}
    )
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password", "role": "employee"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

def test_login():
    setup_database()
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password", "role": "employee"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid():
    setup_database()
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"