from uuid import uuid4
from datetime import datetime

class Product:
    def __init__(self, id: str, date_time: datetime, type: str, reception_id: str):
        self.id = id
        self.date_time = date_time
        self.type = type
        self.reception_id = reception_id

    @staticmethod
    def create_table_sql():
        return """
        CREATE TABLE IF NOT EXISTS products (
            id UUID PRIMARY KEY,
            date_time TIMESTAMP NOT NULL,
            type VARCHAR(50) NOT NULL CHECK (type IN ('электроника', 'одежда', 'обувь')),
            reception_id UUID NOT NULL,
            FOREIGN KEY (reception_id) REFERENCES receptions(id)
        );
        """