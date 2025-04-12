from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import DummyLogin, UserCreate, UserLogin, UserOut, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/dummyLogin", response_model=Token)
async def dummy_login(data: DummyLogin, service: AuthService = Depends()):
    try:
        return service.dummy_login(data.role)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/register", response_model=UserOut)
async def register(data: UserCreate, service: AuthService = Depends()):
    try:
        return service.register(data.email, data.password, data.role)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
async def login(data: UserLogin, service: AuthService = Depends()):
    try:
        return service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))