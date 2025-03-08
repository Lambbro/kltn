import repositories.syll_repository as repository
import schemas.syll_schemas as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException

class HocViService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.HocViRepository(db)

    async def get_all(self) -> List[schemas.HocVi]:
        return await self.repo.get_all()
    
    async def get(self, ma_hoc_vi: int) -> schemas.HocVi:
        hoc_vi = await self.repo.get(ma_hoc_vi)
        if not hoc_vi:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy học vị với mã '{ma_hoc_vi}'")
        return hoc_vi
    
    async def create(self, hoc_vi_data: schemas.HocViCreate) -> schemas.HocVi:
        return await self.repo.create(hoc_vi_data)
    
    async def update(self, ma_hoc_vi: int, hoc_vi_data: schemas.HocViUpdate) -> schemas.HocVi:
        hoc_vi = await self.repo.update(ma_hoc_vi, hoc_vi_data)
        if not hoc_vi:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật học vị với mã '{ma_hoc_vi}', có thể mã này không tồn tại.")
        return hoc_vi
    
    async def delete(self, ma_hoc_vi: int) -> dict:
        success = await self.repo.delete(ma_hoc_vi)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa học vị với mã '{ma_hoc_vi}', có thể mã này không tồn tại.")
        return {"success": True, "message": "Xóa học vị thành công."}