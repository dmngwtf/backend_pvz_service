from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.core.security import create_token

client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products; DELETE FROM receptions; DELETE FROM pvzs;")

def test_create_reception():
    setup_database()
    # Создаём ПВЗ
    token_moderator = create_token({"role": "moderator"})
    pvz_response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token_moderator}"}
    )
    pvz_id = pvz_response.json()["id"]

    token_employee = create_token({"role": "employee"})
    response = client.post(
        "/receptions",
        json={"pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert response.status_code == 201
    assert response.json()["pvz_id"] == pvz_id
    assert response.json()["status"] == "in_progress"

def test_create_reception_no_pvz():
    setup_database()
    token_employee = create_token({"role": "employee"})
    response = client.post(
        "/receptions",
        json={"pvz_id": "00000000-0000-0000-0000-000000000000"},
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "PVZ not found"