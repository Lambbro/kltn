import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from schemas import base_schemas as schemas
from repositories.sinhvien_repository import SinhVienRepository
from repositories.taikhoan_repository import TaiKhoanRepository
from typing import List
from models.base_models import SinhVien
from auths.auth import check_permission

class QLSinhVienService:
    def __init__(self, db: AsyncSession, current_user: dict):
        self.db = db
        self.sv_repo = SinhVienRepository(db)
        self.tk_repo = TaiKhoanRepository(db)
        self.current_user = current_user
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def xem_sv(self, ma_sv: str):
        check_permission(self.current_user, 1)
        try:
            sinh_vien = await self.sv_repo.get(ma_sv)
            if not sinh_vien:
                raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
            return schemas.SinhVienResponse.model_validate(sinh_vien)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi xem sinh viên")
        
    async def xem_danh_sach_sv(self, skip: int = 0, limit: int = 100) -> List[schemas.SinhVienResponse]:
        check_permission(self.current_user, 1)
        try:
            danh_sach_sv = await self.sv_repo.get_all(skip, limit)
            if not danh_sach_sv:
                raise HTTPException(status_code=404, detail="Không có sinh viên nào trong danh sách")

            return [schemas.SinhVienResponse.model_validate(sv) for sv in danh_sach_sv]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xem danh sách sinh viên: {str(e)}")

    async def tao_sinh_vien(self, sinh_vien: schemas.SinhVienCreate):
        check_permission(self.current_user, 1)
        email = f"{sinh_vien.ma_sv}@students.hou.edu.vn"
        mat_khau = sinh_vien.cccd

        try:
            # Tạo tài khoản sinh viên
            tai_khoan_data = {
                "email": email,
                "mat_khau": self.hash_password(mat_khau),
                "quyen_han": 4  # Quyền hạn: Sinh viên
            }
            await self.tk_repo.create(tai_khoan_data)

            # Tạo sinh viên
            sinh_vien_data = sinh_vien.model_dump()
            sinh_vien_data["email"] = email  # Gán email
            new_sinh_vien = await self.sv_repo.create(sinh_vien_data)

            await self.db.commit()  # Thực hiện commit

            return schemas.SinhVienResponse.model_validate(new_sinh_vien)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Sinh viên hoặc tài khoản đã tồn tại")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo sinh viên: {str(e)}")
    
    async def tao_danh_sach_sinh_vien(self, danh_sach_sinh_vien: list[schemas.SinhVienCreate]):
        check_permission(self.current_user, 1)

        try:
            danh_sach_sinh_vien_db = []

            for sv in danh_sach_sinh_vien:
                email = f"{sv.ma_sv}@students.hou.edu.vn"
                mat_khau = sv.cccd

                # Tạo tài khoản
                tai_khoan_data = {
                    "email": email,
                    "mat_khau": self.hash_password(mat_khau),
                    "quyen_han": 4
                }
                await self.tk_repo.create(tai_khoan_data)

                # Chuẩn bị dữ liệu sinh viên
                sinh_vien_data = sv.model_dump()
                sinh_vien_data["email"] = email
                danh_sach_sinh_vien_db.append(SinhVien(**sinh_vien_data))

            self.db.add_all(danh_sach_sinh_vien_db)
            await self.db.commit()  # Commit dữ liệu

            return {"message": "Thêm danh sách sinh viên thành công!"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo danh sách sinh viên: {str(e)}")

    async def xoa_sinh_vien(self, ma_sv: str):
        check_permission(self.current_user, 1)
        sinh_vien = await self.sv_repo.get(ma_sv)
        if not sinh_vien:
            raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

        try:
            await self.tk_repo.delete(sinh_vien.email)
            await self.sv_repo.delete(ma_sv)
            await self.db.commit()  # Commit thay đổi
            return {"message": "Xóa sinh viên thành công"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa sinh viên: {str(e)}")
    
    async def cap_nhat_sinh_vien(self, ma_sv: str, sinh_vien_update: schemas.SinhVienUpdate):
        check_permission(self.current_user, 1)
        sinh_vien = await self.sv_repo.get(ma_sv)
        if not sinh_vien:
            raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

        try:
            # Cập nhật thông tin
            update_data = sinh_vien_update.model_dump(exclude_unset=True)
            updated_sinh_vien = await self.sv_repo.update(ma_sv, update_data)
            await self.db.commit()  # Commit thay đổi
            return schemas.SinhVienResponse.model_validate(updated_sinh_vien)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Dữ liệu cập nhật vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật sinh viên: {str(e)}")
