from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PVZCreate(BaseModel):
    city: str

class PVZOut(BaseModel):
    id: UUID
    registration_date: datetime
    city: str