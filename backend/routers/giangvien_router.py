from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db 
import schemas.base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user, check_permission, check_higher_permission
from repositories.service_repositories import get_ma_khoa_by_email, get_ma_gv_by_email
from services.nckhsv_nhom_service import NhomNCKHSVService
from services.syllgv_hnc_service import SYLLHuongNghienCuuService
from services.nckhsv_detai_service import DeTaiNCKHSVService
from services.nckhsv_dk_service import DangKyService

gv_router = APIRouter(prefix="/gv", tags=["Giảng Viên"])

# ==========================
# 📌 ĐĂNG KÝ THAM GIA NCKH SV
# ==========================

@gv_router.get("/dk_sv")
async def get_dssv_by_dk(
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_gv = await get_ma_gv_by_email(db, email)
    service = DangKyService(db)
    return await service.get_dssv_by_dk(ma_gv)

# ==========================
# 📌 ĐĂNG KÝ NHÓM
# ==========================
@gv_router.post("/nhomnckh", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def add_nhom(
    dssv: List[str],
    detai: schemas.DeTaiNCKHSVCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_gv = get_ma_gv_by_email(email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.add(ma_gv=ma_gv, dssv=dssv, detainckhsv_data=detai)

@gv_router.get("/nhomnckh", response_model=List[detai_sv_schemas.NhomNCKHSVResponse])
async def get_all_nhom(
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.get_all(ma_khoa=ma_khoa)

@gv_router.get("/nhomnckh/{ma_nhom}", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def get_nhom_by_ma_nhom(
    ma_nhom: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.get_by_ma_nhom(ma_nhom=ma_nhom, ma_khoa=ma_khoa)

@gv_router.get("/nhomnckh/gv/{ma_gv}", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def get_nhom_by_ma_gv(
    ma_gv: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.get_by_ma_gv(ma_gv=ma_gv, ma_khoa=ma_khoa)

@gv_router.put("/nhomnckh/{ma_nhom}", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def update_nhom(
    ma_nhom: str, 
    nhom: schemas.NhomNCKHUpdate, 
    dssv: Optional[List[str]],
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.update(ma_nhom=ma_nhom, nhom_data=nhom, dssv=dssv, ma_khoa=ma_khoa)

# ==========================
# 📌 ĐỀ TÀI NCKH SV
# ==========================
@gv_router.post("/detaisv/add")
async def add_detai_cho_nhom(
    ma_nhom: int,
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    detainckhsv_data: schemas.DeTaiNCKHSVCreate = None,
):
    quyen_han = current_user.get("quyen_han")
    service = DeTaiNCKHSVService(db)
    email = current_user.get("email")
    if quyen_han<3:
        ma_khoa = await get_ma_khoa_by_email(db, email)
        return await service.add(ma_nhom=ma_nhom, detainckhsv_data=detainckhsv_data, ma_khoa=ma_khoa)
    elif quyen_han==3:
        mgv = await get_ma_gv_by_email(db, email)
        return await service.add(ma_nhom=ma_nhom, detainckhsv_data=detainckhsv_data, mgv=mgv)
    else:
        return None

# ==========================
# 📌 SYLL HƯỚNG NGHIÊN CỨU
# ==========================

@gv_router.post("/syll/hnc/add")
async def add_hnc(
    ma_gv: str,
    ma_hnc: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    mgv = await get_ma_gv_by_email(db, email)
    service = SYLLHuongNghienCuuService(db)
    return await service.add(ma_gv=ma_gv, ma_hnc=ma_hnc, mgv=mgv)

@gv_router.delete("/syll/hnc/delete")
async def delete_hnc_gv (
    ma_gv: str,
    ma_hnc: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    mgv = await get_ma_gv_by_email(db, email)
    service = SYLLHuongNghienCuuService(db)
    return await service.delete(ma_gv=ma_gv, ma_hnc=ma_hnc, mgv=mgv)