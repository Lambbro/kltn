from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import base_models as models
from sqlalchemy.future import select

async def verify_permission(
    db: AsyncSession = Depends(get_db), 
    user_email: str = None,  # Email của người dùng cần xác thực
    required_permission: int = 1  # Quyền tối thiểu cần thiết để truy cập route
):
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bạn chưa đăng nhập")
    
    query = select(models.TaiKhoan).where(models.TaiKhoan.email == user_email)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None or user.quyen_han > required_permission:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền truy cập")
    
    return user
