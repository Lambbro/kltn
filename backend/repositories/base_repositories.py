from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from sqlalchemy.exc import IntegrityError

#Khoa Repository
class KhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khoa: str):
       return await self.db.get(models.Khoa, ma_khoa)
    
    async def get_all(self):
        result = await self.db.execute(select(models.Khoa))
        return result.scalars().all()
    
    async def create(self, khoa_data: dict):
        db_khoa = models.Khoa(**khoa_data)
        self.db.add(db_khoa)
        await self.db.commit()
        await self.db.refresh(db_khoa)
        return db_khoa
    
    async def update(self, ma_khoa: str, update_data: dict):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return None
        for key, value in update_data.items():
            setattr(db_khoa, key, value)
        await self.db.commit()
        await self.db.refresh(db_khoa)
        return db_khoa
    
    async def delete(self, ma_khoa: str):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return False
        await self.db.delete(db_khoa)
        await self.db.commit()
        return True
    
#Hướng nghiên cứu Repository
class HuongNghienCuuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hnc: int):
        return await self.db.get(models.HuongNghienCuu, ma_hnc)
    
    async def get_all(self):
        result = await self.db.execute(select(models.HuongNghienCuu))
        return result.scalars().all()
    
    async def create(self, hnc_data: dict):
        db_hnc = models.HuongNghienCuu(**hnc_data)
        self.db.add(db_hnc)
        await self.db.commit()
        await self.db.refresh(db_hnc)
        return db_hnc
    
    async def update(self, ma_hnc: int, update_data: dict):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return None
        for key, value in update_data.items():
            setattr(db_hnc, key, value)
        await self.db.commit()
        await self.db.refresh(db_hnc)
        return db_hnc

    async def delete(self, ma_hnc: int):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return False
        await self.db.delete(db_hnc)
        await self.db.commit()
        return True
    
#Tài khoản Repository
class TaiKhoanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, email: str):
        return await self.db.get(models.TaiKhoan, email)

    async def get_all(self):
        result = await self.db.execute(select(models.TaiKhoan))
        return result.scalars().all()

    async def create(self, tai_khoan_data: dict):
        db_tai_khoan = models.TaiKhoan(**tai_khoan_data)
        self.db.add(db_tai_khoan)
        await self.db.commit()
        await self.db.refresh(db_tai_khoan)
        return db_tai_khoan

    async def update(self, email: str, update_data: dict):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return None
        for key, value in update_data.items():
            setattr(db_tai_khoan, key, value)
        await self.db.commit()
        await self.db.refresh(db_tai_khoan)
        return db_tai_khoan

    async def delete(self, email: str):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return False
        await self.db.delete(db_tai_khoan)
        await self.db.commit()
        return True

#Khen Thưởng Repository   
class KhenThuongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khen_thuong: int):
        return await self.db.get(models.KhenThuong, ma_khen_thuong)

    async def get_all(self):
        result = await self.db.execute(select(models.KhenThuong))
        return result.scalars().all()

    async def create(self, khen_thuong_data: dict):
        db_khen_thuong = models.KhenThuong(**khen_thuong_data)
        self.db.add(db_khen_thuong)
        await self.db.commit()
        await self.db.refresh(db_khen_thuong)
        return db_khen_thuong

    async def update(self, ma_khen_thuong: int, update_data: dict):
        db_khen_thuong = await self.get(ma_khen_thuong)
        if db_khen_thuong is None:
            return None
        for key, value in update_data.items():
            setattr(db_khen_thuong, key, value)
        await self.db.commit()
        await self.db.refresh(db_khen_thuong)
        return db_khen_thuong

    async def delete(self, ma_khen_thuong: int):
        db_khen_thuong = await self.get(ma_khen_thuong)
        if db_khen_thuong is None:
            return False
        await self.db.delete(db_khen_thuong)
        await self.db.commit()
        return True
    
#Sinh Viên Repository
class SinhVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sv: str):
        return await self.db.get(models.SinhVien, ma_sv)

    async def get_all(self):
        result = await self.db.execute(select(models.SinhVien))
        return result.scalars().all()

    async def create(self, sinh_vien_data: dict):
        db_sinh_vien = models.SinhVien(**sinh_vien_data)
        self.db.add(db_sinh_vien)
        await self.db.commit()
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def update(self, ma_sv: str, update_data: dict):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return None
        for key, value in update_data.items():
            setattr(db_sinh_vien, key, value)
        await self.db.commit()
        await self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    async def delete(self, ma_sv: str):
        db_sinh_vien = await self.get(ma_sv)
        if db_sinh_vien is None:
            return False
        await self.db.delete(db_sinh_vien)
        await self.db.commit()
        return True
    
#Giảng Viên Repository
class GiangVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_gv: str):
        return await self.db.get(models.GiangVien, ma_gv)

    async def get_all(self):
        result = await self.db.execute(select(models.GiangVien))
        return result.scalars().all()

    async def create(self, giang_vien_data: dict):
        db_giang_vien = models.GiangVien(**giang_vien_data)
        self.db.add(db_giang_vien)
        await self.db.commit()
        await self.db.refresh(db_giang_vien)
        return db_giang_vien

    async def update(self, ma_gv: str, update_data: dict):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return None
        for key, value in update_data.items():
            setattr(db_giang_vien, key, value)
        await self.db.commit()
        await self.db.refresh(db_giang_vien)
        return db_giang_vien

    async def delete(self, ma_gv: str):
        db_giang_vien = await self.get(ma_gv)
        if db_giang_vien is None:
            return False
        await self.db.delete(db_giang_vien)
        await self.db.commit()
        return True
