from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import base_schemas as schemas
from services.dang_ky_service import DangKyService
from dependencies import verify_permission

router = APIRouter(
    prefix="/dang-ky",
    tags=["Đăng ký"]
)

@router.post("/sinh-vien", response_model=schemas.SinhVienResponse)
async def tao_sinh_vien(
    sinh_vien: schemas.SinhVienCreate, 
    user=Depends(lambda db=Depends(get_db): verify_permission(db=db, required_permission=1)),  # Chỉ admin
    db: AsyncSession = Depends(get_db)
):
    service = DangKyService(db)
    return await service.tao_sinh_vien(sinh_vien)

@router.post("/giang-vien", response_model=schemas.GiangVienResponse)
async def tao_giang_vien(
    giang_vien: schemas.GiangVienCreate, 
    user=Depends(lambda db=Depends(get_db): verify_permission(db=db, required_permission=1)),  # Chỉ admin
    db: AsyncSession = Depends(get_db)
):
    """
    Tạo một giảng viên mới và tài khoản tương ứng.
    """
    service = DangKyService(db)
    return await service.tao_giang_vien(giang_vien)

@router.post("/sinh-vien/danh-sach", response_model=list[schemas.SinhVienResponse])
async def tao_danh_sach_sinh_vien(
    danh_sach_sinh_vien: list[schemas.SinhVienCreate], 
    user=Depends(lambda db=Depends(get_db): verify_permission(db=db, required_permission=1)),  # Chỉ admin
    db: AsyncSession = Depends(get_db)
):
    """
    Tạo danh sách sinh viên và tài khoản tương ứng.
    """
    service = DangKyService(db)
    return await service.tao_danh_sach_sinh_vien(danh_sach_sinh_vien)
