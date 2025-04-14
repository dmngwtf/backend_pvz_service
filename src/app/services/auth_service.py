from uuid import uuid4
import bcrypt
from app.core.security import create_token
from app.db.database import get_db
from app.core.custom_logging import setup_logging

logger = setup_logging()

class AuthService:
    def dummy_login(self, role: str):
        logger.info(f"Dummy login attempt with role: {role}")
        if role not in ["employee", "moderator"]:
            logger.error(f"Invalid role provided: {role}")
            raise ValueError("Invalid role. Must be 'employee' or 'moderator'")
        token = create_token({"role": role})
        return {"access_token": token, "token_type": "bearer"}

    def register(self, email: str, password: str, role: str):
        if role not in ["employee", "moderator"]:
            logger.error(f"Invalid role provided: {role}")
            raise ValueError("Invalid role. Must be 'employee' or 'moderator'")
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user_id = str(uuid4())
        
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO users (id, email, password, role)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, email, role
                    """,
                    (user_id, email, hashed_password, role)
                )
                user = cursor.fetchone()
                return {"id": user["id"], "email": user["email"], "role": user["role"]}
            except conn.Error as e:
                if "unique constraint" in str(e).lower():
                    logger.error(f"Email already exists: {email}")
                    raise ValueError("Email already exists")
                raise

    def login(self, email: str, password: str):
        logger.info(f"Login attempt for email: {email}")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, email, password, role
                FROM users
                WHERE email = %s
                """,
                (email,)
            )
            user = cursor.fetchone()
            if not user:
                logger.error(f"User not found: {email}")
                raise ValueError("Invalid credentials")
            
            if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                logger.error(f"Invalid password for user: {email}")
                raise ValueError("Invalid credentials")
            
            token = create_token({"role": user["role"], "user_id": str(user["id"])})
            return {"access_token": token, "token_type": "bearer"}