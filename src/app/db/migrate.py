import os
import glob
import sys
import psycopg2
from app.core.config import settings

def apply_migrations():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cursor = conn.cursor()
    migration_files = sorted(glob.glob("src/app/db/migrations/*.sql"))

    for file in migration_files:
        with open(file, "r") as f:
            sql = f.read()
        cursor.execute(sql)
        print(f"Applied migration: {file}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    apply_migrations()