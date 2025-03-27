from repositories.repository import GiangVienRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import GiangVien, GiangVienCreate, GiangVienUpdate, TaiKhoanCreate
from typing import List, Optional
from fastapi import HTTPException
from services.tai_khoan_service import TaiKhoanService

class GiangVienService:
    def __init__(self, db: AsyncSession):
        self.repo = GiangVienRepository(db)

    async def get_all_giang_vien(self) -> List[GiangVien]:
        return await self.repo.get_all()
    
    async def get_giang_vien(self, ma_gv: str) -> Optional[GiangVien]:
        giang_vien = await self.repo.get(ma_gv)
        if not giang_vien:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy giảng viên với mã '{ma_gv}' không tồn tại.")
        return giang_vien
    
    async def create_giang_vien(self, giang_vien_data: GiangVienCreate, db: AsyncSession) -> GiangVien:
        email = giang_vien_data.email

        tai_khoan_data = TaiKhoanCreate(email=email, mat_khau="88888888", quyen_han=3)
        await TaiKhoanService.dang_ky(db, tai_khoan_data)

        return await self.repo.create(giang_vien_data)
    
    async def update_giang_vien(self, ma_gv: str, giang_vien_data: GiangVienUpdate) -> Optional[GiangVien]:
        giang_vien = await self.repo.update(ma_gv, giang_vien_data)
        if not giang_vien:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật giảng viên với mã '{ma_gv}', có thể mã này không tồn tại.")
        return giang_vien
    
    async def delete_giang_vien(self, ma_gv: str) -> bool:
        success = await self.repo.delete(ma_gv)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa giảng viên với mã '{ma_gv}', có thể mã này không tồn tại.")
        return {"success": True, "message": "Xóa sinh viên thành công."}