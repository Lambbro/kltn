import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import re

from schemas.base_schemas import GiangVienCreate, GiangVienResponse, GiangVienUpdate
from repositories.taikhoan_repository import TaiKhoanRepository
from repositories.giangvien_repository import GiangVienRepository

class QLGiangVienService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tk_repo = TaiKhoanRepository(db)
        self.gv_repo = GiangVienRepository(db)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10

    # Tạo tài khoản giảng viên
    async def add(self, giang_vien: GiangVienCreate):
        
        if not self.is_valid_email(giang_vien.email):
            raise HTTPException(status_code=400, detail="Email không hợp lệ")

        if not self.is_valid_phone(giang_vien.sdt):
            raise HTTPException(status_code=400, detail="Số điện thoại phải là 10 chữ số")

        try:
            # Kiểm tra email đã tồn tại chưa
            existing_account = await self.tk_repo.get(giang_vien.email)
            if existing_account:
                raise HTTPException(status_code=400, detail="Email đã tồn tại")

            # Tạo tài khoản trước
            tai_khoan_data = {
                "email": giang_vien.email,
                "mat_khau": self.hash_password(giang_vien.cccd),
                "quyen_han": giang_vien.quyen_han
            }
            db_tai_khoan = await self.tk_repo.create(tai_khoan_data)  # Nếu repo đã commit, không cần transaction

            # Tạo giảng viên (bỏ `quyen_han` vì nó đã lưu trong tài khoản)
            giang_vien_data = giang_vien.model_dump(exclude={"quyen_han"})
            db_giang_vien = await self.gv_repo.create(giang_vien_data)

            await self.db.commit()
            return GiangVienResponse.model_validate(db_giang_vien)
        except IntegrityError:
            await self.db.rollback()  # Rollback transaction nếu có lỗi
            raise HTTPException(status_code=400, detail="Email đã tồn tại")
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback transaction nếu có lỗi
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo giảng viên: {str(e)}")

    # Xóa tài khoản giảng viên
    async def delete(self, ma_gv: str):
        try:
            giang_vien = await self.gv_repo.get(ma_gv)
            if not giang_vien:
                raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")

            await self.tk_repo.delete(giang_vien.email)
            await self.gv_repo.delete(ma_gv)

            await self.db.commit()

            return {"message": "Xóa giảng viên thành công"}

        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Lỗi khi xóa giảng viên")

    # Đăng ký danh sách giảng viên
    async def update(self, ma_gv: str, giang_vien_update: GiangVienUpdate):
        giang_vien = await self.gv_repo.get(ma_gv)
        if not giang_vien:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        try:
            
            update_data = giang_vien_update.model_dump(exclude_unset=True)
            updated_giang_vien = await self.gv_repo.update(ma_gv, update_data)
            await self.db.commit()
            return GiangVienResponse.model_validate(updated_giang_vien)

        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật giảng viên")

    #Xem thông tin giảng viên
    async def get(self, ma_gv: str, ma_khoa: str = None):
        try:
            if ma_khoa:
                giang_vien = await self.gv_repo.khoa_get(ma_gv, ma_khoa)
            else:
                giang_vien = await self.gv_repo.get(ma_gv)
            if not giang_vien:
                raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
            return GiangVienResponse.model_validate(giang_vien)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy thông tin giảng viên")

    #Xem danh sách giảng viên
    async def get_all(self, ma_khoa: str = None):
        try:
            if ma_khoa:
                danh_sach_giang_vien = await self.gv_repo.khoa_get_all(ma_khoa)
            else:
                danh_sach_giang_vien = await self.gv_repo.get_all()
            return [GiangVienResponse.model_validate(gv) for gv in danh_sach_giang_vien]
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy danh sách giảng viên")