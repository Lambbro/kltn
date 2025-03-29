from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import HoiDongKhoa, TVHDKhoa

class HoiDongKhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int):
        result = await self.db.execute(
            select(HoiDongKhoa).where(HoiDongKhoa.ma_hd == ma_hd)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(HoiDongKhoa))
        return result.scalars().all()

    async def create(self, hoi_dong_khoa_data: dict):
        db_hoi_dong_khoa = HoiDongKhoa(**hoi_dong_khoa_data)
        self.db.add(db_hoi_dong_khoa)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_hoi_dong_khoa)  # Làm mới dữ liệu từ DB
        return db_hoi_dong_khoa

    async def update(self, ma_hd: int, update_data: dict):
        db_hoi_dong_khoa = await self.get(ma_hd)
        if db_hoi_dong_khoa is None:
            return None
        for key, value in update_data.items():
            setattr(db_hoi_dong_khoa, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_hoi_dong_khoa)  # Làm mới dữ liệu từ DB
        return db_hoi_dong_khoa

    async def delete(self, ma_hd: int):
        db_hoi_dong_khoa = await self.get(ma_hd)
        if db_hoi_dong_khoa is None:
            return False
        await self.db.delete(db_hoi_dong_khoa)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True


class TVHDKhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int, ma_gv: str):
        result = await self.db.execute(
            select(TVHDKhoa).where(
                (TVHDKhoa.ma_hd == ma_hd) & (TVHDKhoa.ma_gv == ma_gv)
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(TVHDKhoa))
        return result.scalars().all()

    async def create(self, tvhd_khoa_data: dict):
        db_tvhd_khoa = TVHDKhoa(**tvhd_khoa_data)
        self.db.add(db_tvhd_khoa)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_tvhd_khoa)  # Làm mới dữ liệu từ DB
        return db_tvhd_khoa

    async def update(self, ma_hd: int, ma_gv: str, update_data: dict):
        db_tvhd_khoa = await self.get(ma_hd, ma_gv)
        if db_tvhd_khoa is None:
            return None
        for key, value in update_data.items():
            setattr(db_tvhd_khoa, key, value)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        await self.db.refresh(db_tvhd_khoa)  # Làm mới dữ liệu từ DB
        return db_tvhd_khoa

    async def delete(self, ma_hd: int, ma_gv: str):
        db_tvhd_khoa = await self.get(ma_hd, ma_gv)
        if db_tvhd_khoa is None:
            return False
        await self.db.delete(db_tvhd_khoa)
        await self.db.flush()  # Đẩy dữ liệu nhưng chưa commit
        return True
