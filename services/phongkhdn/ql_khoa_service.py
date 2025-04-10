from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from repositories.base_repositories import KhoaRepository
from schemas.base_schemas import KhoaCreate, KhoaResponse, KhoaUpdate

class QLKhoaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = KhoaRepository(db)

    # Xem thông tin danh sách khoa
    async def get_all(self) -> list[KhoaResponse]:
        try:
            danh_sach_khoa = await self.repo.get_all()
            return [KhoaResponse.model_validate(khoa) for khoa in danh_sach_khoa]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách khoa: {str(e)}")

    async def get(self, ma_khoa: str) -> KhoaResponse:
        try:
            khoa = await self.repo.get(ma_khoa)
            if khoa is None:
                raise HTTPException(status_code=404, detail=f"Khoa với mã '{ma_khoa}' không tồn tại.")
            return KhoaResponse.model_validate(khoa)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi lấy thông tin khoa: {str(e)}")

    async def add(self, khoa_data: KhoaCreate) -> KhoaResponse:
        try:
            # Kiểm tra nếu khoa đã tồn tại trước khi tạo mới
            existing_khoa = await self.repo.get(khoa_data.ma_khoa)
            if existing_khoa:
                raise HTTPException(status_code=400, detail="Khoa đã tồn tại.")
            
            khoa_moi = await self.repo.create(khoa_data.model_dump())
            await self.db.commit()  # Commit sau khi tạo mới
            return KhoaResponse.model_validate(khoa_moi)
        except IntegrityError:
            await self.db.rollback()  # Rollback nếu có lỗi
            raise HTTPException(status_code=400, detail="Khoa vi phạm ràng buộc dữ liệu.")
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback nếu có lỗi
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo khoa: {str(e)}")

    async def update(self, ma_khoa: str, khoa_data: KhoaUpdate) -> KhoaResponse:
        try:
            update_data = khoa_data.model_dump(exclude_unset=True)
            khoa_cap_nhat = await self.repo.update(ma_khoa, update_data)
            if khoa_cap_nhat is None:
                raise HTTPException(status_code=404, detail=f"Khoa với mã '{ma_khoa}' không tồn tại.")
            await self.db.commit()  # Commit sau khi cập nhật
            return KhoaResponse.model_validate(khoa_cap_nhat)
        except IntegrityError:
            await self.db.rollback()  # Rollback nếu có lỗi
            raise HTTPException(status_code=400, detail="Dữ liệu cập nhật vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback nếu có lỗi
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật khoa: {str(e)}")

    async def delete(self, ma_khoa: str) -> dict:
        try:
            success = await self.repo.delete(ma_khoa)
            if not success:
                raise HTTPException(status_code=404, detail=f"Khoa với mã '{ma_khoa}' không tồn tại.")
            await self.db.commit()  # Commit sau khi xóa
            return {"success": True, "message": "Xóa khoa thành công."}
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback nếu có lỗi
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa khoa: {str(e)}")
