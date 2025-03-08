from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.syll_schemas import HocVi, HocViCreate, HocViUpdate
from services.syll_service import HocViService
from typing import List

hoc_vi_router = APIRouter(prefix="/hoc_vi", tags=["Học Vị"])

@hoc_vi_router.get("/", response_model=List[HocVi])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await HocViService(db).get_all()

@hoc_vi_router.get("/{ma_hoc_vi}", response_model=HocVi)
async def get(ma_hoc_vi: int, db: AsyncSession = Depends(get_db)):
    return await HocViService(db).get(ma_hoc_vi)

@hoc_vi_router.post("/", response_model=HocVi)
async def create(hoc_vi: HocViCreate, db: AsyncSession = Depends(get_db)):
    return await HocViService(db).create(hoc_vi)

@hoc_vi_router.put("/{ma_hoc_vi}", response_model=HocVi)
async def update(ma_hoc_vi: int, hoc_vi: HocViUpdate, db: AsyncSession = Depends(get_db)):
    return await HocViService(db).update(ma_hoc_vi, hoc_vi)

@hoc_vi_router.delete("/{ma_hoc_vi}")
async def delete(ma_hoc_vi: int, db: AsyncSession = Depends(get_db)):
    return await HocViService(db).delete(ma_hoc_vi)
