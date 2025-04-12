import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings

def get_db_connection():
    return psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=RealDictCursor
    )

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()