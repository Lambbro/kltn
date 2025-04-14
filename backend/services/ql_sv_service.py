import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from datetime import date

from schemas import base_schemas as schemas
from repositories.sinhvien_repository import SinhVienRepository
from repositories.taikhoan_repository import TaiKhoanRepository
from repositories.base_repositories import KhoaRepository
from typing import List
from models.base_models import SinhVien

class QLSinhVienService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sv_repo = SinhVienRepository(db)
        self.tk_repo = TaiKhoanRepository(db)
        self.khoa_repo = KhoaRepository(db)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def is_valid_cccd(cccd: str) -> bool:
        return cccd.isdigit() and len(cccd) == 12
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10
    
    @staticmethod
    def is_valid_age(birth_date: date) -> bool:
        return date.today().year - birth_date.year >= 18
    
    #Xem thông tin sinh viên
    async def get(self, ma_sv: str, ma_khoa: str = None):
        try:
            if ma_khoa:
                sinh_vien = await self.sv_repo.khoa_get(ma_sv, ma_khoa)
            else:
                sinh_vien = await self.sv_repo.get(ma_sv)
            if not sinh_vien:
                raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
            return schemas.SinhVienResponse.model_validate(sinh_vien)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi xem sinh viên")

    ##Xem danh sách sinh viên
    async def get_all(self, ma_khoa: str = None, skip: int = 0, limit: int = 100) -> List[schemas.SinhVienResponse]:
        try:
            if ma_khoa:
                danh_sach_sv = await self.sv_repo.khoa_get_all(ma_khoa, skip, limit)
            else:
                danh_sach_sv = await self.sv_repo.get_all(skip, limit)
            if not danh_sach_sv:
                raise HTTPException(status_code=404, detail="Không có sinh viên nào trong danh sách")

            return [schemas.SinhVienResponse.model_validate(sv) for sv in danh_sach_sv]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi xem danh sách sinh viên: {str(e)}")


    async def add(self, sinh_vien: schemas.SinhVienCreateReal):

        sinh_vien.ma_sv = sinh_vien.ma_sv.strip()
        sinh_vien.cccd = sinh_vien.cccd.strip()
        sinh_vien.ten_sv = sinh_vien.ten_sv.strip()
        sinh_vien.sdt = sinh_vien.sdt.strip()
        sinh_vien.ma_khoa = sinh_vien.ma_khoa.strip()

        #validate thông tin sinh viên
        if sinh_vien.ma_sv == "" or sinh_vien.cccd == "" or sinh_vien.ten_sv == "" or sinh_vien.ngay_sinh == "" or sinh_vien.sdt == "" or sinh_vien.ma_khoa == "":
            raise HTTPException(status_code=400, detail="Thông tin sinh viên không hợp lệ")
        
        if not self.is_valid_cccd(sinh_vien.cccd):
            raise HTTPException(status_code=400, detail="CCCD không hợp lệ")

        if not self.is_valid_phone(sinh_vien.sdt):
            raise HTTPException(status_code=400, detail="Số điện thoại phải là 10 chữ số")

        khoa = await self.khoa_repo.get(sinh_vien.ma_khoa)
        if not khoa:
            raise HTTPException(status_code=404, detail="Khoa không tồn tại")

        nam_sinh = sinh_vien.ngay_sinh
        if not self.is_valid_age(nam_sinh):
            raise HTTPException(status_code=400, detail="Sinh viên phải từ 18 tuổi trở lên")
        
        #tạo tk, sv
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
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Sinh viên hoặc tài khoản đã tồn tại")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo sinh viên: {str(e)}")
    
    async def add_all(self, danh_sach_sinh_vien: list[schemas.SinhVienCreateReal]):

        try:
            danh_sach_sinh_vien_db = []

            for sv in danh_sach_sinh_vien:

                sv.ma_sv = sv.ma_sv.strip()
                sv.cccd = sv.cccd.strip()
                sv.ten_sv = sv.ten_sv.strip()
                sv.sdt = sv.sdt.strip()
                sv.ma_khoa = sv.ma_khoa.strip()

                #validate thông tin sinh viên
                if sv.ma_sv == "" or sv.cccd == "" or sv.ten_sv == "" or sv.ngay_sinh == "" or sv.sdt == "" or sv.ma_khoa == "":
                    raise HTTPException(status_code=400, detail="Thông tin sinh viên không hợp lệ")
                
                if not self.is_valid_cccd(sv.cccd):
                    raise HTTPException(status_code=400, detail="CCCD không hợp lệ")

                if not self.is_valid_phone(sv.sdt):
                    raise HTTPException(status_code=400, detail="Số điện thoại phải là 10 chữ số")

                khoa = await self.khoa_repo.get(sv.ma_khoa)
                if not khoa:
                    raise HTTPException(status_code=404, detail="Khoa không tồn tại")

                nam_sinh = sv.ngay_sinh
                if not self.is_valid_age(nam_sinh):
                    raise HTTPException(status_code=400, detail="Sinh viên phải từ 18 tuổi trở lên")
                
                
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
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo danh sách sinh viên: {str(e)}")

    async def delete(self, ma_sv: str):
        sinh_vien = await self.sv_repo.get(ma_sv)
        if not sinh_vien:
            raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

        try:
            await self.tk_repo.delete(sinh_vien.email)
            await self.sv_repo.delete(ma_sv)
            await self.db.commit()  # Commit thay đổi
            return {"message": "Xóa sinh viên thành công"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa sinh viên: {str(e)}")
    
    async def update(self, ma_sv: str, sinh_vien_update: schemas.SinhVienUpdate):
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
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Dữ liệu cập nhật vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật sinh viên: {str(e)}")