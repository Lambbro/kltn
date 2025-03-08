from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from services.huong_nc_service import HuongNghienCuuService
from typing import List

router = APIRouter(prefix="/huongnghiencuu", tags=["Hướng Nghiên Cứu"])

@router.get("/", response_model=List[HuongNghienCuu])
async def get_all_hnc(db: AsyncSession = Depends(get_db)):
    return await HuongNghienCuuService(db).get_all_hnc()

@router.get("/{ma_hnc}", response_model=HuongNghienCuu)
async def get_hnc(ma_hnc: int, db: AsyncSession = Depends(get_db)):
    return await HuongNghienCuuService(db).get_hnc(ma_hnc)

@router.post("/", response_model=HuongNghienCuu)
async def create_hnc(hnc_data: HuongNghienCuuCreate, db: AsyncSession = Depends(get_db)):
    return await HuongNghienCuuService(db).create_hnc(hnc_data)

@router.put("/{ma_hnc}", response_model=HuongNghienCuu)
async def update_hnc(ma_hnc: int, hnc_data: HuongNghienCuuUpdate, db: AsyncSession = Depends(get_db)):
    return await HuongNghienCuuService(db).update_hnc(ma_hnc, hnc_data)

@router.delete("/{ma_hnc}")
async def delete_hnc(ma_hnc: int, db: AsyncSession = Depends(get_db)):
    return await HuongNghienCuuService(db).delete_hnc(ma_hnc)
    