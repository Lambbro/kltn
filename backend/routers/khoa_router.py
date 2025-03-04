from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import Khoa, KhoaCreate, KhoaUpdate
from services.khoa_service import KhoaService
from typing import List

router = APIRouter(prefix="/khoa", tags=["Khoa"])

@router.get("/", response_model=List[Khoa])
def get_all_khoa(db: Session = Depends(get_db)):
    service = KhoaService(db)
    return service.get_all_khoa()

@router.get("/{ma_khoa}", response_model=Khoa)
def get_khoa(ma_khoa: str, db: Session = Depends(get_db)):
    service = KhoaService(db)
    return service.get_khoa(ma_khoa)

@router.post("/", response_model=Khoa)
def create_khoa(khoa: KhoaCreate, db: Session = Depends(get_db)):
    service = KhoaService(db)
    return service.create_khoa(khoa)

@router.put("/{ma_khoa}", response_model=Khoa)
def update_khoa(ma_khoa: str, khoa: KhoaUpdate, db: Session = Depends(get_db)):
    service = KhoaService(db)
    return service.update_khoa(ma_khoa, khoa)

@router.delete("/{ma_khoa}")
def delete_khoa(ma_khoa: str, db: Session = Depends(get_db)):
    service = KhoaService(db)
    return {"success": service.delete_khoa(ma_khoa)}