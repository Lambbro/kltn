import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import re

from schemas.base_schemas import GiangVienResponse
from repositories.taikhoan_repository import TaiKhoanRepository
from repositories.giangvien_repository import GiangVienRepository

class KhoaGiangVienService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tk_repo = TaiKhoanRepository(db)
        self.gv_repo = GiangVienRepository(db)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10

    #Xem thông tin giảng viên
    async def get(self, ma_gv: str, ma_khoa: str):
        try:
            giang_vien = await self.gv_repo.khoa_get(ma_gv, ma_khoa)
            if not giang_vien:
                raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")

            return GiangVienResponse.model_validate(giang_vien)

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy thông tin giảng viên")
        
    #Xem danh sách giảng viên
    async def get_all(self, ma_khoa: str):
        try:
            danh_sach_giang_vien = await self.gv_repo.khoa_get_all(ma_khoa)
            return [GiangVienResponse.model_validate(gv) for gv in danh_sach_giang_vien]

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy danh sách giảng viên")
