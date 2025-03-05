from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import Khoa, KhoaCreate, KhoaUpdate
from services.khoa_service import KhoaService
from typing import List

router = APIRouter(prefix="/khoa", tags=["Khoa"])

@router.get("/", response_model=List[Khoa])
async def get_all_khoa(db: AsyncSession = Depends(get_db)):
    service = KhoaService(db)
    return await service.get_all_khoa()

@router.get("/{ma_khoa}", response_model=Khoa)
async def get_khoa(ma_khoa: str, db: AsyncSession = Depends(get_db)):
    service = KhoaService(db)
    return await service.get_khoa(ma_khoa)

@router.post("/", response_model=Khoa)
async def create_khoa(khoa: KhoaCreate, db: AsyncSession = Depends(get_db)):
    service = KhoaService(db)
    return await service.create_khoa(khoa)

@router.put("/{ma_khoa}", response_model=Khoa)
async def update_khoa(ma_khoa: str, khoa: KhoaUpdate, db: AsyncSession = Depends(get_db)):
    service = KhoaService(db)
    return await service.update_khoa(ma_khoa, khoa)

@router.delete("/{ma_khoa}")
async def delete_khoa(ma_khoa: str, db: AsyncSession = Depends(get_db)):
    service = KhoaService(db)
    success = await service.delete_khoa(ma_khoa)
    if not success:
        raise HTTPException(status_code=404, detail="Không thể xóa khoa, có thể mã này không tồn tại.")
    return {"success": success}
