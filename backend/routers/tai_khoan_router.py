from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.schemas import TaiKhoan, TaiKhoanCreate, TaiKhoanUpdate
from services import tai_khoan_service

router = APIRouter(prefix="/tai_khoan", tags=["Tài Khoản"])

@router.post("/dang_ky", response_model=TaiKhoan)
async def dang_ky(tai_khoan: TaiKhoanCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await tai_khoan_service.TaiKhoanService.dang_ky(db, tai_khoan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dang_nhap", response_model=TaiKhoan)
async def dang_nhap(email: str, mat_khau: str, db: AsyncSession = Depends(get_db)):
    user = await tai_khoan_service.TaiKhoanService.dang_nhap(db, email, mat_khau)
    if not user:
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")
    return user

@router.get("/", response_model=list[TaiKhoan])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await tai_khoan_service.TaiKhoanService.get_all(db)

@router.get("/{email}", response_model=TaiKhoan)
async def get_by_email(email: str, db: AsyncSession = Depends(get_db)):
    user = await tai_khoan_service.TaiKhoanService.get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return user

@router.put("/{email}", response_model=TaiKhoan)
async def update(email: str, tai_khoan: TaiKhoanUpdate, db: AsyncSession = Depends(get_db)):
    user = await tai_khoan_service.TaiKhoanService.update(db, email, tai_khoan)
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return user

@router.delete("/{email}")
async def delete(email: str, db: AsyncSession = Depends(get_db)):
    success = await tai_khoan_service.TaiKhoanService.delete(db, email)
    if not success:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    return {"message": "Xóa thành công"}
