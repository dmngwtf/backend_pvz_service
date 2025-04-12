from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import ProductService
from app.api.dependencies import require_role

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def add_product(
    data: ProductCreate,
    service: ProductService = Depends(),
    user: dict = Depends(require_role("employee"))
):
    try:
        return service.add_product(data.type, str(data.pvz_id), user["role"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))