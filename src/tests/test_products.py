from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.core.security import create_token

client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products; DELETE FROM receptions; DELETE FROM pvzs;")

def test_add_product():
    setup_database()
    # Создаём ПВЗ
    token_moderator = create_token({"role": "moderator"})
    pvz_response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token_moderator}"}
    )
    pvz_id = pvz_response.json()["id"]

    # Создаём приёмку
    token_employee = create_token({"role": "employee"})
    reception_response = client.post(
        "/receptions",
        json={"pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )

    # Добавляем товар
    response = client.post(
        "/products",
        json={"type": "электроника", "pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert response.status_code == 201
    assert response.json()["type"] == "электроника"

def test_delete_last_product():
    setup_database()
    token_moderator = create_token({"role": "moderator"})
    pvz_response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token_moderator}"}
    )
    pvz_id = pvz_response.json()["id"]

    token_employee = create_token({"role": "employee"})
    client.post(
        "/receptions",
        json={"pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    client.post(
        "/products",
        json={"type": "электроника", "pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )

    response = client.post(
        f"/pvz/{pvz_id}/delete_last_product",
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted"