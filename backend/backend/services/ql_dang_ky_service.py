import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from fastapi import HTTPException

from models import base_models as models
from schemas import base_schemas as schemas

class QLDangKyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def tao_sinh_vien(self, sinh_vien: schemas.SinhVienCreate):
        async with self.db.begin():
            try:
                # Tạo email từ mã sinh viên
                email = f"{sinh_vien.ma_sv}@gmail.com"
                mat_khau = sinh_vien.cccd
                
                # Tạo tài khoản sinh viên
                tai_khoan = models.TaiKhoan(
                    email=email,
                    mat_khau=self.hash_password(mat_khau),  # Mật khẩu mặc định
                    quyen_han=4  # Quyền hạn: Sinh viên
                )
                self.db.add(tai_khoan)

                # Tạo sinh viên
                sinh_vien_data = sinh_vien.model_dump()
                sinh_vien_data["email"] = email  # Cập nhật email
                sinh_vien_model = models.SinhVien(**sinh_vien_data)
                self.db.add(sinh_vien_model)

                await self.db.commit()
                return schemas.SinhVienResponse(**sinh_vien.model_dump())

            except SQLAlchemyError:
                await self.db.rollback()
                raise HTTPException(status_code=500, detail="Lỗi khi tạo sinh viên")

    async def tao_danh_sach_sinh_vien(self, danh_sach_sinh_vien: list[schemas.SinhVienCreate]):
        async with self.db.begin():
            try:
                sinh_vien_models = []
                tai_khoan_models = []

                for sv in danh_sach_sinh_vien:
                    email = f"{sv.ma_sv}@gmail.com"

                    # Tạo tài khoản cho sinh viên
                    tai_khoan = models.TaiKhoan(
                        email=email,
                        mat_khau=self.hash_password("matkhau123"),
                        quyen_han=4
                    )
                    tai_khoan_models.append(tai_khoan)

                    # Tạo sinh viên
                    sinh_vien_data = sv.model_dump()
                    sinh_vien_data["email"] = email
                    sinh_vien_models.append(models.SinhVien(**sinh_vien_data))

                self.db.add_all(tai_khoan_models)
                self.db.add_all(sinh_vien_models)

                await self.db.commit()
                return [schemas.SinhVienResponse(**sv.model_dump()) for sv in danh_sach_sinh_vien]

            except SQLAlchemyError:
                await self.db.rollback()
                raise HTTPException(status_code=500, detail="Lỗi khi tạo danh sách sinh viên")
            
    async def tao_giang_vien(self, giang_vien: schemas.GiangVienCreate):
        try:
            email = giang_vien.email
            quyen_han = giang_vien.quyen_han
            mat_khau = giang_vien.cccd

            tai_khoan = models.TaiKhoan(
                email=email,
                mat_khau=self.hash_password(mat_khau),
                quyen_han=quyen_han  
            )
            self.db.add(tai_khoan)

            giang_vien_data = {key: value for key, value in giang_vien.model_dump().items() if key != "quyen_han"}
            giang_vien_model = models.GiangVien(**giang_vien_data)
            self.db.add(giang_vien_model)

            if not self.db.in_transaction():
                async with self.db.begin():  # Transaction sẽ tự commit khi thành công
                    return schemas.GiangVienResponse(**giang_vien.model_dump())
            else:
                await self.db.flush()  # Chỉ flush nếu đã có transaction
                return schemas.GiangVienResponse(**giang_vien.model_dump())

        except SQLAlchemyError:
            if self.db.in_transaction():  
                await self.db.rollback()  # Đảm bảo rollback nếu có lỗi
            raise HTTPException(status_code=500, detail="Lỗi khi tạo giảng viên")