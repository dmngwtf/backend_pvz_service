from uuid import uuid4
from datetime import datetime
from app.db.database import get_db
from app.core.custom_logging import setup_logging
from app.core.metrics import PRODUCTS_ADDED

logger = setup_logging()

class ProductService:
    def add_product(self, type: str, pvz_id: str, user_role: str):
        logger.info(f"Attempting to add product of type: {type} to PVZ: {pvz_id} by role: {user_role}")
        if user_role != "employee":
            logger.error("Unauthorized attempt to add product")
            raise ValueError("Only employees can add products")
        if type not in ["электроника", "одежда", "обувь"]:
            logger.error(f"Invalid product type: {type}")
            raise ValueError("Invalid product type")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                logger.error(f"PVZ not found: {pvz_id}")
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
                logger.error("No open reception found")
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
            PRODUCTS_ADDED.inc()
            logger.info(f"Product added: {product['id']}")
            return {
                "id": product["id"],
                "date_time": product["date_time"],
                "type": product["type"],
                "reception_id": product["reception_id"]
            }

    def delete_last_product(self, pvz_id: str, user_role: str):
        logger.info(f"Attempting to delete last product from PVZ: {pvz_id} by role: {user_role}")
        if user_role != "employee":
            logger.error("Unauthorized attempt to delete product")
            raise ValueError("Only employees can delete products")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                logger.error(f"PVZ not found: {pvz_id}")
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
                logger.error("No open reception found")
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
                logger.error("No products to delete")
                raise ValueError("No products to delete")

            cursor.execute(
                "DELETE FROM products WHERE id = %s",
                (product["id"],)
            )
            logger.info(f"Product deleted: {product['id']}")
            return {"message": "Product deleted"}