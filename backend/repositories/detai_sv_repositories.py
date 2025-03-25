from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

#Đăng ký Repository
class DangKyNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_dk: int):
        result = await self.db.execute(select(models.DangKyNCKH).where(models.DangKyNCKH.ma_dk == ma_dk))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DangKyNCKH))
        return result.scalars().all()

    async def create(self, dang_ky_data: dict):
        async with self.db.begin():
            try:
                db_dang_ky = models.DangKyNCKH(**dang_ky_data)
                self.db.add(db_dang_ky)
                await self.db.flush()
                await self.db.refresh(db_dang_ky)
                return db_dang_ky
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi tạo đăng ký NCKH: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_dk: int, update_data: dict):
        async with self.db.begin():
            db_dang_ky = await self.get(ma_dk)
            if db_dang_ky is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_dang_ky, key, value)
                await self.db.flush()
                await self.db.refresh(db_dang_ky)
                return db_dang_ky
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi cập nhật đăng ký NCKH: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_dk: int):
        async with self.db.begin():
            db_dang_ky = await self.get(ma_dk)
            if db_dang_ky is None:
                return False
            try:
                await self.db.delete(db_dang_ky)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

#Nguyện vọng đăng ký Repository
class NguyenVongDKRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_dk: int, ma_gv: str):
        result = await self.db.execute(
            select(models.NguyenVongDK).where(
                (models.NguyenVongDK.ma_dk == ma_dk) & (models.NguyenVongDK.ma_gv == ma_gv)
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.NguyenVongDK))
        return result.scalars().all()

    async def create(self, data: dict):
        async with self.db.begin():
            try:
                instance = models.NguyenVongDK(**data)
                self.db.add(instance)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi tạo NguyenVongDK: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_dk: int, ma_gv: str, update_data: dict):
        async with self.db.begin():
            instance = await self.get(ma_dk, ma_gv)
            if instance is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(instance, key, value)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi cập nhật NguyenVongDK: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_dk: int, ma_gv: str):
        async with self.db.begin():
            instance = await self.get(ma_dk, ma_gv)
            if instance is None:
                return False
            try:
                await self.db.delete(instance)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")
            
    async def get_by_giang_vien(self, ma_gv: str):
        result = await self.db.execute(select(models.NguyenVongDK).where(models.NguyenVongDK.ma_gv == ma_gv))
        return result.scalars().all()
    
    async def get_by_dang_ky(self, ma_dk: int):
        result = await self.db.execute(select(models.NguyenVongDK).where(models.NguyenVongDK.ma_dk == ma_dk))
        return result.scalars().all()
    
    async def update_trang_thai(self, ma_dk: int, ma_gv: str, trang_thai: int):
        async with self.db.begin():
            instance = await self.get(ma_dk, ma_gv)
            if instance:
                instance.trang_thai = trang_thai
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            return None
#Đề tài NCKH sinh viên Repository
class DeTaiNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int):
        result = await self.db.execute(
            select(models.DeTaiNCKHSV).where(models.DeTaiNCKHSV.ma_de_tai == ma_de_tai)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DeTaiNCKHSV))
        return result.scalars().all()

    async def create(self, data: dict):
        async with self.db.begin():
            try:
                instance = models.DeTaiNCKHSV(**data)
                self.db.add(instance)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi tạo DeTaiNCKHSV: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_de_tai: int, update_data: dict):
        async with self.db.begin():
            instance = await self.get(ma_de_tai)
            if instance is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(instance, key, value)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi cập nhật DeTaiNCKHSV: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_de_tai: int):
        async with self.db.begin():
            instance = await self.get(ma_de_tai)
            if instance is None:
                return False
            try:
                await self.db.delete(instance)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def get_by_khoa(self, ma_khoa: str):
        result = await self.db.execute(select(models.DeTaiNCKHSV).where(models.DeTaiNCKHSV.ma_khoa == ma_khoa))
        return result.scalars().all()
    
    async def update_trang_thai(self, ma_de_tai: int, trang_thai: int):
        async with self.db.begin():
            instance = await self.get(ma_de_tai)
            if instance:
                instance.trang_thai = trang_thai
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            return None
        
class TaiLieuNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tai_lieu: int):
        result = await self.db.execute(
            select(models.TaiLieuNCKHSV).where(models.TaiLieuNCKHSV.ma_tai_lieu == ma_tai_lieu)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiLieuNCKHSV))
        return result.scalars().all()

    async def create(self, data: dict):
        async with self.db.begin():
            try:
                instance = models.TaiLieuNCKHSV(**data)
                self.db.add(instance)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi tạo TaiLieuNCKHSV: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_tai_lieu: int, update_data: dict):
        async with self.db.begin():
            instance = await self.get(ma_tai_lieu)
            if instance is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(instance, key, value)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi cập nhật TaiLieuNCKHSV: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_tai_lieu: int):
        async with self.db.begin():
            instance = await self.get(ma_tai_lieu)
            if instance is None:
                return False
            try:
                await self.db.delete(instance)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def get_by_de_tai(self, ma_de_tai: int):
        result = await self.db.execute(select(models.TaiLieuNCKHSV).where(models.TaiLieuNCKHSV.ma_de_tai == ma_de_tai))
        return result.scalars().all()
    
    async def update_trang_thai(self, ma_tai_lieu: int, trang_thai: int):
        async with self.db.begin():
            instance = await self.get(ma_tai_lieu)
            if instance:
                instance.trang_thai = trang_thai
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            return None
        
#Nhóm NCKH Repository
class NhomNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_nhom: int):
        result = await self.db.execute(
            select(models.NhomNCKH).where(models.NhomNCKH.ma_nhom == ma_nhom)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.NhomNCKH))
        return result.scalars().all()

    async def create(self, data: dict):
        async with self.db.begin():
            try:
                instance = models.NhomNCKH(**data)
                self.db.add(instance)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi tạo NhomNCKH: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_nhom: int, update_data: dict):
        async with self.db.begin():
            instance = await self.get(ma_nhom)
            if instance is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(instance, key, value)
                await self.db.flush()
                await self.db.refresh(instance)
                return instance
            except IntegrityError as e:
                raise ValueError(f"Lỗi khi cập nhật NhomNCKH: {str(e)}")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_nhom: int):
        async with self.db.begin():
            instance = await self.get(ma_nhom)
            if instance is None:
                return False
            try:
                await self.db.delete(instance)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def get_by_giang_vien(self, ma_gv: str):
        result = await self.db.execute(select(models.NhomNCKH).where(models.NhomNCKH.ma_gv == ma_gv))
        return result.scalars().all()
    
    async def get_by_de_tai(self, ma_de_tai: int):
        result = await self.db.execute(select(models.NhomNCKH).where(models.NhomNCKH.ma_de_tai == ma_de_tai))
        return result.scalars().all()