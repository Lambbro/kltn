from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import models
from schemas import nckh_schemas

# Dang Ky NCKH Repository
class DangKyNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, ma_dk: int):
        result = await self.db.execute(select(models.DangKyNCKH).filter(models.DangKyNCKH.ma_dk == ma_dk))
        return result.scalars().first()
    
    async def get_all(self):
        result = await self.db.execute(select(models.DangKyNCKH))
        return result.scalars().all()
    
    async def create(self, dang_ky: nckh_schemas.DangKyNCKHCreate):
        db_dang_ky = models.DangKyNCKH(**dang_ky.model_dump())
        self.db.add(db_dang_ky)
        await self.db.commit()
        await self.db.refresh(db_dang_ky)
        return db_dang_ky

    async def update(self, ma_dk: int, dang_ky: nckh_schemas.DangKyNCKHUpdate):
        db_dang_ky = await self.get(ma_dk)
        if db_dang_ky is None:
            return None
        for key, value in dang_ky.model_dump(exclude_unset=True).items():
            setattr(db_dang_ky, key, value)
        await self.db.commit()
        await self.db.refresh(db_dang_ky)
        return db_dang_ky

    async def delete(self, ma_dk: int):
        db_dang_ky = await self.get(ma_dk)
        if db_dang_ky is None:
            return False
        await self.db.delete(db_dang_ky)
        await self.db.commit()
        return True
    
# NguyenVongDangKyNCKH Repository
class NguyenVongDangKyNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_dk: int, ma_gv: str):
        """Lấy một nguyện vọng đăng ký theo mã đăng ký và mã giảng viên (composite key)."""
        result = await self.db.execute(select(models.NguyenVongDangKyNCKH).filter(
            models.NguyenVongDangKyNCKH.ma_dk == ma_dk,
            models.NguyenVongDangKyNCKH.ma_gv == ma_gv
        ))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.NguyenVongDangKyNCKH))
        return result.scalars().all()

    async def create(self, nguyen_vong: nckh_schemas.NguyenVongDangKyNCKHCreate, ma_dk: int):
        """Tạo một nguyện vọng đăng ký mới."""
        db_nguyen_vong = models.NguyenVongDangKyNCKH(
            ma_dk=ma_dk,
            ma_gv=nguyen_vong.ma_gv,
            muc_uu_tien=nguyen_vong.muc_uu_tien,
            trang_thai=nguyen_vong.trang_thai
        )
        self.db.add(db_nguyen_vong)
        await self.db.commit()
        await self.db.refresh(db_nguyen_vong)
        return db_nguyen_vong

    async def update(self, ma_dk: int, ma_gv: str, nguyen_vong: nckh_schemas.NguyenVongDangKyNCKHUpdate):
        """Cập nhật một nguyện vọng đăng ký hiện có."""
        db_nguyen_vong = await self.get(ma_dk, ma_gv)
        if db_nguyen_vong is None:
            return None

        for key, value in nguyen_vong.model_dump(exclude_unset=True).items():
            setattr(db_nguyen_vong, key, value)

        await self.db.commit()
        await self.db.refresh(db_nguyen_vong)
        return db_nguyen_vong

    async def delete(self, ma_dk: int, ma_gv: str):
        """Xóa một nguyện vọng đăng ký."""
        db_nguyen_vong = await self.get(ma_dk, ma_gv)
        if db_nguyen_vong is None:
            return False

        await self.db.delete(db_nguyen_vong)
        await self.db.commit()
        return True


# NhomNCKH Repository
class NhomNCKHRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_nhom: int):
        result = await self.db.execute(select(models.NhomNCKH).filter(models.NhomNCKH.ma_nhom == ma_nhom))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.NhomNCKH))
        return result.scalars().all()

    async def create(self, nhom_nckh: nckh_schemas.NhomNCKHCreate):
        db_nhom_nckh = models.NhomNCKH(**nhom_nckh.model_dump())
        self.db.add(db_nhom_nckh)
        await self.db.commit()
        await self.db.refresh(db_nhom_nckh)
        return db_nhom_nckh

    async def update(self, ma_nhom: int, nhom_nckh: nckh_schemas.NhomNCKHUpdate):
        db_nhom_nckh = await self.get(ma_nhom)
        if db_nhom_nckh is None:
            return None
        for key, value in nhom_nckh.model_dump(exclude_unset=True).items():
            setattr(db_nhom_nckh, key, value)
        await self.db.commit()
        await self.db.refresh(db_nhom_nckh)
        return db_nhom_nckh

    async def delete(self, ma_nhom: int):
        db_nhom_nckh = await self.get(ma_nhom)
        if db_nhom_nckh is None:
            return False
        await self.db.delete(db_nhom_nckh)
        await self.db.commit()
        return True
    
# DeTaiNCKHSV Repository
class DeTaiNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int):
        result = await self.db.execute(select(models.DeTaiNCKHSV).filter(models.DeTaiNCKHSV.ma_de_tai == ma_de_tai))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DeTaiNCKHSV))
        return result.scalars().all()

    async def create(self, de_tai: nckh_schemas.DeTaiNCKHSVCreate):
        db_de_tai = models.DeTaiNCKHSV(**de_tai.model_dump())
        self.db.add(db_de_tai)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def update(self, ma_de_tai: int, de_tai: nckh_schemas.DeTaiNCKHSVUpdate):
        db_de_tai = await self.get(ma_de_tai)
        if db_de_tai is None:
            return None
        for key, value in de_tai.model_dump(exclude_unset=True).items():
            setattr(db_de_tai, key, value)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def delete(self, ma_de_tai: int):
        db_de_tai = await self.get(ma_de_tai)
        if db_de_tai is None:
            return False
        await self.db.delete(db_de_tai)
        await self.db.commit()
        return True


