from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

from typing import List
from schemas import base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user, check_permission, check_higher_permission
from services import (
    ql_khoa_service, ql_hnc_service,
    ql_sv_service, ql_gv_service,
    nckhsv_dk_service
)

ql_router = APIRouter(
    prefix="/phongkhdn",
    tags=["Phòng KH&ĐN"]
)

# ==========================
# 📌 QUẢN LÝ KHOA
# ==========================

#Khoa
@ql_router.get("/khoa", response_model=list[schemas.KhoaResponse])
async def get_all_khoa(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db)
    return await service.get_all()

@ql_router.get("/khoa/{ma_khoa}", response_model=schemas.KhoaResponse)
async def xem_khoa(
    ma_khoa: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db)
    return await service.get(ma_khoa)

# Thêm khoa mới
@ql_router.post("/khoa/add", response_model=schemas.KhoaResponse)
async def them_khoa(
    khoa: schemas.KhoaCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db)
    return await service.add(khoa)

# Cập nhật khoa
@ql_router.put("/khoa/update/{ma_khoa}", response_model=schemas.KhoaResponse)
async def cap_nhat_khoa(
    ma_khoa: str,
    khoa: schemas.KhoaUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db)
    return await service.update(ma_khoa, khoa)

# Xóa khoa
@ql_router.delete("/khoa/delete/{ma_khoa}", response_model=dict)
async def xoa_khoa(
    ma_khoa: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_khoa_service.QLKhoaService(db)
    return await service.delete(ma_khoa)

# ==========================
# 📌 QUẢN LÝ HƯỚNG NGHIÊN CỨU
# ==========================
#Hướng nghiên cứu
@ql_router.get("/hnc", response_model=list[schemas.HuongNghienCuuResponse])
async def get_all_huong_nghien_cuu(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db)
    return await service.get_all()

@ql_router.post("/hnc/add", response_model=schemas.HuongNghienCuuResponse, status_code=201)
async def create_huong_nghien_cuu(
    hnc_data: schemas.HuongNghienCuuCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db)
    return await service.add(hnc_data)

@ql_router.put("/hnc/update/{ma_hnc}", response_model=schemas.HuongNghienCuuResponse)
async def update_huong_nghien_cuu(
    ma_hnc: int, 
    hnc_data: schemas.HuongNghienCuuUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db)
    return await service.update(ma_hnc, hnc_data)

@ql_router.delete("/hnc/delete/{ma_hnc}", response_model=dict)
async def delete_huong_nghien_cuu(
    ma_hnc: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ql_hnc_service.QLHuongNghienCuuService(db)
    return await service.delete(ma_hnc)

# ==========================
# 📌 QUẢN LÝ SINH VIÊN
# ==========================

@ql_router.get("/sv/{ma_sv}", response_model=schemas.SinhVienResponse)
async def xem_sinh_vien(
    ma_sv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db)
    return await service.get(ma_sv)

@ql_router.get("/sv", response_model=List[schemas.SinhVienResponse])
async def xem_danh_sach_sv(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
): 
    service = ql_sv_service.QLSinhVienService(db)
    return await service.get_all()

# Đăng ký một sinh viên
@ql_router.post("/sv/add", response_model=schemas.SinhVienResponse)
async def tao_sinh_vien(
    sinh_vien: schemas.SinhVienCreateReal, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db)
    return await service.add(sinh_vien)

# Xóa sinh viên theo mã
@ql_router.delete("/sv/delete/{ma_sv}", response_model=dict)
async def xoa_sinh_vien(
    ma_sv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db)
    return await service.delete(ma_sv)

# Đăng ký danh sách sinh viên
@ql_router.post("/sv/add_list", response_model=dict)
async def tao_danh_sach_sinh_vien(
    danh_sach_sinh_vien: list[schemas.SinhVienCreateReal], 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db)
    return await service.add_all(danh_sach_sinh_vien)

# Cập nhật thông tin sinh viên
@ql_router.put("/sv/update/{ma_sv}", response_model=schemas.SinhVienResponse)
async def cap_nhat_sinh_vien(
    ma_sv: str,
    sinh_vien_update: schemas.SinhVienUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_sv_service.QLSinhVienService(db)
    return await service.update(ma_sv, sinh_vien_update)

# ==========================
# 📌 QUẢN LÝ GIẢNG VIÊN
# ==========================

# Thêm giảng viên
@ql_router.post("/gv/add", response_model=schemas.GiangVienResponse)
async def tao_giang_vien(
    giang_vien: schemas.GiangVienCreate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db)
    return await service.add(giang_vien)

# Xóa giảng viên
@ql_router.delete("/gv/delete/{ma_gv}", response_model=dict)
async def xoa_giang_vien(
    ma_gv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db)
    return await service.delete(ma_gv)

# Cập nhật giảng viên
@ql_router.put("/gv/update/{ma_gv}", response_model=schemas.GiangVienResponse)
async def cap_nhat_giang_vien(
    ma_gv: str,
    giang_vien_update: schemas.GiangVienUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db)
    return await service.update(ma_gv, giang_vien_update)

@ql_router.get("/gv/{ma_gv}", response_model=schemas.GiangVienResponse)
async def xem_giang_vien(
    ma_gv: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db)
    return await service.get(ma_gv)

@ql_router.get("/gv", response_model=list[schemas.GiangVienResponse])
async def lay_danh_sach_giang_vien(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ql_gv_service.QLGiangVienService(db)
    return await service.get_all()

# ==========================
# 📌 QUẢN LÝ NCKH SV
# ==========================
# LẤY TẤT CẢ ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
@ql_router.get("/nckhsv/dk", response_model=List[detai_sv_schemas.DangKyNCKHSVResponse])
async def get_all_dangky(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = nckhsv_dk_service.DangKyService(db)
    list_dang_ky = await service.get_all()
    return list_dang_ky

# LẤY CHI TIẾT ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
@ql_router.get("/nckhsv/dk/mdk/{ma_dk}", response_model=detai_sv_schemas.DangKyNCKHSVResponse)
async def get_dangky_by_id(
    ma_dk: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    service = nckhsv_dk_service.DangKyService(db)
    return await service.get(ma_dk=ma_dk)

# LẤY ĐĂNG KÝ ĐANG THỰC HIỆN THEO MÃ SINH VIÊN (KÈM NGUYỆN VỌNG)
@ql_router.get("/nckhsv/dk/msv/{ma_sv}", response_model=detai_sv_schemas.DangKyNCKHSVResponse)
async def get_dangky_by_ma_sv(
    ma_sv: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    service = nckhsv_dk_service.DangKyService(db)
    return await service.get(ma_sv=ma_sv)