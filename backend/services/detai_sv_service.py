import schemas.detai_sv_schemas as schemas
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from repositories.detai_sv_repositories import DangKyNCKHRepository, NguyenVongDKRepository
from auths.auth import check_permission, check_higher_permission

class DangKyNCKHService:
    def __init__(self, db: AsyncSession, current_user: dict):
        self.db = db
        self.dk_repo = DangKyNCKHRepository(db)
        self.nv_repo = NguyenVongDKRepository(db)
        self.current_user = current_user

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[schemas.DangKyNCKHResponse]:
        check_permission(self.current_user, 1)
        try:
            dsdk = await self.dk_repo.get_all(skip, limit)
            if not dsdk:
                raise HTTPException(status_code=404, detail="Chưa có sinh viên nào đăng ký")
            return [schemas.DangKyNCKHResponse.model_validate(dk) for dk in dsdk]
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xem danh sách đăng ký")

    async def get(self, ma_dk: int) -> schemas.DangKyNCKHResponse:
        check_permission(self.current_user, 1)
        try:
            dang_ky = await self.dk_repo.get(ma_dk)
            if not dang_ky:
                raise HTTPException(status_code=404, detail=f"Không tìm thấy đăng ký nckh với mã {ma_dk}")
            return schemas.DangKyNCKHResponse.model_validate(dang_ky)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi xem đăng ký")
    
    async def create(self, dang_ky: schemas.DangKyNCKHCreate, list_nguyen_vong: List[schemas.NguyenVongDKCreate]) -> schemas.DangKyNCKHResponse:
        check_higher_permission(self.current_user, 4)

        if len(list_nguyen_vong) > 2:
            raise HTTPException(status_code=400, detail="Chỉ được đăng ký tối đa 2 nguyện vọng")

        try:
            new_dk = await self.dk_repo.create(dang_ky.model_dump())
            
            for nv in list_nguyen_vong:
                nv.ma_dk = new_dk.ma_dk
                await self.nv_repo.create(nv.model_dump())
            
            await self.db.commit()

            return schemas.DangKyNCKHResponse.model_validate(new_dk)
        
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Lỗi ràng buộc dữ liệu: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo đăng ký hoặc nguyện vọng: {str(e)}")
    
    async def update(self, ma_dk: int, list_nv: List[schemas.NguyenVongDKUpdate]) -> schemas.NguyenVongDKResponse:
        check_higher_permission(self.current_user, 4)
        try:
            dang_ky = await self.dk_repo.get(ma_dk)
            if not dang_ky:
                raise HTTPException(status_code=404, detail=f"Không tìm thấy đăng ký mã {ma_dk}")

            updated_nv_list = []
            for nv in list_nv:
                updated_nv = await self.nv_repo.update(ma_dk, nv.ma_gv, nv.model_dump(exclude_unset=True))
                if updated_nv:
                    updated_nv_list.append(schemas.NguyenVongDKResponse.model_validate(updated_nv))

            await self.db.commit()
            return updated_nv_list

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Dữ liệu cập nhật vi phạm ràng buộc: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật dữ liệu đăng ký tham dự nckh: {str(e)}")

    async def delete(self, ma_dang_ky: int) -> dict:
        check_higher_permission(self.current_user, 4)

        try:
            success = await self.dk_repo.delete(ma_dang_ky)
            if not success:
                raise HTTPException(status_code=404, detail=f"Không thể xóa đăng ký với mã {ma_dang_ky}")

            await self.db.commit()
            return {"success": True, "message": "Xóa đăng ký NCKH thành công."}

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa đăng ký: {str(e)}")