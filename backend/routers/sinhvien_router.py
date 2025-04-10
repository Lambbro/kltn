from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db 
import schemas.base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user, check_permission, check_higher_permission
from repositories.service_repositories import get_ma_khoa_by_email
from services.sinhvien.sv_nckhsv_dk_service import SVDangKyService
from services.giangvien.gv_nckhsv_nhom_service import GVNhomNCKHSVService

sv_router = APIRouter(prefix="/sv", tags=["Sinh Viên"])

# TẠO ĐĂNG KÝ + NGUYỆN VỌNG
@sv_router.post("/dangky/them", response_model=detai_sv_schemas.DangKyNguyenVongResponse)
async def create_dangky(
    dang_ky: schemas.DangKyNCKHCreate, 
    list_nguyen_vong: List[schemas.NguyenVongDKCreate], 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = SVDangKyService(db)
    return await dang_ky_service.add(dang_ky=dang_ky, list_nguyen_vong=list_nguyen_vong)