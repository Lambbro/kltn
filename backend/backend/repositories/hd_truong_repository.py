from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import HoiDongTruong, TVHDTruong
from sqlalchemy.exc import IntegrityError, SQLAlchemyError    

# Hội đồng trường Repository
class HoiDongTruongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int):
        result = await self.db.execute(
            select(HoiDongTruong).where(HoiDongTruong.ma_hd == ma_hd)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(HoiDongTruong))
        return result.scalars().all()

    async def create(self, hd_truong_data: dict):
        db_hd_truong = HoiDongTruong(**hd_truong_data)
        self.db.add(db_hd_truong)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_hd_truong)  # Làm mới dữ liệu từ DB
        return db_hd_truong

    async def update(self, ma_hd: int, update_data: dict):
        db_hd_truong = await self.get(ma_hd)
        if db_hd_truong is None:
            return None
        for key, value in update_data.items():
            setattr(db_hd_truong, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_hd_truong)  # Làm mới dữ liệu từ DB
        return db_hd_truong

    async def delete(self, ma_hd: int):
        db_hd_truong = await self.get(ma_hd)
        if db_hd_truong is None:
            return False
        await self.db.delete(db_hd_truong)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True

# Thành viên hội đồng trường Repository
class TVHDTruongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tv: int):
        result = await self.db.execute(
            select(TVHDTruong).where(TVHDTruong.ma_tv == ma_tv)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(TVHDTruong))
        return result.scalars().all()

    async def create(self, tvhd_truong_data: dict):
        db_tvhd_truong = TVHDTruong(**tvhd_truong_data)
        self.db.add(db_tvhd_truong)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_tvhd_truong)  # Làm mới dữ liệu từ DB
        return db_tvhd_truong

    async def update(self, ma_tv: int, update_data: dict):
        db_tvhd_truong = await self.get(ma_tv)
        if db_tvhd_truong is None:
            return None
        for key, value in update_data.items():
            setattr(db_tvhd_truong, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_tvhd_truong)  # Làm mới dữ liệu từ DB
        return db_tvhd_truong

    async def delete(self, ma_tv: int):
        db_tvhd_truong = await self.get(ma_tv)
        if db_tvhd_truong is None:
            return False
        await self.db.delete(db_tvhd_truong)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True