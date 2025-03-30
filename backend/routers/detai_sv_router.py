from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import detai_sv_schemas
from typing import List
from auths.auth import get_current_user

from services.detai_sv_service import DangKyNCKHService

dtsv_router = APIRouter(
    prefix="/nckh",
    tags=["Nghiên cứu khoa học"]
)
@dtsv_router.get("/", response_model=List[detai_sv_schemas.DangKyNCKHResponse])
async def get_all(skip: int = 0, limit: int = 100, 
                  db: AsyncSession = Depends(get_db), 
                  current_user: dict = Depends(get_current_user)):
    service = DangKyNCKHService(db, current_user)
    return await service.get_all(skip, limit)

@dtsv_router.get("/{ma_dk}", response_model=detai_sv_schemas.DangKyNCKHResponse)
async def get_dk(ma_dk: int, 
                 db: AsyncSession = Depends(get_db), 
                 current_user: dict = Depends(get_current_user)):
    service = DangKyNCKHService(db, current_user)
    return await service.get(ma_dk)

@dtsv_router.post("/", response_model=detai_sv_schemas.DangKyNCKHResponse)
async def create_dk(dang_ky: detai_sv_schemas.DangKyNCKHCreate, 
                    list_nguyen_vong: List[detai_sv_schemas.NguyenVongDKCreate], 
                    db: AsyncSession = Depends(get_db), 
                    current_user: dict = Depends(get_current_user)):
    service = DangKyNCKHService(db, current_user)
    return await service.create(dang_ky, list_nguyen_vong)

@dtsv_router.put("/{ma_dk}", response_model=List[detai_sv_schemas.NguyenVongDKResponse])
async def update_dk(ma_dk: int, 
                    list_nv: List[detai_sv_schemas.NguyenVongDKUpdate], 
                    db: AsyncSession = Depends(get_db), 
                    current_user: dict = Depends(get_current_user)):
    service = DangKyNCKHService(db, current_user)
    return await service.update(ma_dk, list_nv)

@dtsv_router.delete("/{ma_dang_ky}")
async def delete_dk(ma_dk: int, 
                    db: AsyncSession = Depends(get_db), 
                    current_user: dict = Depends(get_current_user)):
    service = DangKyNCKHService(db, current_user)
    return await service.delete(ma_dk)