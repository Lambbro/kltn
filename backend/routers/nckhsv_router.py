from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db 
from services.nckhsv_dangky_service import DangKyService
import schemas.base_schemas as schemas
from schemas.detai_sv_schemas import DangKyNguyenVongResponse
from auths.auth import get_current_user

dtsv_router = APIRouter(prefix="/nckh_sv", tags=["Đề tài NCKH"])

# ========================== LẤY TẤT CẢ ĐĂNG KÝ (KÈM NGUYỆN VỌNG) ==========================
@dtsv_router.get("/dang_ky", response_model=List[DangKyNguyenVongResponse])
async def get_all_dangky(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = DangKyService(db, current_user)
    list_dang_ky = await service.get_all()
    return list_dang_ky

# ========================== LẤY CHI TIẾT ĐĂNG KÝ (KÈM NGUYỆN VỌNG) ==========================
@dtsv_router.get("/dangky/{ma_dk}", response_model=DangKyNguyenVongResponse)
async def get_dangky_by_id(
    ma_dk: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db=db, current_user=current_user)
    return await dang_ky_service.get_by_id(ma_dk=ma_dk)

# ========================== LẤY ĐĂNG KÝ ĐANG THỰC HIỆN THEO MÃ SINH VIÊN (KÈM NGUYỆN VỌNG) ==========================
@dtsv_router.get("/dangky_msv/{ma_sv}", response_model=DangKyNguyenVongResponse)
async def get_dangky_by_ma_sv(
    ma_sv: str, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db=db, current_user=current_user)
    return await dang_ky_service.get_by_ma_sv(ma_sv=ma_sv)

# ========================== TẠO ĐĂNG KÝ + NGUYỆN VỌNG ==========================
@dtsv_router.post("/dangky", response_model=DangKyNguyenVongResponse)
async def create_dangky(
    dang_ky: schemas.DangKyNCKHCreate, 
    list_nguyen_vong: List[schemas.NguyenVongDKCreate], 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db=db, current_user=current_user)
    return await dang_ky_service.create(dang_ky=dang_ky, list_nguyen_vong=list_nguyen_vong)

# ========================== CẬP NHẬT ĐĂNG KÝ + NGUYỆN VỌNG ==========================
@dtsv_router.put("/dangky/{ma_dk}", response_model=DangKyNguyenVongResponse)
async def update_dangky(
    ma_dk: int, 
    dang_ky: schemas.DangKyNCKHUpdate, 
    list_nguyen_vong: List[schemas.NguyenVongDKUpdate], 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db=db, current_user=current_user)
    return await dang_ky_service.update(ma_dk=ma_dk, dang_ky=dang_ky, list_nguyen_vong=list_nguyen_vong)

# ========================== XÓA ĐĂNG KÝ (KÈM NGUYỆN VỌNG) ==========================
@dtsv_router.delete("/dangky/{ma_dk}")
async def delete_dangky(
    ma_dk: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db=db, current_user=current_user)
    return await dang_ky_service.delete(ma_dk=ma_dk)