# TaiLieuNCKHSV Repository
class TaiLieuNCKHSVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tai_lieu: int):
        result = await self.db.execute(select(models.TaiLieuNCKHSV).filter(models.TaiLieuNCKHSV.ma_tai_lieu == ma_tai_lieu))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiLieuNCKHSV))
        return result.scalars().all()

    async def create(self, tai_lieu: nckh_schemas.TaiLieuNCKHSVCreate):
        db_tai_lieu = models.TaiLieuNCKHSV(**tai_lieu.model_dump())
        self.db.add(db_tai_lieu)
        await self.db.commit()
        await self.db.refresh(db_tai_lieu)
        return db_tai_lieu

    async def update(self, ma_tai_lieu: int, tai_lieu: nckh_schemas.TaiLieuNCKHSVUpdate):
        db_tai_lieu = await self.get(ma_tai_lieu)
        if db_tai_lieu is None:
            return None
        for key, value in tai_lieu.model_dump(exclude_unset=True).items():
            setattr(db_tai_lieu, key, value)
        await self.db.commit()
        await self.db.refresh(db_tai_lieu)
        return db_tai_lieu

    async def delete(self, ma_tai_lieu: int):
        db_tai_lieu = await self.get(ma_tai_lieu)
        if db_tai_lieu is None:
            return False
        await self.db.delete(db_tai_lieu)
        await self.db.commit()
        return True
    
# DeTaiNCKHGV Repository
class DeTaiNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int):
        result = await self.db.execute(select(models.DeTaiNCKHGV).filter(models.DeTaiNCKHGV.ma_de_tai == ma_de_tai))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DeTaiNCKHGV))
        return result.scalars().all()

    async def create(self, de_tai: nckh_schemas.DeTaiNCKHGVCreate):
        db_de_tai = models.DeTaiNCKHGV(**de_tai.model_dump())
        self.db.add(db_de_tai)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def update(self, ma_de_tai: int, de_tai: nckh_schemas.DeTaiNCKHGVUpdate):
        db_de_tai = await self.get(ma_de_tai)
        if db_de_tai is None:
            return None
        for key, value in de_tai.model_dump(exclude_unset=True).items():
            setattr(db_de_tai, key, value)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def delete(self, ma_de_tai: int):
        db_de_tai = await self.get(ma_de_tai)
        if db_de_tai is None:
            return False
        await self.db.delete(db_de_tai)
        await self.db.commit()
        return True


# TaiLieuNCKHGV Repository
class TaiLieuNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tai_lieu: int):
        result = await self.db.execute(select(models.TaiLieuNCKHGV).filter(models.TaiLieuNCKHGV.ma_tai_lieu == ma_tai_lieu))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiLieuNCKHGV))
        return result.scalars().all()

    async def create(self, tai_lieu: nckh_schemas.TaiLieuNCKHGVCreate):
        db_tai_lieu = models.TaiLieuNCKHGV(**tai_lieu.model_dump())
        self.db.add(db_tai_lieu)
        await self.db.commit()
        await self.db.refresh(db_tai_lieu)
        return db_tai_lieu

    async def update(self, ma_tai_lieu: int, tai_lieu: nckh_schemas.TaiLieuNCKHGVUpdate):
        db_tai_lieu = await self.get(ma_tai_lieu)
        if db_tai_lieu is None:
            return None
        for key, value in tai_lieu.model_dump(exclude_unset=True).items():
            setattr(db_tai_lieu, key, value)
        await self.db.commit()
        await self.db.refresh(db_tai_lieu)
        return db_tai_lieu

    async def delete(self, ma_tai_lieu: int):
        db_tai_lieu = await self.get(ma_tai_lieu)
        if db_tai_lieu is None:
            return False
        await self.db.delete(db_tai_lieu)
        await self.db.commit()
        return True

# ThanhVienDeTaiNCKHGV Repository
class ThanhVienDeTaiNCKHGVRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_de_tai: int, ma_gv: str):
        result = await self.db.execute(
            select(models.ThanhVienDeTaiNCKHGV).filter(
                models.ThanhVienDeTaiNCKHGV.ma_de_tai == ma_de_tai,
                models.ThanhVienDeTaiNCKHGV.ma_gv == ma_gv
            )
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.ThanhVienDeTaiNCKHGV))
        return result.scalars().all()

    async def create(self, thanh_vien: nckh_schemas.ThanhVienDeTaiNCKHGVCreate):
        db_thanh_vien = models.ThanhVienDeTaiNCKHGV(**thanh_vien.model_dump())
        self.db.add(db_thanh_vien)
        await self.db.commit()
        await self.db.refresh(db_thanh_vien)
        return db_thanh_vien

    async def update(self, ma_de_tai: int, ma_gv: str, thanh_vien: nckh_schemas.ThanhVienDeTaiNCKHGVUpdate):
        db_thanh_vien = await self.get(ma_de_tai, ma_gv)
        if db_thanh_vien is None:
            return None
        
        for key, value in thanh_vien.model_dump(exclude_unset=True).items():
            setattr(db_thanh_vien, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_thanh_vien)
        return db_thanh_vien

    async def delete(self, ma_de_tai: int, ma_gv: str):
        db_thanh_vien = await self.get(ma_de_tai, ma_gv)
        if db_thanh_vien is None:
            return False
        
        await self.db.delete(db_thanh_vien)
        await self.db.commit()
        return True
