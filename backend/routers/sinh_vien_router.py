from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import SinhVien, SinhVienCreate, SinhVienUpdate
from services.sinh_vien_service import SinhVienService
from typing import List

router = APIRouter(prefix="/sinh_vien", tags=["Sinh Viên"])

@router.get("/", response_model=List[SinhVien])
async def get_all_sinh_vien(db: AsyncSession = Depends(get_db)):
    return await SinhVienService(db).get_all_sinh_vien()

@router.get("/{ma_sv}", response_model=SinhVien)
async def get_sinh_vien(ma_sv: str, db: AsyncSession = Depends(get_db)):
    return await SinhVienService(db).get_sinh_vien(ma_sv)

@router.post("/", response_model=SinhVien)
async def create_sinh_vien(sinh_vien: SinhVienCreate, db: AsyncSession = Depends(get_db)):
    return await SinhVienService(db).create_sinh_vien(sinh_vien, db)

@router.put("/{ma_sv}", response_model=SinhVien)
async def update_sinh_vien(ma_sv: str, sinh_vien: SinhVienUpdate, db: AsyncSession = Depends(get_db)):
    return await SinhVienService(db).update_sinh_vien(ma_sv, sinh_vien)

@router.delete("/{ma_sv}")
async def delete_sinh_vien(ma_sv: str, db: AsyncSession = Depends(get_db)):
    service = SinhVienService(db)
    return await service.delete_sinh_vien(ma_sv)
