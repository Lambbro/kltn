from repositories.repository import KhoaRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import Khoa, KhoaCreate, KhoaUpdate
from typing import List

class KhoaService:
    def __init__(self, db: AsyncSession):
        self.repo = KhoaRepository(db)

    async def get_all_khoa(self) -> List[Khoa]:
        return await self.repo.get_all()
    
    async def get_khoa(self, ma_khoa: str) -> Khoa:
        khoa = await self.repo.get(ma_khoa)
        if not khoa:
            raise ValueError(f"Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa
    
    async def create_khoa(self, khoa_data: KhoaCreate) -> Khoa:
        return await self.repo.create(khoa_data)
    
    async def update_khoa(self, ma_khoa: str, khoa_data: KhoaUpdate) -> Khoa:
        khoa = await self.repo.update(ma_khoa, khoa_data)
        if not khoa:
            raise ValueError(f"Không thể cập nhật khoa với mã '{ma_khoa}', có thể mã này không tồn tại.")
        return khoa
    
    async def delete_khoa(self, ma_khoa: str) -> bool:
        success = await self.repo.delete(ma_khoa)
        if not success:
            raise ValueError(f"Không thể xóa khoa với mã '{ma_khoa}', có thể mã này không tồn tại.")
        return success
