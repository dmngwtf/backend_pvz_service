from uuid import uuid4
from datetime import datetime
from app.db.database import get_db

class ProductService:
    def add_product(self, type: str, pvz_id: str, user_role: str):
        if user_role != "employee":
            raise ValueError("Only employees can add products")
        if type not in ["электроника", "одежда", "обувь"]:
            raise ValueError("Invalid product type")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                raise ValueError("PVZ not found")

            # Находим открытую приёмку
            cursor.execute(
                """
                SELECT id FROM receptions
                WHERE pvz_id = %s AND status = 'in_progress'
                """,
                (pvz_id,)
            )
            reception = cursor.fetchone()
            if not reception:
                raise ValueError("No open reception found")

            product_id = str(uuid4())
            date_time = datetime.utcnow()

            cursor.execute(
                """
                INSERT INTO products (id, date_time, type, reception_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, date_time, type, reception_id
                """,
                (product_id, date_time, type, reception["id"])
            )
            product = cursor.fetchone()
            return {
                "id": product["id"],
                "date_time": product["date_time"],
                "type": product["type"],
                "reception_id": product["reception_id"]
            }

    def delete_last_product(self, pvz_id: str, user_role: str):
        if user_role != "employee":
            raise ValueError("Only employees can delete products")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                raise ValueError("PVZ not found")

            # Находим открытую приёмку
            cursor.execute(
                """
                SELECT id FROM receptions
                WHERE pvz_id = %s AND status = 'in_progress'
                """,
                (pvz_id,)
            )
            reception = cursor.fetchone()
            if not reception:
                raise ValueError("No open reception found")

            # Находим последний товар
            cursor.execute(
                """
                SELECT id FROM products
                WHERE reception_id = %s
                ORDER BY date_time DESC
                LIMIT 1
                """,
                (reception["id"],)
            )
            product = cursor.fetchone()
            if not product:
                raise ValueError("No products to delete")

            cursor.execute(
                "DELETE FROM products WHERE id = %s",
                (product["id"],)
            )
            return {"message": "Product deleted"}