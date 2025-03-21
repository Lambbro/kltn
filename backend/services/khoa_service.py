from repositories.repository import KhoaRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import Khoa, KhoaCreate, KhoaUpdate
from typing import List
from fastapi import HTTPException

class KhoaService:
    def __init__(self, db: AsyncSession):
        self.repo = KhoaRepository(db)

    async def get_all_khoa(self) -> List[Khoa]:
        return await self.repo.get_all()
    
    async def get_khoa(self, ma_khoa: str) -> Khoa:
        khoa = await self.repo.get(ma_khoa)
        if khoa is None:
            raise HTTPException(status_code=404, detail=f"Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa
    
    async def create_khoa(self, khoa_data: KhoaCreate) -> Khoa:
        return await self.repo.create(khoa_data)
    
    async def update_khoa(self, ma_khoa: str, khoa_data: KhoaUpdate) -> Khoa:
        khoa = await self.repo.update(ma_khoa, khoa_data)
        if khoa is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa
    
    async def delete_khoa(self, ma_khoa: str) -> bool:
        success = await self.repo.delete(ma_khoa)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa. Khoa với mã '{ma_khoa}' không tồn tại.")
        return {"success": True, "message": "Xóa sinh viên thành công."}
