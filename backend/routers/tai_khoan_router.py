from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import TaiKhoan, TaiKhoanCreate, TaiKhoanUpdate
from services.tai_khoan_service import TaiKhoanService
from typing import List

router = APIRouter(prefix="/tai_khoan", tags=["Tài Khoản"])

@router.post("/dang_ky", response_model=TaiKhoan)
async def dang_ky(tai_khoan: TaiKhoanCreate, db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.dang_ky(db, tai_khoan)

@router.post("/dang_nhap", response_model=TaiKhoan)
async def dang_nhap(email: str, mat_khau: str, db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.dang_nhap(db, email, mat_khau)

@router.get("/", response_model=List[TaiKhoan])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.get_all(db)

@router.get("/{email}", response_model=TaiKhoan)
async def get_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.get_by_email(db, email)

@router.put("/{email}", response_model=TaiKhoan)
async def update(email: str, tai_khoan: TaiKhoanUpdate, db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.update(db, email, tai_khoan)

@router.delete("/{email}")
async def delete(email: str, db: AsyncSession = Depends(get_db)):
    return await TaiKhoanService.delete(db, email)
