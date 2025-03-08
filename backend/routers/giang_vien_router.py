from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import GiangVien, GiangVienCreate, GiangVienUpdate
from services.giang_vien_service import GiangVienService
from typing import List

router = APIRouter(prefix="/giang_vien", tags=["Giảng Viên"])

@router.get("/", response_model=List[GiangVien])
async def get_all_giang_vien(db: AsyncSession = Depends(get_db)):
    return await GiangVienService(db).get_all_giang_vien()

@router.get("/{ma_gv}", response_model=GiangVien)
async def get_giang_vien(ma_gv: str, db: AsyncSession = Depends(get_db)):
    return await GiangVienService(db).get_giang_vien(ma_gv)

@router.post("/", response_model=GiangVien)
async def create_giang_vien(giang_vien: GiangVienCreate, db: AsyncSession = Depends(get_db)):
    return await GiangVienService(db).create_giang_vien(giang_vien, db)

@router.put("/{ma_gv}", response_model=GiangVien)
async def update_giang_vien(ma_gv: str, giang_vien: GiangVienUpdate, db: AsyncSession = Depends(get_db)):
    return await GiangVienService(db).update_giang_vien(ma_gv, giang_vien)

@router.delete("/{ma_gv}")
async def delete_giang_vien(ma_gv: str, db: AsyncSession = Depends(get_db)):
    return await GiangVienService(db).delete_giang_vien(ma_gv)
