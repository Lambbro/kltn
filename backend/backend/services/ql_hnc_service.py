from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from repositories.base_repositories import HuongNghienCuuRepository
from schemas.base_schemas import HuongNghienCuuCreate, HuongNghienCuuResponse, HuongNghienCuuUpdate

class QLHuongNghienCuuService:
    def __init__(self, db: AsyncSession):
        self.repo = HuongNghienCuuRepository(db)

    async def get_all_huong_nghien_cuu(self) -> list[HuongNghienCuuResponse]:
        return await self.repo.get_all()
    
    async def get_huong_nghien_cuu(self, ma_huong_nghien_cuu: str) -> HuongNghienCuuResponse:
        huong_nghien_cuu = await self.repo.get(ma_huong_nghien_cuu)
        if huong_nghien_cuu is None:
            raise HTTPException(status_code=404, detail=f"Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
        return huong_nghien_cuu
    
    async def create_huong_nghien_cuu(self, huong_nghien_cuu_data: HuongNghienCuuCreate) -> HuongNghienCuuResponse:
        return await self.repo.create(huong_nghien_cuu_data)
    
    async def update_huong_nghien_cuu(self, ma_huong_nghien_cuu: str, huong_nghien_cuu_data: HuongNghienCuuUpdate) -> HuongNghienCuuResponse:
        huong_nghien_cuu = await self.repo.update(ma_huong_nghien_cuu, huong_nghien_cuu_data)
        if huong_nghien_cuu is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
        return huong_nghien_cuu
    
    async def delete_huong_nghien_cuu(self, ma_huong_nghien_cuu: str) -> dict:
        success = await self.repo.delete(ma_huong_nghien_cuu)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa. Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
        return {"success": True, "message": "Xóa hướng nghiên cứu thành công."}