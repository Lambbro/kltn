import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import models
from schemas import schemas
from sqlalchemy.exc import IntegrityError

#Khoa Repository
class KhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, ma_khoa: str):
        result = await self.db.execute(select(models.Khoa).filter(models.Khoa.ma_khoa == ma_khoa))
        return result.scalars().first()
    
    async def get_all(self):
        result = await self.db.execute(select(models.Khoa))
        return result.scalars().all()
    
    async def create(self, khoa: schemas.KhoaCreate):
        db_khoa = models.Khoa(**khoa.model_dump())
        self.db.add(db_khoa)
        await self.db.commit()
        await self.db.refresh(db_khoa)
        return db_khoa
    
    async def update(self, ma_khoa: str, khoa: schemas.KhoaUpdate):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return None
        for key, value in khoa.model_dump(exclude_unset=True).items():
            setattr(db_khoa, key, value)
        await self.db.commit()
        await self.db.refresh(db_khoa)
        return db_khoa
    
    async def delete(self, ma_khoa: str):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return False
        await self.db.delete(db_khoa)
        await self.db.commit()
        return True
    
#Huong Nghien Cuu Repository
class HuongNghienCuuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, ma_huong_nc: int):
        result = await self.db.execute(select(models.HuongNghienCuu).filter(models.HuongNghienCuu.ma_huong_nc == ma_huong_nc))
        return result.scalars().first()
    
    async def get_all(self):
        result = await self.db.execute(select(models.HuongNghienCuu))
        return result.scalars().all()
    
    async def create(self, huong_nghien_cuu: schemas.HuongNghienCuuCreate):
        db_huong_nghien_cuu = models.HuongNghienCuu(**huong_nghien_cuu.model_dump())
        self.db.add(db_huong_nghien_cuu)
        await self.db.commit()
        await self.db.refresh(db_huong_nghien_cuu)
        return db_huong_nghien_cuu
    
    async def update(self, ma_huong_nc: int, huong_nghien_cuu: schemas.HuongNghienCuuUpdate):
        db_huong_nghien_cuu = await self.get(ma_huong_nc)
        if db_huong_nghien_cuu is None:
            return None
        for key, value in huong_nghien_cuu.model_dump(exclude_unset=True).items():
            setattr(db_huong_nghien_cuu, key, value)
        await self.db.commit()
        await self.db.refresh(db_huong_nghien_cuu)
        return db_huong_nghien_cuu

    async def delete(self, ma_huong_nc: int):
        db_huong_nghien_cuu = await self.get(ma_huong_nc)
        if db_huong_nghien_cuu is None:
            return False
        await self.db.delete(db_huong_nghien_cuu)
        await self.db.commit()
        return True

    
# TaiKhoan Repository

class TaiKhoanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, email: str):
        result = await self.db.execute(select(models.TaiKhoan).filter(models.TaiKhoan.email == email))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiKhoan))
        return result.scalars().all()

    async def create(self, tai_khoan: schemas.TaiKhoanCreate):
        """Tạo tài khoản mới, hash mật khẩu trước khi lưu."""
        hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        db_tai_khoan = models.TaiKhoan(
            email=tai_khoan.email,
            mat_khau=hashed_password,
            quyen_han=tai_khoan.quyen_han
        )
        self.db.add(db_tai_khoan)
        try:
            await self.db.commit()
            await self.db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Email đã tồn tại.") from e
        
    async def update(self, email: str, tai_khoan: schemas.TaiKhoanUpdate):
        """Cập nhật tài khoản, chỉ cập nhật quyền hạn và mật khẩu (nếu được cung cấp), hash mật khẩu trước khi lưu."""
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return None

        if tai_khoan.quyen_han is not None:
            db_tai_khoan.quyen_han = tai_khoan.quyen_han

        if tai_khoan.mat_khau is not None:
            hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
            db_tai_khoan.mat_khau = hashed_password

        await self.db.commit()
        await self.db.refresh(db_tai_khoan)
        return db_tai_khoan
    
    async def update_matkhau(self, email: str, new_password: str):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return None
        
        hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        db_tai_khoan.mat_khau = hashed_password
        await self.db.commit()
        await self.db.refresh(db_tai_khoan)
        return db_tai_khoan

    async def delete(self, email: str):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return False
        await self.db.delete(db_tai_khoan)
        await self.db.commit()
        return True
    
# SinhVien Repository
class SinhVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sv: str):
        result = await self.db.execute(select(models.SinhVien).filter(models.SinhVien.ma_sv == ma_sv))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.SinhVien))
        return result.scalars().all()

    async def create(self, sinh_vien: schemas.SinhVienCreate):
        db_sinh_vien = models.SinhVien(**sinh_vien.model_dump())
        self.db.add(db_sinh_vien)
        await self.db.commit()
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def update(self, ma_sv: str, sinh_vien: schemas.SinhVienUpdate):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return None
        for key, value in sinh_vien.model_dump(exclude_unset=True).items():
            setattr(db_sinh_vien, key, value)
        await self.db.commit()
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def delete(self, ma_sv: str):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return False
        await self.db.delete(db_sinh_vien)
        await self.db.commit()
        return True
    
# GiangVien Repository
class GiangVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_gv: str):
        result = await self.db.execute(select(models.GiangVien).filter(models.GiangVien.ma_gv == ma_gv))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.GiangVien))
        return result.scalars().all()

    async def create(self, giang_vien: schemas.GiangVienCreate):
        db_giang_vien = models.GiangVien(**giang_vien.model_dump())
        self.db.add(db_giang_vien)
        await self.db.commit()
        await self.db.refresh(db_giang_vien)
        return db_giang_vien

    async def update(self, ma_gv: str, giang_vien: schemas.GiangVienUpdate):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return None
        for key, value in giang_vien.model_dump(exclude_unset=True).items():
            setattr(db_giang_vien, key, value)
        await self.db.commit()
        await self.db.refresh(db_giang_vien)
        return db_giang_vien

    async def delete(self, ma_gv: str):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return False
        await self.db.delete(db_giang_vien)
        await self.db.commit()
        return True
