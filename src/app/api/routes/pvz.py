from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from datetime import datetime
from app.schemas.pvz import PVZCreate, PVZOut
from app.schemas.reception import ReceptionOut
from app.services.pvz_service import PVZService
from app.services.product_service import ProductService
from app.api.dependencies import require_role

router = APIRouter(prefix="/pvz", tags=["pvz"])

@router.post("", response_model=PVZOut, status_code=status.HTTP_201_CREATED)
async def create_pvz(
    data: PVZCreate,
    service: PVZService = Depends(),
    user: dict = Depends(require_role("moderator"))
):
    try:
        return service.create_pvz(data.city, user["role"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("")
async def get_pvz_list(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=30),
    service: PVZService = Depends(),
    user: dict = Depends(require_role("employee"))
):
    return service.get_pvz_list(start_date, end_date, page, limit)

@router.post("/{pvzId}/close_last_reception", response_model=ReceptionOut)
async def close_last_reception(
    pvzId: str = Path(...),
    service: PVZService = Depends(),
    user: dict = Depends(require_role("employee"))
):
    try:
        return service.close_last_reception(pvzId, user["role"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{pvzId}/delete_last_product")
async def delete_last_product(
    pvzId: str = Path(...),
    service: ProductService = Depends(),
    user: dict = Depends(require_role("employee"))
):
    try:
        return service.delete_last_product(pvzId, user["role"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))