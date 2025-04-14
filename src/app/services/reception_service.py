from uuid import uuid4
from datetime import datetime
from app.db.database import get_db
from app.core.custom_logging import setup_logging
from app.core.metrics import RECEPTIONS_CREATED

logger = setup_logging()

class ReceptionService:
    def create_reception(self, pvz_id: str, user_role: str):
        logger.info(f"Attempting to create reception for PVZ: {pvz_id} by role: {user_role}")
        if user_role != "employee":
            logger.error("Unauthorized attempt to create reception")
            raise ValueError("Only employees can create receptions")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                logger.error(f"PVZ not found: {pvz_id}")
                raise ValueError("PVZ not found")

            # Проверяем, нет ли открытой приёмки
            cursor.execute(
                """
                SELECT id FROM receptions
                WHERE pvz_id = %s AND status = 'in_progress'
                """,
                (pvz_id,)
            )
            if cursor.fetchone():
                logger.error("An open reception already exists")
                raise ValueError("An open reception already exists")

            reception_id = str(uuid4())
            date_time = datetime.utcnow()

            cursor.execute(
                """
                INSERT INTO receptions (id, date_time, pvz_id, status)
                VALUES (%s, %s, %s, %s)
                RETURNING id, date_time, pvz_id, status
                """,
                (reception_id, date_time, pvz_id, "in_progress")
            )
            reception = cursor.fetchone()
            RECEPTIONS_CREATED.inc()
            logger.info(f"Reception created: {reception['id']}")
            return {
                "id": reception["id"],
                "date_time": reception["date_time"],
                "pvz_id": reception["pvz_id"],
                "status": reception["status"]
            }