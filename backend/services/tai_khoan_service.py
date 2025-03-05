import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import models
from schemas import schemas

class TaiKhoanService:
    @staticmethod
    async def dang_ky(db: AsyncSession, tai_khoan: schemas.TaiKhoanCreate):
        hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        db_tai_khoan = models.TaiKhoan(
            email=tai_khoan.email,
            mat_khau=hashed_password,
            quyen_han=tai_khoan.quyen_han
        )
        db.add(db_tai_khoan)
        try:
            await db.commit()
            await db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError:
            await db.rollback()
            raise ValueError("Email đã tồn tại.")
    
    @staticmethod
    async def dang_nhap(db: AsyncSession, email: str, mat_khau: str):
        hashed_password = hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()
        result = await db.execute(select(models.TaiKhoan).filter_by(email=email, mat_khau=hashed_password))
        user = result.scalars().first()
        return user

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(models.TaiKhoan))
        return result.scalars().all()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(models.TaiKhoan).filter(models.TaiKhoan.email == email))
        return result.scalars().first()

    @staticmethod
    async def update(db: AsyncSession, email: str, tai_khoan: schemas.TaiKhoanUpdate):
        user = await TaiKhoanService.get_by_email(db, email)
        if not user:
            return None
        
        if tai_khoan.quyen_han is not None:
            user.quyen_han = tai_khoan.quyen_han
        
        if tai_khoan.mat_khau is not None:
            user.mat_khau = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete(db: AsyncSession, email: str):
        user = await TaiKhoanService.get_by_email(db, email)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        return True
