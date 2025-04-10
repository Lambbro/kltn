from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db 
import schemas.base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user, check_permission, check_higher_permission
from repositories.service_repositories import get_ma_khoa_by_email
from services.giangvien.gv_nckhsv_nhom_service import GVNhomNCKHSVService

gv_router = APIRouter(prefix="/gv", tags=["Giảng Viên"])

# ==========================
# 📌 ĐĂNG KÝ NHÓM
# ==========================
@gv_router.post("/nhomnckh", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def add_nhom(
    nhom: schemas.NhomNCKHCreate, 
    dssv: List[str], 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
    nhom_service = GVNhomNCKHSVService(db)
    return await nhom_service.add(nhom_data=nhom, dssv=dssv)

@gv_router.get("/nhomnckh", response_model=List[detai_sv_schemas.NhomNCKHSVResponse])
async def get_all_nhom(
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = GVNhomNCKHSVService(db)
    return await nhom_service.get_all(ma_khoa=ma_khoa)

@gv_router.get("/nhomnckh/{ma_nhom}", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def get_nhom_by_ma_nhom(
    ma_nhom: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = GVNhomNCKHSVService(db)
    return await nhom_service.get_by_ma_nhom(ma_nhom=ma_nhom, ma_khoa=ma_khoa)

@gv_router.put("/nhomnckh/{ma_nhom}", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def update_nhom(
    ma_nhom: str, 
    nhom: schemas.NhomNCKHCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = GVNhomNCKHSVService(db)
    return await nhom_service.update(ma_nhom=ma_nhom, nhom_data=nhom, ma_khoa=ma_khoa)

# ==========================
# 📌 ĐĂNG KÝ NHÓM
# ==========================