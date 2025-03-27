from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import Khoa, HuongNghienCuu, KhenThuong

#Khoa Repository
class KhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khoa: str):
        result = await self.db.execute(select(Khoa).where(Khoa.ma_khoa == ma_khoa))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(Khoa))
        return result.scalars().all()

    async def create(self, khoa_data: dict):
        db_khoa = Khoa(**khoa_data)
        self.db.add(db_khoa)
        await self.db.flush()  # Chỉ flush, không commit
        return db_khoa

    async def update(self, ma_khoa: str, update_data: dict):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return None
        for key, value in update_data.items():
            setattr(db_khoa, key, value)
        await self.db.flush()  # Chỉ flush, không commit
        return db_khoa

    async def delete(self, ma_khoa: str):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return False
        await self.db.delete(db_khoa)
        await self.db.flush()  # Chỉ flush, không commit
        return True

#Hướng Nghiên Cứu Repository
class HuongNghienCuuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hnc: int):
        result = await self.db.execute(
            select(HuongNghienCuu).where(HuongNghienCuu.ma_hnc == ma_hnc)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(HuongNghienCuu))
        return result.scalars().all()

    async def create(self, hnc_data: dict):
        db_hnc = HuongNghienCuu(**hnc_data)
        self.db.add(db_hnc)
        await self.db.flush()  # Chỉ flush, không commit
        return db_hnc

    async def update(self, ma_hnc: int, update_data: dict):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return None
        for key, value in update_data.items():
            setattr(db_hnc, key, value)
        await self.db.flush()  # Chỉ flush, không commit
        return db_hnc

    async def delete(self, ma_hnc: int):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return False
        await self.db.delete(db_hnc)
        await self.db.flush()  # Chỉ flush, không commit
        return True
    
#Khen Thưởng Repository
class KhenThuongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khen_thuong: int):
        result = await self.db.execute(
            select(KhenThuong).where(KhenThuong.ma_khen_thuong == ma_khen_thuong)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(KhenThuong))
        return result.scalars().all()

    async def create(self, khen_thuong_data: dict):
        db_khen_thuong = KhenThuong(**khen_thuong_data)
        self.db.add(db_khen_thuong)
        await self.db.flush()  # Chỉ flush, không commit
        return db_khen_thuong

    async def update(self, ma_khen_thuong: int, update_data: dict):
        db_khen_thuong = await self.get(ma_khen_thuong)
        if db_khen_thuong is None:
            return None
        for key, value in update_data.items():
            setattr(db_khen_thuong, key, value)
        await self.db.flush()  # Chỉ flush, không commit
        return db_khen_thuong

    async def delete(self, ma_khen_thuong: int):
        db_khen_thuong = await self.get(ma_khen_thuong)
        if db_khen_thuong is None:
            return False
        await self.db.delete(db_khen_thuong)
        await self.db.flush()  # Chỉ flush, không commit
        return True
