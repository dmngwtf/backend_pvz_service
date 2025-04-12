from uuid import uuid4
from datetime import datetime

class User:
    def __init__(self, id: str, email: str, password: str, role: str):
        self.id = id
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def create_table_sql():
        return """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL CHECK (role IN ('employee', 'moderator'))
        );
        """