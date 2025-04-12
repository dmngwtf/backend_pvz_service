from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.core.security import create_token

client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products; DELETE FROM receptions; DELETE FROM pvzs;")

def test_integration_scenario():
    setup_database()
    # Шаг 1: Создаём ПВЗ
    token_moderator = create_token({"role": "moderator"})
    pvz_response = client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token_moderator}"}
    )
    assert pvz_response.status_code == 201
    pvz_id = pvz_response.json()["id"]

    # Шаг 2: Создаём приёмку
    token_employee = create_token({"role": "employee"})
    reception_response = client.post(
        "/receptions",
        json={"pvz_id": pvz_id},
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert reception_response.status_code == 201

    # Шаг 3: Добавляем 50 товаров
    for i in range(50):
        response = client.post(
            "/products",
            json={"type": "электроника", "pvz_id": pvz_id},
            headers={"Authorization": f"Bearer {token_employee}"}
        )
        assert response.status_code == 201

    # Шаг 4: Закрываем приёмку
    close_response = client.post(
        f"/pvz/{pvz_id}/close_last_reception",
        headers={"Authorization": f"Bearer {token_employee}"}
    )
    assert close_response.status_code == 200
    assert close_response.json()["status"] == "close"

    # Проверяем, что товары добавлены
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM products WHERE reception_id = %s",
            (reception_response.json()["id"],)
        )
        count = cursor.fetchone()["count"]
        assert count == 50