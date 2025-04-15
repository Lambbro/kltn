from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models

# Đề tài NCKH giảng viên repository
class DeTaiNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int):
        result = await self.db.execute(
            select(models.DeTaiNCKHGV).where(models.DeTaiNCKHGV.ma_de_tai == ma_de_tai)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DeTaiNCKHGV))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = models.DeTaiNCKHGV(**data)
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
        await self.db.flush()  # Thay commit

            
#Thành viên đề tài giảng viên schemas
class ThanhVienNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int, ma_gv: str):
        result = await self.db.execute(
            select(models.ThanhVienNCKHGV).where(
                (models.ThanhVienNCKHGV.ma_de_tai == ma_de_tai) & (models.ThanhVienNCKHGV.ma_gv == ma_gv)
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.ThanhVienNCKHGV))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = models.ThanhVienNCKHGV(**data)
        self.db.add(instance)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return instance

    async def update(self, ma_de_tai: int, ma_gv: str, update_data: dict):
        instance = await self.get(ma_de_tai, ma_gv)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return instance

    async def delete(self, ma_de_tai: int, ma_gv: str):
        instance = await self.get(ma_de_tai, ma_gv)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return True
            
#Tài liệu NCKH giảng viên schemas
class TaiLieuNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tai_lieu: int):
        result = await self.db.execute(
            select(models.TaiLieuNCKHGV).where(models.TaiLieuNCKHGV.ma_tai_lieu == ma_tai_lieu)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiLieuNCKHGV))
        return result.scalars().all()

    async def create(self, data: dict):
        instance = models.TaiLieuNCKHGV(**data)
        self.db.add(instance)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return instance

    async def update(self, ma_tai_lieu: int, update_data: dict):
        instance = await self.get(ma_tai_lieu)
        if instance is None:
            return None
        for key, value in update_data.items():
            setattr(instance, key, value)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return instance

    async def delete(self, ma_tai_lieu: int):
        instance = await self.get(ma_tai_lieu)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()  # Flush để ghi tạm thời, không commit
        return True