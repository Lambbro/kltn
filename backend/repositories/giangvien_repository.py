from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import GiangVien

class GiangVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_gv: str):
        result = await self.db.execute(select(GiangVien).where(GiangVien.ma_gv == ma_gv))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(GiangVien))
        return result.scalars().all()

    async def create(self, giang_vien_data: dict):
        db_giang_vien = GiangVien(**giang_vien_data)
        self.db.add(db_giang_vien)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_giang_vien)  # Làm mới dữ liệu từ DB
        return db_giang_vien

    async def update(self, ma_gv: str, update_data: dict):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return None
        for key, value in update_data.items():
            setattr(db_giang_vien, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_giang_vien)  # Làm mới dữ liệu từ DB
        return db_giang_vien

    async def delete(self, ma_gv: str):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return False
        await self.db.delete(db_giang_vien)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True
