from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProductCreate(BaseModel):
    type: str
    pvz_id: UUID

class ProductOut(BaseModel):
    id: UUID
    date_time: datetime
    type: str
    reception_id: UUID