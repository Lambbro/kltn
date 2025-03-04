from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import SinhVien, SinhVienCreate, SinhVienUpdate
from services.sinh_vien_service import SinhVienService
from typing import List

router = APIRouter(prefix="/sinh_vien", tags=["Sinh Viên"])

@router.get("/", response_model=List[SinhVien])
def get_all_sinh_vien(db: Session = Depends(get_db)):
    service = SinhVienService(db)
    return service.get_all_sinh_vien()

@router.get("/{ma_sv}", response_model=SinhVien)
def get_sinh_vien(ma_sv: str, db: Session = Depends(get_db)):
    service = SinhVienService(db)
    return service.get_sinh_vien(ma_sv)

@router.post("/", response_model=SinhVien)
def create_sinh_vien(sinh_vien: SinhVienCreate, db: Session = Depends(get_db)):
    service = SinhVienService(db)
    return service.create_sinh_vien(sinh_vien)

@router.put("/{ma_sv}", response_model=SinhVien)
def update_sinh_vien(ma_sv: str, sinh_vien: SinhVienUpdate, db: Session = Depends(get_db)):
    service = SinhVienService(db)
    return service.update_sinh_vien(ma_sv, sinh_vien)

@router.delete("/{ma_sv}")
def delete_sinh_vien(ma_sv: str, db: Session = Depends(get_db)):
    service = SinhVienService(db)
    return {"success": service.delete_sinh_vien(ma_sv)}
