from sqlalchemy.ext.asyncio import AsyncSession
from models.base_models import GiangVien, SinhVien
from sqlalchemy.future import select

#Lấy mã khoa của giảng viên theo email
async def get_ma_khoa_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(GiangVien.ma_khoa).where(GiangVien.email == email)
    )
    return result.scalars().first()

#Lấy mã giảng viên theo email
async def get_ma_gv_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(GiangVien.ma_gv).where(GiangVien.email == email)
    )
    return result.scalars().first()

#Lấy mã khoa của sinh viên theo email
async def get_ma_khoa_by_sv_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(SinhVien.ma_khoa).where(SinhVien.email == email)
    )
    return result.scalars().first()