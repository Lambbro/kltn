from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from typing import List

from schemas import base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user

from services.ql_sv_service import QLSinhVienService
from services.ql_gv_service import QLGiangVienService
from services.nckhsv_dk_service import DangKyService

from services.nckhsv_nhom_service import NhomNCKHSVService

from repositories.service_repositories import get_ma_khoa_by_email

qlk_router = APIRouter(
    prefix="/tonckh",
    tags=["Tổ NCKH"]
)

# ==========================
# 📌 QUẢN LÝ SINH VIÊN
# ==========================

@qlk_router.get("/sinh-vien/{ma_sv}", response_model=schemas.SinhVienResponse)
async def xem_sinh_vien(
    ma_sv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db=db, email=email)
    service = QLSinhVienService(db)
    return await service.get(ma_sv=ma_sv, ma_khoa=ma_khoa)

@qlk_router.get("/sinh-vien", response_model=List[schemas.SinhVienResponse])
async def xem_danh_sach_sv(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    service = QLSinhVienService(db)
    return await service.get_all(ma_khoa)

# ==========================
# 📌 QUẢN LÝ GIẢNG VIÊN
# ==========================

@qlk_router.get("/giang-vien/{ma_gv}", response_model=schemas.GiangVienResponse)
async def xem_giang_vien(
    ma_gv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    service = QLGiangVienService(db)
    return await service.get(ma_gv, ma_khoa)

@qlk_router.get("/giang-vien", response_model=list[schemas.GiangVienResponse])
async def lay_danh_sach_giang_vien(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    service = QLGiangVienService(db)
    return await service.get_all(ma_khoa)

# ==========================
# 📌 QUẢN LÝ ĐĂNG KÝ NCKH SV
# ==========================
# LẤY TẤT CẢ ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
@qlk_router.get("/dang_ky/danh_sach", response_model=List[detai_sv_schemas.DangKyNCKHSVResponse])
async def get_all_dangky(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    service = DangKyService(db)
    list_dang_ky = await service.get_all(ma_khoa=ma_khoa)
    return list_dang_ky

# LẤY CHI TIẾT ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
@qlk_router.get("/dangky/{ma_dk}", response_model=detai_sv_schemas.DangKyNCKHSVResponse)
async def get_dangky_by_id(
    ma_dk: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    dang_ky_service = DangKyService(db)
    return await dang_ky_service.get(ma_dk=ma_dk, ma_khoa=ma_khoa)

# LẤY ĐĂNG KÝ ĐANG THỰC HIỆN THEO MÃ SINH VIÊN (KÈM NGUYỆN VỌNG)
@qlk_router.get("/dangky_msv/{ma_sv}", response_model=detai_sv_schemas.DangKyNCKHSVResponse)
async def get_dangky_by_ma_sv(
    ma_sv: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    dang_ky_service = DangKyService(db)
    return await dang_ky_service.get(ma_sv=ma_sv, ma_khoa=ma_khoa)

# ==========================
# 📌 QUẢN LÝ NHÓM NCKH SV
# ==========================
@qlk_router.delete("/nhomnckh/{ma_nhom}", response_model=dict)
async def delete_nhom(
    ma_nhom: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    ma_khoa = await get_ma_khoa_by_email(db, email)
    nhom_service = NhomNCKHSVService(db)
    return await nhom_service.delete(ma_nhom=ma_nhom, ma_khoa=ma_khoa)