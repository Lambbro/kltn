from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import base_schemas as schemas
from services.dang_nhap_service import DangNhapService

router = APIRouter(prefix="/dang-nhap", tags=["Đăng nhập"])

@router.post("/", response_model=schemas.TaiKhoanResponse)
async def dang_nhap(dang_nhap_data: schemas.TaiKhoanLogin, db: AsyncSession = Depends(get_db)):
    service = DangNhapService(db)
    return await service.dang_nhap(dang_nhap_data)