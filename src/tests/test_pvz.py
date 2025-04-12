from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.core.security import create_token

client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products; DELETE FROM receptions; DELETE FROM pvzs;")

def test_create_pvz_moderator():
    setup_database()
    token = create_token({"role": "moderator"})
    response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["city"] == "Москва"

def test_create_pvz_invalid_city():
    setup_database()
    token = create_token({"role": "moderator"})
    response = client.post(
        "/pvz",
        json={"city": "Сочи"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid city"

def test_create_pvz_unauthorized():
    setup_database()
    token = create_token({"role": "employee"})
    response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Requires moderator role"

def test_get_pvz_list():
    setup_database()
    token = create_token({"role": "employee"})
    response = client.get(
        "/pvz?page=1&limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)