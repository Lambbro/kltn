from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import base_schemas as schemas

from auths.auth import get_current_user
from services import (
    ql_dang_ky_service, ql_khoa_service, ql_khenthuong_service, ql_hnc_service
)

router = APIRouter(
    prefix="/quan-ly",
    tags=["Quản Lý"]
)
#Khoa
@router.post("/khoa/danh-sach", response_model=list[schemas.KhoaResponse])
async def xem_danh_sach_khoa(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db, current_user)
    return await service.get_all_khoa()

#Đăng ký sinh viên, giảng viên và thêm tài khoản
@router.post("/sinh-vien/them-sv", response_model=schemas.SinhVienResponse)
async def tao_sinh_vien(
    sinh_vien: schemas.SinhVienCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_dang_ky_service.QLDangKyService(db)
    return await service.tao_sinh_vien(sinh_vien)

@router.post("/sinh-vien/dang-ky-danh-sach", response_model=list[schemas.SinhVienResponse])
async def tao_danh_sach_sinh_vien(
    danh_sach_sinh_vien: list[schemas.SinhVienCreate], 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_dang_ky_service.QLDangKyService(db)
    return await service.tao_danh_sach_sinh_vien(danh_sach_sinh_vien)

#Giảng Viên
@router.post("/giang-vien/them-gv", response_model=schemas.GiangVienResponse)
async def tao_giang_vien(
    giang_vien: schemas.GiangVienCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_dang_ky_service.QLDangKyService(db)
    return await service.tao_giang_vien(giang_vien)