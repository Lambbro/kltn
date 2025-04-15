from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db 
import schemas.base_schemas as schemas
from schemas.detai_sv_schemas import HNCvaGV
from auths.auth import get_current_user, check_permission, check_higher_permission
from repositories.service_repositories import get_ma_khoa_by_email, get_ma_gv_by_email, get_ma_khoa_by_sv_email
from services.ql_hnc_service import QLHuongNghienCuuService
from services.syllgv_hnc_service import SYLLHuongNghienCuuService

get_data_router = APIRouter(prefix="/get_data", tags=["Data"])
# HƯỚNG NGHIÊN CỨU
@get_data_router.get("/hnc", response_model=list[schemas.HuongNghienCuuResponse])
async def get_all_huong_nghien_cuu_by_sv(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email")
    quyen_han = current_user.get("quyen_han")
    service = QLHuongNghienCuuService(db)
    if quyen_han == 4:
        ma_khoa = await get_ma_khoa_by_sv_email(db, email)
        result = await service.get_all(ma_khoa)
    else:
        result = await service.get_all()
    return result

@get_data_router.get("/hnc/{ma_hnc}", response_model=schemas.HuongNghienCuuResponse)
async def get_huong_nghien_cuu(
    ma_hnc: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = QLHuongNghienCuuService(db)
    return await service.get(ma_hnc)

#HNC và Giảng Viên
@get_data_router.get("/hnc_by_gv/{ma_gv}", response_model=List[schemas.HuongNghienCuuResponse])
async def get_hnc_by_gv (
    ma_gv: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = SYLLHuongNghienCuuService(db)
    return await service.get_hnc_by_gv(ma_gv=ma_gv)

@get_data_router.get("/gv_by_hnc/{ma_hnc}", response_model=List[schemas.GiangVienResponse])
async def get_gv_by_hnc (
    ma_hnc: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = SYLLHuongNghienCuuService(db)
    return await service.get_gv_by_hnc(ma_hnc=ma_hnc)