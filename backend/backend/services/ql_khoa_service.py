from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from repositories.base_repositories import KhoaRepository
from schemas.base_schemas import KhoaCreate, KhoaResponse, KhoaUpdate
from auths.auth import check_permission

class QLKhoaService:
    def __init__(self, db: AsyncSession, current_user: dict):
        self.repo = KhoaRepository(db)
        self.current_user = current_user

    async def get_all_khoa(self) -> list[KhoaResponse]:
        check_permission(self.current_user, 1)
        return await self.repo.get_all()
    
    async def get_khoa(self, ma_khoa: str) -> KhoaResponse:
        check_permission(self.current_user, 1)
        khoa = await self.repo.get(ma_khoa)
        if khoa is None:
            raise HTTPException(status_code=404, detail=f"Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa
    
    async def create_khoa(self, khoa_data: KhoaCreate) -> KhoaResponse:
        check_permission(self.current_user, 1)  # Kiểm tra quyền admin trước khi tạo
        return await self.repo.create(khoa_data)

    async def update_khoa(self, ma_khoa: str, khoa_data: KhoaUpdate) -> KhoaResponse:
        check_permission(self.current_user, 1)  # Kiểm tra quyền admin trước khi cập nhật
        khoa = await self.repo.update(ma_khoa, khoa_data)
        if khoa is None:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa

    async def delete_khoa(self, ma_khoa: str) -> dict:
        check_permission(self.current_user, 1)  # Kiểm tra quyền admin trước khi xóa
        success = await self.repo.delete(ma_khoa)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa. Khoa với mã '{ma_khoa}' không tồn tại.")
        return {"success": True, "message": "Xóa khoa thành công."}