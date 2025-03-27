from repositories.repository import HuongNghienCuuRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from typing import List
from fastapi import HTTPException

class HuongNghienCuuService:
    def __init__(self, db: AsyncSession):
        self.repo = HuongNghienCuuRepository(db)

    async def get_all_hnc(self) -> List[HuongNghienCuu]:
        return await self.repo.get_all()
    
    async def get_hnc(self, ma_hnc: int) -> HuongNghienCuu:
        hnc = await self.repo.get(ma_hnc)
        if hnc is None:
            raise HTTPException(status_code=404, detail=f"Hướng nghiên cứu với mã '{ma_hnc}' không tồn tại.")
        return hnc
    
    async def create_hnc(self, hnc_data: HuongNghienCuuCreate) -> HuongNghienCuu:
        return await self.repo.create(hnc_data)
    
    async def update_hnc(self, ma_hnc: int, hnc_data: HuongNghienCuuUpdate) -> HuongNghienCuu:
        updated_hnc = await self.repo.update(ma_hnc, hnc_data)
        if updated_hnc is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Hướng nghiên cứu với mã '{ma_hnc}' không tồn tại.")
        return updated_hnc
    
    async def delete_hnc(self, ma_hnc: int) -> bool:
        success = await self.repo.delete(ma_hnc)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa. Hướng nghiên cứu với mã '{ma_hnc}' không tồn tại.")
        return {"success": True, "message": "Xóa sinh viên thành công."}