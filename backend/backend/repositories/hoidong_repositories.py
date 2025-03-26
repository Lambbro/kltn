from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

#Hội đồng khoa Repository
class HoiDongKhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int):
        result = await self.db.execute(
            select(models.HoiDongKhoa).where(models.HoiDongKhoa.ma_hd == ma_hd)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HoiDongKhoa))
        return result.scalars().all()

    async def create(self, hoi_dong_khoa_data: dict):
        async with self.db.begin():
            try:
                db_hoi_dong_khoa = models.HoiDongKhoa(**hoi_dong_khoa_data)
                self.db.add(db_hoi_dong_khoa)
                await self.db.flush()
                await self.db.refresh(db_hoi_dong_khoa)
                return db_hoi_dong_khoa
            except IntegrityError as e:
                raise ValueError(f"Hội đồng khoa đã tồn tại hoặc vi phạm ràng buộc dữ liệu: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo hội đồng khoa: {str(e)}")

    async def update(self, ma_hd: int, update_data: dict):
        async with self.db.begin():
            db_hoi_dong_khoa = await self.get(ma_hd)
            if db_hoi_dong_khoa is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_hoi_dong_khoa, key, value)
                await self.db.flush()
                await self.db.refresh(db_hoi_dong_khoa)
                return db_hoi_dong_khoa
            except IntegrityError as e:
                raise ValueError(f"Dữ liệu cập nhật vi phạm ràng buộc: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật hội đồng khoa: {str(e)}")

    async def delete(self, ma_hd: int):
        async with self.db.begin():
            db_hoi_dong_khoa = await self.get(ma_hd)
            if db_hoi_dong_khoa is None:
                return False
            try:
                await self.db.delete(db_hoi_dong_khoa)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa hội đồng khoa: {str(e)}")
            
#Thành viên hội đồng khoa Repository
class TVHDKhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int, ma_gv: str):
        result = await self.db.execute(
            select(models.TVHDKhoa).where(
                (models.TVHDKhoa.ma_hd == ma_hd) & (models.TVHDKhoa.ma_gv == ma_gv)
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TVHDKhoa))
        return result.scalars().all()

    async def create(self, tvhd_khoa_data: dict):
        async with self.db.begin():
            try:
                db_tvhd_khoa = models.TVHDKhoa(**tvhd_khoa_data)
                self.db.add(db_tvhd_khoa)
                await self.db.flush()
                await self.db.refresh(db_tvhd_khoa)
                return db_tvhd_khoa
            except IntegrityError as e:
                raise ValueError(f"Thành viên hội đồng khoa đã tồn tại hoặc vi phạm ràng buộc dữ liệu: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo thành viên hội đồng khoa: {str(e)}")

    async def update(self, ma_hd: int, ma_gv: str, update_data: dict):
        async with self.db.begin():
            db_tvhd_khoa = await self.get(ma_hd, ma_gv)
            if db_tvhd_khoa is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_tvhd_khoa, key, value)
                await self.db.flush()
                await self.db.refresh(db_tvhd_khoa)
                return db_tvhd_khoa
            except IntegrityError as e:
                raise ValueError(f"Dữ liệu cập nhật vi phạm ràng buộc: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật thành viên hội đồng khoa: {str(e)}")

    async def delete(self, ma_hd: int, ma_gv: str):
        async with self.db.begin():
            db_tvhd_khoa = await self.get(ma_hd, ma_gv)
            if db_tvhd_khoa is None:
                return False
            try:
                await self.db.delete(db_tvhd_khoa)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa thành viên hội đồng khoa: {str(e)}")
            
#Hội đồng trường Repository
class HoiDongTruongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hd: int):
        result = await self.db.execute(
            select(models.HoiDongTruong).where(models.HoiDongTruong.ma_hd == ma_hd)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HoiDongTruong))
        return result.scalars().all()

    async def create(self, hd_truong_data: dict):
        async with self.db.begin():
            try:
                db_hd_truong = models.HoiDongTruong(**hd_truong_data)
                self.db.add(db_hd_truong)
                await self.db.flush()
                await self.db.refresh(db_hd_truong)
                return db_hd_truong
            except IntegrityError as e:
                raise ValueError(f"Hội đồng trường đã tồn tại hoặc vi phạm ràng buộc dữ liệu: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo hội đồng trường: {str(e)}")

    async def update(self, ma_hd: int, update_data: dict):
        async with self.db.begin():
            db_hd_truong = await self.get(ma_hd)
            if db_hd_truong is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_hd_truong, key, value)
                await self.db.flush()
                await self.db.refresh(db_hd_truong)
                return db_hd_truong
            except IntegrityError as e:
                raise ValueError(f"Dữ liệu cập nhật vi phạm ràng buộc: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật hội đồng trường: {str(e)}")

    async def delete(self, ma_hd: int):
        async with self.db.begin():
            db_hd_truong = await self.get(ma_hd)
            if db_hd_truong is None:
                return False
            try:
                await self.db.delete(db_hd_truong)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa hội đồng trường: {str(e)}")
            
#Thành viên hội đồng trường Repository
class TVHDTruongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tv: int):
        result = await self.db.execute(
            select(models.TVHDTruong).where(models.TVHDTruong.ma_tv == ma_tv)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TVHDTruong))
        return result.scalars().all()

    async def create(self, tvhd_truong_data: dict):
        async with self.db.begin():
            try:
                db_tvhd_truong = models.TVHDTruong(**tvhd_truong_data)
                self.db.add(db_tvhd_truong)
                await self.db.flush()
                await self.db.refresh(db_tvhd_truong)
                return db_tvhd_truong
            except IntegrityError as e:
                raise ValueError(f"Thành viên hội đồng trường đã tồn tại hoặc vi phạm ràng buộc dữ liệu: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo thành viên hội đồng trường: {str(e)}")

    async def update(self, ma_tv: int, update_data: dict):
        async with self.db.begin():
            db_tvhd_truong = await self.get(ma_tv)
            if db_tvhd_truong is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_tvhd_truong, key, value)
                await self.db.flush()
                await self.db.refresh(db_tvhd_truong)
                return db_tvhd_truong
            except IntegrityError as e:
                raise ValueError(f"Dữ liệu cập nhật vi phạm ràng buộc: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật thành viên hội đồng trường: {str(e)}")

    async def delete(self, ma_tv: int):
        async with self.db.begin():
            db_tvhd_truong = await self.get(ma_tv)
            if db_tvhd_truong is None:
                return False
            try:
                await self.db.delete(db_tvhd_truong)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa thành viên hội đồng trường: {str(e)}")
            
