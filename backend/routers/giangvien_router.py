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

gv_router = APIRouter(prefix="/gv", tags=["Giảng Viên"])

# ==========================
# 📌 ĐĂNG KÝ NHÓM
# ==========================
@gv_router.post("/nhomnckh", response_model=detai_sv_schemas.NhomNCKHSVResponse)
async def add_nhom(
    nhom: schemas.NhomNCKHCreate, 
    dssv: List[str],
    detai: schemas.DeTaiNCKHSVCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.add(nhom_data=nhom, dssv=dssv, detainckhsv_data=detai)


@gv_router.get("/nhomnckh", response_model=List[detai_sv_schemas.NhomNCKHSVResponse])
async def get_all_nhom(
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 3)
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
    check_higher_permission(current_user, 3)
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
    check_higher_permission(current_user, 3)
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
    check_higher_permission(current_user, 3)
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
    detainckhsv_data: schemas.DeTaiNCKHSVCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    quyen_han = current_user.get("quyen_han")
    service = DeTaiNCKHSVService(db)
    if quyen_han<3:
        return await service.add(ma_nhom=ma_nhom, detainckhsv_data=detainckhsv_data)
    elif quyen_han==3:
        email = current_user.get("email")
        mgv = await get_ma_gv_by_email(db, email)
        return await service.add(ma_nhom=ma_nhom, detainckhsv_data=detainckhsv_data, mgv=mgv)
    else:
        check_higher_permission(current_user, 3)
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
    check_higher_permission(current_user, 3)
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
    check_higher_permission(current_user, 3)
    email = current_user.get("email")
    mgv = await get_ma_gv_by_email(db, email)
    service = SYLLHuongNghienCuuService(db)
    return await service.delete(ma_gv=ma_gv, ma_hnc=ma_hnc, mgv=mgv)

@gv_router.get("/syll/hnc_by_gv/{ma_gv}", response_model=List[schemas.HuongNghienCuuResponse])
async def get_hnc_by_gv (
    ma_gv: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 4)
    service = SYLLHuongNghienCuuService(db)
    return await service.get_hnc_by_gv(ma_gv=ma_gv)

@gv_router.get("/syll/gv_by_hnc/{ma_hnc}", response_model=List[schemas.GiangVienResponse])
async def get_gv_by_hnc (
    ma_hnc: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_higher_permission(current_user, 4)
    service = SYLLHuongNghienCuuService(db)
    return await service.get_gv_by_hnc(ma_hnc=ma_hnc)