import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from schemas import base_schemas as schemas
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

class DangNhapService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def dang_nhap(self, dang_nhap: schemas.TaiKhoanLogin)  -> schemas.TaiKhoanResponse:
        # Kiểm tra dữ liệu đầu vào
        if not dang_nhap.email or not dang_nhap.mat_khau:
            raise HTTPException(status_code=400, detail="Email và mật khẩu không được để trống")

        try:
            query = select(models.TaiKhoan).where(models.TaiKhoan.email == dang_nhap.email)
            result = await self.db.execute(query)
            tai_khoan = result.scalars().first()

            if tai_khoan is None or tai_khoan.mat_khau != self.hash_password(dang_nhap.mat_khau):
                raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")

            return schemas.TaiKhoanResponse(
                email=tai_khoan.email,
                quyen_han=tai_khoan.quyen_han
            )

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Lỗi kết nối cơ sở dữ liệu")