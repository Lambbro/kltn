from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from services.huong_nc_service import HuongNghienCuuService
from typing import List

router = APIRouter(prefix="/huongnghiencuu", tags=["Hướng Nghiên Cứu"])

@router.get("/", response_model=List[HuongNghienCuu])
async def get_all_hnc(db: AsyncSession = Depends(get_db)):
    service = HuongNghienCuuService(db)
    return await service.get_all_hnc()

@router.get("/{ma_hnc}", response_model=HuongNghienCuu)
async def get_hnc(ma_hnc: int, db: AsyncSession = Depends(get_db)):
    service = HuongNghienCuuService(db)
    hnc = await service.get_hnc(ma_hnc)
    if not hnc:
        raise HTTPException(status_code=404, detail="Hướng Nghiên Cứu không tồn tại")
    return hnc

@router.post("/", response_model=HuongNghienCuu)
async def create_hnc(hnc_data: HuongNghienCuuCreate, db: AsyncSession = Depends(get_db)):
    service = HuongNghienCuuService(db)
    return await service.create_hnc(hnc_data)

@router.put("/{ma_hnc}", response_model=HuongNghienCuu)
async def update_hnc(ma_hnc: int, hnc_data: HuongNghienCuuUpdate, db: AsyncSession = Depends(get_db)):
    service = HuongNghienCuuService(db)
    updated_hnc = await service.update_hnc(ma_hnc, hnc_data)
    if not updated_hnc:
        raise HTTPException(status_code=404, detail="Không thể cập nhật, có thể mã này không tồn tại")
    return updated_hnc

@router.delete("/{ma_hnc}")
async def delete_hnc(ma_hnc: int, db: AsyncSession = Depends(get_db)):
    service = HuongNghienCuuService(db)
    success = await service.delete_hnc(ma_hnc)
    if not success:
        raise HTTPException(status_code=404, detail="Không thể xóa, có thể mã này không tồn tại")
    return {"message": "Xóa thành công"}
