import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from schemas import base_schemas as schemas
from repositories.sinhvien_repository import SinhVienRepository
from repositories.taikhoan_repository import TaiKhoanRepository
from repositories.base_repositories import KhoaRepository
from typing import List

class KhoaSinhVienService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sv_repo = SinhVienRepository(db)
        self.tk_repo = TaiKhoanRepository(db)
        self.khoa_repo = KhoaRepository(db)

    async def get(self, ma_sv: str, ma_khoa: str):
        try:
            sinh_vien = await self.sv_repo.khoa_get(ma_sv=ma_sv, ma_khoa=ma_khoa)
            if not sinh_vien:
                raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
            return schemas.SinhVienResponse.model_validate(sinh_vien)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi xem sinh viên")

    async def get_all(self, ma_khoa:str, skip: int = 0, limit: int = 100) -> List[schemas.SinhVienResponse]:
        try:
            danh_sach_sv = await self.sv_repo.khoa_get_all(ma_khoa=ma_khoa, skip=skip, limit=limit)
            if not danh_sach_sv:
                raise HTTPException(status_code=404, detail="Không có sinh viên nào trong danh sách")

            return [schemas.SinhVienResponse.model_validate(sv) for sv in danh_sach_sv]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xem danh sách sinh viên: {str(e)}")