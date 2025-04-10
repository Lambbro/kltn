from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import SinhVien

class SinhVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sv: str):
        result = await self.db.execute(select(SinhVien).where(SinhVien.ma_sv == ma_sv))
        return result.scalars().first()
    
    async def khoa_get(self, ma_sv:str, ma_khoa: str):
        result = await self.db.execute(
            select(SinhVien).where(SinhVien.ma_khoa == ma_khoa and SinhVien.ma_sv == ma_sv)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(SinhVien).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def khoa_get_all(self, ma_khoa:str, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(SinhVien).where(SinhVien.ma_khoa == ma_khoa).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_all_by_khoa(self, ma_khoa: str, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(SinhVien).where(SinhVien.ma_khoa == ma_khoa).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, sinh_vien_data: dict):
        db_sinh_vien = SinhVien(**sinh_vien_data)
        self.db.add(db_sinh_vien)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def update(self, ma_sv: str, update_data: dict):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return None
        for key, value in update_data.items():
            setattr(db_sinh_vien, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def delete(self, ma_sv: str):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return False
        await self.db.delete(db_sinh_vien)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True
