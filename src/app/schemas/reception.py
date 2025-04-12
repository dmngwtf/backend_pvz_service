from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ReceptionCreate(BaseModel):
    pvz_id: UUID

class ReceptionOut(BaseModel):
    id: UUID
    date_time: datetime
    pvz_id: UUID
    status: str