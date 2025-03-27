from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import base_schemas as schemas
from typing import List
from auths.auth import get_current_user
from services import (
    ql_khoa_service, ql_khenthuong_service, ql_hnc_service,
    ql_sv_service, ql_gv_service
)

router = APIRouter(
    prefix="/quan-ly",
    tags=["Quản Lý"]
)

# ==========================
# 📌 QUẢN LÝ KHOA
# ==========================

#Khoa
@router.get("/khoa", response_model=list[schemas.KhoaResponse])
async def xem_danh_sach_khoa(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db, current_user)
    return await service.get_all_khoa()

# Thêm khoa mới
@router.post("/khoa/them", response_model=schemas.KhoaResponse)
async def them_khoa(
    khoa: schemas.KhoaCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db, current_user)
    return await service.create_khoa(khoa)

# Cập nhật khoa
@router.put("/khoa/cap-nhat/{ma_khoa}", response_model=schemas.KhoaResponse)
async def cap_nhat_khoa(
    ma_khoa: str,
    khoa: schemas.KhoaUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db, current_user)
    return await service.update_khoa(ma_khoa, khoa)

# Xóa khoa
@router.delete("/khoa/xoa/{ma_khoa}", response_model=dict)
async def xoa_khoa(
    ma_khoa: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db, current_user)
    return await service.delete_khoa(ma_khoa)

# ==========================
# 📌 QUẢN LÝ KHOA
# ==========================
#Hướng nghiên cứu
@router.get("/hnc", response_model=list[schemas.HuongNghienCuuResponse])
async def get_all_huong_nghien_cuu(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db, current_user)
    return await service.get_all_huong_nghien_cuu()

@router.get("/hnc/{ma_hnc}", response_model=schemas.HuongNghienCuuResponse)
async def get_huong_nghien_cuu(
    ma_hnc: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
    ):
    service = ql_hnc_service.QLHuongNghienCuuService(db, current_user)
    return await service.get_huong_nghien_cuu(ma_hnc)

@router.post("/hnc/create", response_model=schemas.HuongNghienCuuResponse, status_code=201)
async def create_huong_nghien_cuu(
    hnc_data: schemas.HuongNghienCuuCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
    ):
    service = ql_hnc_service.QLHuongNghienCuuService(db, current_user)
    return await service.create_huong_nghien_cuu(hnc_data)

@router.put("/hnc/update/{ma_hnc}", response_model=schemas.HuongNghienCuuResponse)
async def update_huong_nghien_cuu(
    ma_hnc: int, 
    hnc_data: schemas.HuongNghienCuuUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db, current_user)
    return await service.update_huong_nghien_cuu(ma_hnc, hnc_data)

@router.delete("/hnc/delete/{ma_hnc}", response_model=dict)
async def delete_huong_nghien_cuu(
    ma_hnc: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db, current_user)
    return await service.delete_huong_nghien_cuu(ma_hnc)

# ==========================
# 📌 QUẢN LÝ SINH VIÊN
# ==========================

@router.get("/sinh-vien/{ma_sv}", response_model=schemas.SinhVienResponse)
async def xem_sinh_vien(
    ma_sv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.xem_sv(ma_sv)

@router.get("/sinh-vien", response_model=List[schemas.SinhVienResponse])
async def xem_danh_sach_sv(
    skip: int = 0,       # Mặc định bỏ qua 0 bản ghi
    limit: int = 100,    # Mặc định lấy 100 bản ghi mỗi lần
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.xem_danh_sach_sv(skip, limit)

# Đăng ký một sinh viên
@router.post("/sinh-vien/them", response_model=schemas.SinhVienResponse)
async def tao_sinh_vien(
    sinh_vien: schemas.SinhVienCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.tao_sinh_vien(sinh_vien)

# Xóa sinh viên theo mã
@router.delete("/sinh-vien/xoa/{ma_sv}", response_model=dict)
async def xoa_sinh_vien(
    ma_sv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.xoa_sinh_vien(ma_sv)

# Đăng ký danh sách sinh viên
@router.post("/sinh-vien/dang-ky", response_model=dict)
async def tao_danh_sach_sinh_vien(
    danh_sach_sinh_vien: list[schemas.SinhVienCreate], 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.tao_danh_sach_sinh_vien(danh_sach_sinh_vien)

# Cập nhật thông tin sinh viên
@router.put("/sinh-vien/cap-nhat/{ma_sv}", response_model=schemas.SinhVienResponse)
async def cap_nhat_sinh_vien(
    ma_sv: str,
    sinh_vien_update: schemas.SinhVienUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db, current_user)
    return await service.cap_nhat_sinh_vien(ma_sv, sinh_vien_update)

# ==========================
# 📌 QUẢN LÝ GIẢNG VIÊN
# ==========================

# Thêm giảng viên
@router.post("/giang-vien/them", response_model=schemas.GiangVienResponse)
async def tao_giang_vien(
    giang_vien: schemas.GiangVienCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db, current_user)
    return await service.tao_giang_vien(giang_vien)

# Xóa giảng viên
@router.delete("/giang-vien/xoa/{ma_gv}", response_model=dict)
async def xoa_giang_vien(
    ma_gv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db, current_user)
    return await service.xoa_giang_vien(ma_gv)

# Cập nhật giảng viên
@router.put("/giang-vien/cap-nhat/{ma_gv}", response_model=schemas.GiangVienResponse)
async def cap_nhat_giang_vien(
    ma_gv: str,
    giang_vien_update: schemas.GiangVienUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db, current_user)
    return await service.cap_nhat_giang_vien(ma_gv, giang_vien_update)

@router.get("/giang-vien/{ma_gv}", response_model=schemas.GiangVienResponse)
async def xem_giang_vien(
    ma_gv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db, current_user)
    return await service.xem_giang_vien(ma_gv)

@router.get("/giang-vien", response_model=list[schemas.GiangVienResponse])
async def lay_danh_sach_giang_vien(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db, current_user)
    return await service.lay_danh_sach_giang_vien()