from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.reception import ReceptionCreate, ReceptionOut
from app.services.reception_service import ReceptionService
from app.api.dependencies import require_role

router = APIRouter(prefix="/receptions", tags=["receptions"])

@router.post("", response_model=ReceptionOut, status_code=status.HTTP_201_CREATED)
async def create_reception(
    data: ReceptionCreate,
    service: ReceptionService = Depends(),
    user: dict = Depends(require_role("employee"))
):
    try:
        return service.create_reception(str(data.pvz_id), user["role"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))