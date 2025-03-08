import hashlib
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import models
from schemas import schemas
from fastapi import HTTPException

class TaiKhoanService:
    @staticmethod
    async def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    async def dang_ky(db: AsyncSession, tai_khoan: schemas.TaiKhoanCreate):
        hashed_password = TaiKhoanService.hash_password(tai_khoan.mat_khau)
        new_tai_khoan = models.TaiKhoan(
            email=tai_khoan.email,
            mat_khau=hashed_password,
            quyen_han=tai_khoan.quyen_han
        )
        db.add(new_tai_khoan)
        try:
            await db.commit()
            await db.refresh(new_tai_khoan)
            return new_tai_khoan
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Email đã tồn tại.")

    @staticmethod
    async def dang_nhap(db: AsyncSession, email: str, mat_khau: str):
        hashed_password = TaiKhoanService.hash_password(mat_khau)
        result = await db.execute(select(models.TaiKhoan).filter(
            models.TaiKhoan.email == email,
            models.TaiKhoan.mat_khau == hashed_password
        ))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng.")
        return user

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(models.TaiKhoan))
        return result.scalars().all()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(models.TaiKhoan).filter(models.TaiKhoan.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="Tài khoản không tồn tại.")
        return user

    @staticmethod
    async def update(db: AsyncSession, email: str, tai_khoan: schemas.TaiKhoanUpdate):
        user = await TaiKhoanService.get_by_email(db, email)

        if tai_khoan.quyen_han is not None:
            user.quyen_han = tai_khoan.quyen_han

        if tai_khoan.mat_khau:
            user.mat_khau = TaiKhoanService.hash_password(tai_khoan.mat_khau)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(db: AsyncSession, email: str):
        user = await TaiKhoanService.get_by_email(db, email)

        await db.delete(user)
        await db.commit()
        return {"success": True, "message": f"Tài khoản '{email}' đã được xóa thành công."}
