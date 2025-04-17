from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from database import get_db 
import schemas.base_schemas as schemas
import schemas.detai_sv_schemas as detai_sv_schemas
from auths.auth import get_current_user, check_permission, check_higher_permission
from repositories.service_repositories import get_ma_khoa_by_email
from services.nckhsv_dk_service import DangKyService
from services.nckhsv_tailieu_service import TaiLieuNCKHSVService
from services.ql_hnc_service import QLHuongNghienCuuService

sv_router = APIRouter(prefix="/sv", tags=["Sinh Viên"])

# TẠO ĐĂNG KÝ + NGUYỆN VỌNG
@sv_router.post("/dangky/them", response_model=detai_sv_schemas.DangKyNCKHSVResponse)
async def add_dk(
    dang_ky: schemas.DangKyNCKHCreate, 
    list_nguyen_vong: Optional[List[schemas.NguyenVongDKCreate]], 
    list_hnc: List[int],
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    dang_ky_service = DangKyService(db)
    return await dang_ky_service.add(
        dang_ky=dang_ky, 
        list_nguyen_vong=list_nguyen_vong,
        list_hnc=list_hnc
    )

# NỘP TÀI LIỆU CỦA NCKHSV
@sv_router.post("/upload/{ma_de_tai}/{loai_tai_lieu}")
async def nop_tai_lieu(
    ma_de_tai: int,
    loai_tai_lieu: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = TaiLieuNCKHSVService(db)

    result = await service.add(
        ma_de_tai=ma_de_tai,
        loai_tai_lieu=loai_tai_lieu,
        file=file
    )

    return result

@sv_router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Xử lý tệp tải lên
        contents = await file.read()
        # Ví dụ: In ra tên file
        return {"filename": file.filename}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})