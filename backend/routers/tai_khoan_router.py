from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import TaiKhoan, TaiKhoanCreate, TaiKhoanUpdate
from services import tai_khoan_service

router = APIRouter(prefix="/tai_khoan", tags=["Tài Khoản"])

@router.post("/dang_ky", response_model=TaiKhoan)
def dang_ky(tai_khoan: TaiKhoanCreate, db: Session = Depends(get_db)):
    try:
        return tai_khoan_service.TaiKhoanService.dang_ky(db, tai_khoan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dang_nhap", response_model=TaiKhoan)
def dang_nhap(email: str, mat_khau: str, db: Session = Depends(get_db)):
    user = tai_khoan_service.TaiKhoanService.dang_nhap(db, email, mat_khau)
    if not user:
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")
    return user

@router.get("/", response_model=list[TaiKhoan])
def get_all(db: Session = Depends(get_db)):
    return tai_khoan_service.TaiKhoanService.get_all(db)

@router.get("/{email}", response_model=TaiKhoan)
def get_by_email(email: str, db: Session = Depends(get_db)):
    user = tai_khoan_service.TaiKhoanService.get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return user

@router.put("/{email}", response_model=TaiKhoan)
def update(email: str, tai_khoan: TaiKhoanUpdate, db: Session = Depends(get_db)):
    user = tai_khoan_service.TaiKhoanService.update(db, email, tai_khoan)
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return user

@router.delete("/{email}")
def delete(email: str, db: Session = Depends(get_db)):
    success = tai_khoan_service.TaiKhoanService.delete(db, email)
    if not success:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return {"message": "Xóa thành công"}
