from repositories.repository import HuongNghienCuuRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from typing import List, Optional

class HuongNghienCuuService:
    def __init__(self, db: AsyncSession):
        self.repo = HuongNghienCuuRepository(db)

    async def get_all_hnc(self) -> List[HuongNghienCuu]:
        return await self.repo.get_all()
    
    async def get_hnc(self, ma_hnc: int) -> Optional[HuongNghienCuu]:
        return await self.repo.get(ma_hnc)  # Trả về `None` nếu không tìm thấy
    
    async def create_hnc(self, hnc_data: HuongNghienCuuCreate) -> HuongNghienCuu:
        return await self.repo.create(hnc_data)
    
    async def update_hnc(self, ma_hnc: int, hnc_data: HuongNghienCuuUpdate) -> Optional[HuongNghienCuu]:
        return await self.repo.update(ma_hnc, hnc_data)  # Trả về `None` nếu không cập nhật được
    
    async def delete_hnc(self, ma_hnc: int) -> bool:
        return await self.repo.delete(ma_hnc)  # Trả về `False` nếu không xóa được
