from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from services.huong_nc_service import HuongNghienCuuService
from typing import List

router = APIRouter(prefix="/huongnghiencuu", tags=["Hướng Nghiên Cứu"])

@router.get("/", response_model=List[HuongNghienCuu])
def get_all_hnc(db: Session = Depends(get_db)):
    service = HuongNghienCuuService(db)
    return service.get_all_hnc()

@router.get("/{ma_hnc}", response_model=HuongNghienCuu)
def get_hnc(ma_hnc: int, db: Session = Depends(get_db)):
    service = HuongNghienCuuService(db)
    try:
        return service.get_hnc(ma_hnc)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/", response_model=HuongNghienCuu)
def create_hnc(hnc_data: HuongNghienCuuCreate, db: Session = Depends(get_db)):
    service = HuongNghienCuuService(db)
    return service.create_hnc(hnc_data)

@router.put("/{ma_hnc}", response_model=HuongNghienCuu)
def update_hnc(ma_hnc: int, hnc_data: HuongNghienCuuUpdate, db: Session = Depends(get_db)):
    service = HuongNghienCuuService(db)
    try:
        return service.update_hnc(ma_hnc, hnc_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{ma_hnc}", response_model=dict)
def delete_hnc(ma_hnc: int, db: Session = Depends(get_db)):
    service = HuongNghienCuuService(db)
    try:
        service.delete_hnc(ma_hnc)
        return {"message": "Xóa thành công"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))