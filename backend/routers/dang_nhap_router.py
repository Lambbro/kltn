from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas import base_schemas as schemas
from services.dang_nhap_service import DangNhapService

dn_router = APIRouter(prefix="/dang-nhap", tags=["Đăng nhập"])

@dn_router.post("/", response_model=dict)
async def dang_nhap(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    service = DangNhapService(db)
    dang_nhap_data = schemas.TaiKhoanLogin(email=form_data.username, mat_khau=form_data.password)
    return await service.dang_nhap(dang_nhap_data)