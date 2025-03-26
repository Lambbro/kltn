from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from repositories.base_repositories import KhenThuongRepository
from schemas.base_schemas import KhenThuongCreate, KhenThuongResponse, KhenThuongUpdate

class QLKhenThuongService:
    def __init__(self, db: AsyncSession):
        self.repo = KhenThuongRepository(db)

    async def get_all_khen_thuong(self) -> list[KhenThuongResponse]:
        return await self.repo.get_all()
    
    async def get_khen_thuong(self, ma_khen_thuong: str) -> KhenThuongResponse:
        khen_thuong = await self.repo.get(ma_khen_thuong)
        if khen_thuong is None:
            raise HTTPException(status_code=404, detail=f"Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
        return khen_thuong
    
    async def create_khen_thuong(self, khen_thuong_data: KhenThuongCreate) -> KhenThuongResponse:
        return await self.repo.create(khen_thuong_data)
    
    async def update_khen_thuong(self, ma_khen_thuong: str, khen_thuong_data: KhenThuongUpdate) -> KhenThuongResponse:
        khen_thuong = await self.repo.update(ma_khen_thuong, khen_thuong_data)
        if khen_thuong is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
        return khen_thuong
    
    async def delete_khen_thuong(self, ma_khen_thuong: str) -> dict:
        success = await self.repo.delete(ma_khen_thuong)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa. Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
        return {"success": True, "message": "Xóa khen thuởng thành công."}
