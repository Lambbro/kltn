from repositories.repository import SinhVienRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import SinhVien, SinhVienCreate, SinhVienUpdate, TaiKhoanCreate
from typing import List
from fastapi import HTTPException
from services.tai_khoan_service import TaiKhoanService

class SinhVienService:
    def __init__(self, db: AsyncSession):
        self.repo = SinhVienRepository(db)

    async def get_all_sinh_vien(self) -> List[SinhVien]:
        return await self.repo.get_all()

    async def get_sinh_vien(self, ma_sv: str) -> SinhVien:
        sinh_vien = await self.repo.get(ma_sv)
        if sinh_vien is None:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy sinh viên với mã '{ma_sv}'.")
        return sinh_vien

    async def create_sinh_vien(self, sinh_vien_data: SinhVienCreate, db: AsyncSession) -> SinhVien:
        email = sinh_vien_data.email

        tai_khoan_data = TaiKhoanCreate(email=email, mat_khau="88888888", quyen_han=4)
        await TaiKhoanService.dang_ky(db, tai_khoan_data)
        
        return await self.repo.create(sinh_vien_data)

    async def update_sinh_vien(self, ma_sv: str, sinh_vien_data: SinhVienUpdate) -> SinhVien:
        sinh_vien = await self.repo.update(ma_sv, sinh_vien_data)
        if sinh_vien is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật, sinh viên với mã '{ma_sv}' không tồn tại.")
        return sinh_vien

    async def delete_sinh_vien(self, ma_sv: str) -> dict:
        success = await self.repo.delete(ma_sv)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa, sinh viên với mã '{ma_sv}' không tồn tại.")
        return {"success": True, "message": "Xóa sinh viên thành công."}
