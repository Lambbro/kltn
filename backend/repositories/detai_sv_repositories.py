from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import DangKyNCKH, NguyenVongDK, DeTaiNCKHSV, TaiLieuNCKHSV, NhomNCKH

#Đăng ký Repository
class DangKyNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_dk: int):
        result = await self.db.execute(select(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(DangKyNCKH).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, dang_ky_data: dict):
        db_dang_ky = DangKyNCKH(**dang_ky_data)
        self.db.add(db_dang_ky)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(db_dang_ky)  # Làm mới dữ liệu từ DB
        return db_dang_ky

    async def update(self, ma_dk: int, update_data: dict):
        db_dang_ky = await self.get(ma_dk)
        if db_dang_ky is None:
            return None
        for key, value in update_data.items():
            setattr(db_dang_ky, key, value)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(db_dang_ky)  # Làm mới dữ liệu từ DB
        return db_dang_ky

    async def delete(self, ma_dk: int):
        db_dang_ky = await self.get(ma_dk)
        if db_dang_ky is None:
            return False
        await self.db.delete(db_dang_ky)
        await self.db.flush()  # Thay commit bằng flush
        return True

#Nguyện vọng đăng ký Repository
class NguyenVongDKRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_dk: int, ma_gv: str):
        result = await self.db.execute(
            select(NguyenVongDK).where(
                (NguyenVongDK.ma_dk == ma_dk) & (NguyenVongDK.ma_gv == ma_gv)
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(NguyenVongDK))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = NguyenVongDK(**data)
        self.db.add(instance)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)  # Làm mới dữ liệu từ DB
        return instance

    async def update(self, ma_dk: int, ma_gv: str, update_data: dict):
        instance = await self.get(ma_dk, ma_gv)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)  # Làm mới dữ liệu từ DB
        return instance

    async def delete(self, ma_dk: int, ma_gv: str):
        instance = await self.get(ma_dk, ma_gv)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Thay commit bằng flush
        return True

    async def get_by_giang_vien(self, ma_gv: str):
        result = await self.db.execute(select(NguyenVongDK).where(NguyenVongDK.ma_gv == ma_gv))
        return result.scalars().all()

    async def get_by_dang_ky(self, ma_dk: int):
        result = await self.db.execute(select(NguyenVongDK).where(NguyenVongDK.ma_dk == ma_dk))
        return result.scalars().all()

    async def update_trang_thai(self, ma_dk: int, ma_gv: str, trang_thai: int):
        instance = await self.get(ma_dk, ma_gv)
        if instance is None:
            return None
        instance.trang_thai = trang_thai
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)  # Làm mới dữ liệu từ DB
        return instance

# Đề tài NCKH sinh viên Repository
class DeTaiNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int):
        result = await self.db.execute(
            select(DeTaiNCKHSV).where(DeTaiNCKHSV.ma_de_tai == ma_de_tai)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(DeTaiNCKHSV))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = DeTaiNCKHSV(**data)
        self.db.add(instance)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def update(self, ma_de_tai: int, update_data: dict):
        instance = await self.get(ma_de_tai)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def delete(self, ma_de_tai: int):
        instance = await self.get(ma_de_tai)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Thay commit bằng flush
        return True

    async def get_by_khoa(self, ma_khoa: str):
        result = await self.db.execute(select(DeTaiNCKHSV).where(DeTaiNCKHSV.ma_khoa == ma_khoa))
        return result.scalars().all()

    async def update_trang_thai(self, ma_de_tai: int, trang_thai: int):
        instance = await self.get(ma_de_tai)
        if instance:
            instance.trang_thai = trang_thai
            await self.db.flush()  # Thay commit bằng flush
            await self.db.refresh(instance)
            return instance
        return None

# TaiLieuNCKHSV Repository
class TaiLieuNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tai_lieu: int):
        result = await self.db.execute(
            select(TaiLieuNCKHSV).where(TaiLieuNCKHSV.ma_tai_lieu == ma_tai_lieu)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(TaiLieuNCKHSV))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = TaiLieuNCKHSV(**data)
        self.db.add(instance)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def update(self, ma_tai_lieu: int, update_data: dict):
        instance = await self.get(ma_tai_lieu)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def delete(self, ma_tai_lieu: int):
        instance = await self.get(ma_tai_lieu)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Thay commit bằng flush
        return True

    async def get_by_de_tai(self, ma_de_tai: int):
        result = await self.db.execute(select(TaiLieuNCKHSV).where(TaiLieuNCKHSV.ma_de_tai == ma_de_tai))
        return result.scalars().all()
    
    async def update_trang_thai(self, ma_tai_lieu: int, trang_thai: int):
        instance = await self.get(ma_tai_lieu)
        if instance:
            instance.trang_thai = trang_thai
            await self.db.flush()  # Thay commit bằng flush
            await self.db.refresh(instance)
            return instance
        return None
        
# NhomNCKH Repository
class NhomNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_nhom: int):
        result = await self.db.execute(
            select(NhomNCKH).where(NhomNCKH.ma_nhom == ma_nhom)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(NhomNCKH))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = NhomNCKH(**data)
        self.db.add(instance)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def update(self, ma_nhom: int, update_data: dict):
        instance = await self.get(ma_nhom)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Thay commit bằng flush
        await self.db.refresh(instance)
        return instance

    async def delete(self, ma_nhom: int):
        instance = await self.get(ma_nhom)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Thay commit bằng flush
        return True

    async def get_by_giang_vien(self, ma_gv: str):
        result = await self.db.execute(select(NhomNCKH).where(NhomNCKH.ma_gv == ma_gv))
        return result.scalars().all()
    
    async def get_by_de_tai(self, ma_de_tai: int):
        result = await self.db.execute(select(NhomNCKH).where(NhomNCKH.ma_de_tai == ma_de_tai))
        return result.scalars().all()