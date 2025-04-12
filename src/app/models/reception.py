from uuid import uuid4
from datetime import datetime

class Reception:
    def __init__(self, id: str, date_time: datetime, pvz_id: str, status: str):
        self.id = id
        self.date_time = date_time
        self.pvz_id = pvz_id
        self.status = status

    @staticmethod
    def create_table_sql():
        return """
        CREATE TABLE IF NOT EXISTS receptions (
            id UUID PRIMARY KEY,
            date_time TIMESTAMP NOT NULL,
            pvz_id UUID NOT NULL,
            status VARCHAR(50) NOT NULL CHECK (status IN ('in_progress', 'close')),
            FOREIGN KEY (pvz_id) REFERENCES pvzs(id)
        );
        """