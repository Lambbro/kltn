from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from fastapi import HTTPException

from repositories.base_repositories import KhenThuongRepository
from schemas.base_schemas import KhenThuongCreate, KhenThuongResponse, KhenThuongUpdate

class QLKhenThuongService:
    def __init__(self, db: AsyncSession):
        self.repo = KhenThuongRepository(db)
        self.db = db

    # Lấy tất cả khen thưởng
    async def get_all(self) -> list[KhenThuongResponse]:
        try:
            return await self.repo.get_all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

    # Lấy thông tin khen thưởng theo mã
    async def get(self, ma_khen_thuong: str) -> KhenThuongResponse:
        try:
            khen_thuong = await self.repo.get(ma_khen_thuong)
            if khen_thuong is None:
                raise HTTPException(status_code=404, detail=f"Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
            return khen_thuong
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

    # Tạo mới khen thưởng
    async def add(self, khen_thuong_data: KhenThuongCreate) -> KhenThuongResponse:
        try:
            return await self.repo.create(khen_thuong_data)
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa).")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo mới: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định khi tạo mới: {str(e)}")

    # Cập nhật thông tin khen thưởng
    async def update(self, ma_khen_thuong: str, khen_thuong_data: KhenThuongUpdate) -> KhenThuongResponse:
        try:
            khen_thuong = await self.repo.update(ma_khen_thuong, khen_thuong_data)
            if khen_thuong is None:
                raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
            return khen_thuong
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu khi cập nhật.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định khi cập nhật: {str(e)}")

    # Xóa khen thưởng
    async def delete(self, ma_khen_thuong: str) -> dict:
        try:
            success = await self.repo.delete(ma_khen_thuong)
            if not success:
                raise HTTPException(status_code=404, detail=f"Không thể xóa. Khen thưởng với mã '{ma_khen_thuong}' không tồn tại.")
            await self.db.commit()
            return {"success": True, "message": "Xóa khen thưởng thành công."}
        except HTTPException as http_err:
            raise http_err
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định khi xóa: {str(e)}")