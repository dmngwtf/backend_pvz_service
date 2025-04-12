from uuid import uuid4
from datetime import datetime
from app.db.database import get_db

class PVZService:
    def create_pvz(self, city: str, user_role: str):
        if user_role != "moderator":
            raise ValueError("Only moderators can create PVZ")
        if city not in ["Москва", "Санкт-Петербург", "Казань"]:
            raise ValueError("Invalid city")

        pvz_id = str(uuid4())
        registration_date = datetime.utcnow()

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pvzs (id, registration_date, city)
                VALUES (%s, %s, %s)
                RETURNING id, registration_date, city
                """,
                (pvz_id, registration_date, city)
            )
            pvz = cursor.fetchone()
            return {
                "id": pvz["id"],
                "registration_date": pvz["registration_date"],
                "city": pvz["city"]
            }

    def get_pvz_list(self, start_date: datetime | None, end_date: datetime | None, page: int, limit: int):
        offset = (page - 1) * limit
        query = """
            SELECT p.id, p.registration_date, p.city,
                   r.id as reception_id, r.date_time, r.pvz_id, r.status,
                   pr.id as product_id, pr.date_time as product_date_time, pr.type, pr.reception_id
            FROM pvzs p
            LEFT JOIN receptions r ON p.id = r.pvz_id
            LEFT JOIN products pr ON r.id = pr.reception_id
        """
        params = []
        conditions = []

        if start_date:
            conditions.append("r.date_time >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("r.date_time <= %s")
            params.append(end_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY p.id, r.date_time, pr.date_time"
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            pvz_map = {}
            for row in rows:
                pvz_id = row["id"]
                if pvz_id not in pvz_map:
                    pvz_map[pvz_id] = {
                        "pvz": {
                            "id": row["id"],
                            "registration_date": row["registration_date"],
                            "city": row["city"]
                        },
                        "receptions": {}
                    }
                
                if row["reception_id"]:
                    reception_id = row["reception_id"]
                    if reception_id not in pvz_map[pvz_id]["receptions"]:
                        pvz_map[pvz_id]["receptions"][reception_id] = {
                            "reception": {
                                "id": row["reception_id"],
                                "date_time": row["date_time"],
                                "pvz_id": row["pvz_id"],
                                "status": row["status"]
                            },
                            "products": []
                        }
                    
                    if row["product_id"]:
                        pvz_map[pvz_id]["receptions"][reception_id]["products"].append({
                            "id": row["product_id"],
                            "date_time": row["product_date_time"],
                            "type": row["type"],
                            "reception_id": row["reception_id"]
                        })

            result = [
                {
                    "pvz": pvz["pvz"],
                    "receptions": list(pvz["receptions"].values())
                }
                for pvz in pvz_map.values()
            ]
            return result
        

    def close_last_reception(self, pvz_id: str, user_role: str):
        if user_role != "employee":
            raise ValueError("Only employees can close receptions")

        with get_db() as conn:
            cursor = conn.cursor()
            # Проверяем существование ПВЗ
            cursor.execute("SELECT id FROM pvzs WHERE id = %s", (pvz_id,))
            if not cursor.fetchone():
                raise ValueError("PVZ not found")

            # Находим открытую приёмку
            cursor.execute(
                """
                SELECT id, date_time, pvz_id, status
                FROM receptions
                WHERE pvz_id = %s AND status = 'in_progress'
                """,
                (pvz_id,)
            )
            reception = cursor.fetchone()
            if not reception:
                raise ValueError("No open reception found")

            cursor.execute(
                """
                UPDATE receptions
                SET status = 'close'
                WHERE id = %s
                RETURNING id, date_time, pvz_id, status
                """,
                (reception["id"],)
            )
            updated_reception = cursor.fetchone()
            return {
                "id": updated_reception["id"],
                "date_time": updated_reception["date_time"],
                "pvz_id": updated_reception["pvz_id"],
                "status": updated_reception["status"]
            }