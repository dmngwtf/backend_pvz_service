import datetime

class pvz:
    def __init__(self, id: str,registration_date:datetime, city: str):
        self.id = id
        self.city = city
        self.registration_date = registration_date

    @staticmethod
    def create_table_sql():
        return """
        CREATE TABLE IF NOT EXISTS pvzs (
            id UUID PRIMARY KEY,
            registration_date TIMESTAMP NOT NULL,
            city VARCHAR(50) NOT NULL CHECK (city IN ('Москва', 'Санкт-Петербург', 'Казань'))
        );
        """
    