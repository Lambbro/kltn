import repositories.nckh_repository as repository
import schemas.nckh_schemas as schemas
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class DeTaiNCKHGVService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.DeTaiNCKHGVRepository(db)

    async def get_all(self) -> List[schemas.DeTaiNCKHGV]:
        return await self.repo.get_all()
    
    async def get(self, ma_de_tai: int) -> schemas.DeTaiNCKHGV:
        de_tai = await self.repo.get(ma_de_tai)
        if not de_tai:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy đề tài có mã {ma_de_tai}")
        return de_tai
    
    async def create(self, de_tai_data: schemas.DeTaiNCKHGVCreate) -> schemas.DeTaiNCKHGV:
        return await self.repo.create(de_tai_data)
    
    async def update(self, ma_de_tai: int, de_tai_data: schemas.DeTaiNCKHGVUpdate) -> schemas.DeTaiNCKHGV:
        de_tai = await self.repo.update(ma_de_tai, de_tai_data)
        if not de_tai:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy đề tài {ma_de_tai} để cập nhật")
        return de_tai
    
    async def delete(self, ma_de_tai: int) -> dict:
        success = await self.repo.delete(ma_de_tai)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa đề tài có mã {ma_de_tai}")
        return {"success": True, "message": "Xóa thành công đề tài giảng viên."}
    
class TaiLieuNCKHGVService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.TaiLieuNCKHGVRepository(db)

    async def get_all(self) -> List[schemas.TaiLieuNCKHGV]:
        return await self.repo.get_all()
    
    async def get(self, ma_tai_lieu:int ) -> schemas.TaiLieuNCKHGV:
        tai_lieu = await self.repo.get(ma_tai_lieu)
        if not tai_lieu:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy tài liệu mã {ma_tai_lieu}")
        return tai_lieu
    
    async def create(self, de_tai_data: schemas.TaiLieuNCKHGVCreate) -> schemas.TaiLieuNCKHGV:
        return await self.repo.create(de_tai_data)
    
    async def update(self, ma_tai_lieu: int, tai_lieu_data: schemas.TaiLieuNCKHGVUpdate) -> schemas.TaiLieuNCKHGV:
        tai_lieu = await self.repo.update(ma_tai_lieu, tai_lieu_data)
        if not tai_lieu:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật tài liệu mã {ma_tai_lieu}")
        return tai_lieu
    
    async def delete(self, ma_tai_lieu: int) -> dict:
        success = await self.repo.delete(ma_tai_lieu)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa tài liệu {ma_tai_lieu}")
        return {"success": True, "message": "Xóa thành công tài liệu"}