import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from schemas.base_schemas import GiangVienCreate, GiangVienResponse, GiangVienUpdate
from repositories.taikhoan_repository import TaiKhoanRepository
from repositories.giangvien_repository import GiangVienRepository
from auths.auth import check_permission

class QLGiangVienService:
    def __init__(self, db: AsyncSession, current_user: dict):
        self.db = db
        self.tk_repo = TaiKhoanRepository(db)
        self.gv_repo = GiangVienRepository(db)
        self.current_user = current_user
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def tao_giang_vien(self, giang_vien: GiangVienCreate):
        check_permission(self.current_user, 1)
        try:
            # Kiểm tra email đã tồn tại chưa
            existing_account = await self.tk_repo.get(giang_vien.email)
            if existing_account:
                raise HTTPException(status_code=400, detail="Email đã tồn tại")

            async with self.db.begin():  # Mở transaction
                # Tạo tài khoản trước
                tai_khoan_data = {
                    "email": giang_vien.email,
                    "mat_khau": self.hash_password(giang_vien.cccd),
                    "quyen_han": giang_vien.quyen_han
                }
                db_tai_khoan = await self.tk_repo.create(tai_khoan_data)

                # Tạo giảng viên (bỏ `quyen_han` vì nó đã lưu trong tài khoản)
                giang_vien_data = giang_vien.model_dump(exclude={"quyen_han"})
                db_giang_vien = await self.gv_repo.create(giang_vien_data)

                await self.db.commit()  # Commit sau khi tạo mới

            return GiangVienResponse.model_validate(db_giang_vien)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Email đã tồn tại")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo giảng viên: {str(e)}")

    async def xoa_giang_vien(self, ma_gv: str):
        check_permission(self.current_user, 1)
        try:
            giang_vien = await self.gv_repo.get(ma_gv)
            if not giang_vien:
                raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")

            await self.tk_repo.delete(giang_vien.email)
            await self.gv_repo.delete(ma_gv)

            await self.db.commit()

            return {"message": "Xóa giảng viên thành công"}

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi xóa giảng viên")

    async def cap_nhat_giang_vien(self, ma_gv: str, giang_vien_update: GiangVienUpdate):
        check_permission(self.current_user, 1)
        giang_vien = await self.gv_repo.get(ma_gv)
        if not giang_vien:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        try:
            
            update_data = giang_vien_update.model_dump(exclude_unset=True)
            updated_giang_vien = await self.gv_repo.update(ma_gv, update_data)
            await self.db.commit()
            return GiangVienResponse.model_validate(updated_giang_vien)

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật giảng viên")

    async def xem_giang_vien(self, ma_gv: str):
        check_permission(self.current_user, 1)
        try:
            giang_vien = await self.gv_repo.get(ma_gv)
            if not giang_vien:
                raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")

            return GiangVienResponse.model_validate(giang_vien)

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy thông tin giảng viên")

    async def lay_danh_sach_giang_vien(self):
        check_permission(self.current_user, 1)
        try:
            danh_sach_giang_vien = await self.gv_repo.get_all()
            return [GiangVienResponse.model_validate(gv) for gv in danh_sach_giang_vien]

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy danh sách giảng viên")
