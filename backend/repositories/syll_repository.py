from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import models
from schemas import syll_schemas

# HocVi Repository
class HocViRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hoc_vi: int):
        result = await self.db.execute(
            select(models.HocVi).filter(models.HocVi.ma_hoc_vi == ma_hoc_vi)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HocVi))
        return result.scalars().all()

    async def create(self, hoc_vi: syll_schemas.HocViCreate):
        db_hoc_vi = models.HocVi(**hoc_vi.model_dump())
        self.db.add(db_hoc_vi)
        await self.db.commit()
        await self.db.refresh(db_hoc_vi)
        return db_hoc_vi

    async def update(self, ma_hoc_vi: int, hoc_vi: syll_schemas.HocViUpdate):
        db_hoc_vi = await self.get(ma_hoc_vi)
        if db_hoc_vi is None:
            return None
        
        for key, value in hoc_vi.model_dump(exclude_unset=True).items():
            setattr(db_hoc_vi, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_hoc_vi)
        return db_hoc_vi

    async def delete(self, ma_hoc_vi: int):
        db_hoc_vi = await self.get(ma_hoc_vi)
        if db_hoc_vi is None:
            return False
        
        await self.db.delete(db_hoc_vi)
        await self.db.commit()
        return True


# ChucDanhKhoaHoc Repository
class ChucDanhKhoaHocRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_cdkh: int):
        result = await self.db.execute(
            select(models.ChucDanhKhoaHoc).filter(models.ChucDanhKhoaHoc.ma_cdkh == ma_cdkh)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.ChucDanhKhoaHoc))
        return result.scalars().all()

    async def create(self, chuc_danh: syll_schemas.ChucDanhKhoaHocCreate):
        db_chuc_danh = models.ChucDanhKhoaHoc(**chuc_danh.model_dump())
        self.db.add(db_chuc_danh)
        await self.db.commit()
        await self.db.refresh(db_chuc_danh)
        return db_chuc_danh

    async def update(self, ma_cdkh: int, chuc_danh: syll_schemas.ChucDanhKhoaHocUpdate):
        db_chuc_danh = await self.get(ma_cdkh)
        if db_chuc_danh is None:
            return None
        
        for key, value in chuc_danh.model_dump(exclude_unset=True).items():
            setattr(db_chuc_danh, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_chuc_danh)
        return db_chuc_danh

    async def delete(self, ma_cdkh: int):
        db_chuc_danh = await self.get(ma_cdkh)
        if db_chuc_danh is None:
            return False
        
        await self.db.delete(db_chuc_danh)
        await self.db.commit()
        return True

# TrinhDoHocVan Repository
class TrinhDoHocVanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tdhv: int):
        result = await self.db.execute(
            select(models.TrinhDoHocVan).filter(models.TrinhDoHocVan.ma_tdhv == ma_tdhv)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TrinhDoHocVan))
        return result.scalars().all()

    async def create(self, trinh_do: syll_schemas.TrinhDoHocVanCreate):
        db_trinh_do = models.TrinhDoHocVan(**trinh_do.model_dump())
        self.db.add(db_trinh_do)
        await self.db.commit()
        await self.db.refresh(db_trinh_do)
        return db_trinh_do

    async def update(self, ma_tdhv: int, trinh_do: syll_schemas.TrinhDoHocVanUpdate):
        db_trinh_do = await self.get(ma_tdhv)
        if db_trinh_do is None:
            return None
        
        for key, value in trinh_do.model_dump(exclude_unset=True).items():
            setattr(db_trinh_do, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_trinh_do)
        return db_trinh_do

    async def delete(self, ma_tdhv: int):
        db_trinh_do = await self.get(ma_tdhv)
        if db_trinh_do is None:
            return False
        
        await self.db.delete(db_trinh_do)
        await self.db.commit()
        return True


# KhoaDaoTao Repository
class KhoaDaoTaoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khoa_dao_tao: int):
        result = await self.db.execute(
            select(models.KhoaDaoTao).filter(models.KhoaDaoTao.ma_khoa_dao_tao == ma_khoa_dao_tao)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.KhoaDaoTao))
        return result.scalars().all()

    async def create(self, khoa_dao_tao: syll_schemas.KhoaDaoTaoCreate):
        db_khoa_dao_tao = models.KhoaDaoTao(**khoa_dao_tao.model_dump())
        self.db.add(db_khoa_dao_tao)
        await self.db.commit()
        await self.db.refresh(db_khoa_dao_tao)
        return db_khoa_dao_tao

    async def update(self, ma_khoa_dao_tao: int, khoa_dao_tao: syll_schemas.KhoaDaoTaoUpdate):
        db_khoa_dao_tao = await self.get(ma_khoa_dao_tao)
        if db_khoa_dao_tao is None:
            return None
        for key, value in khoa_dao_tao.model_dump(exclude_unset=True).items():
            setattr(db_khoa_dao_tao, key, value)
        await self.db.commit()
        await self.db.refresh(db_khoa_dao_tao)
        return db_khoa_dao_tao

    async def delete(self, ma_khoa_dao_tao: int):
        db_khoa_dao_tao = await self.get(ma_khoa_dao_tao)
        if db_khoa_dao_tao is None:
            return False
        await self.db.delete(db_khoa_dao_tao)
        await self.db.commit()
        return True

# TrinhDoNgoaiNgu Repository
class TrinhDoNgoaiNguRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_nn: int):
        result = await self.db.execute(
            select(models.TrinhDoNgoaiNgu).filter(models.TrinhDoNgoaiNgu.ma_nn == ma_nn)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TrinhDoNgoaiNgu))
        return result.scalars().all()

    async def create(self, trinh_do_nn: syll_schemas.TrinhDoNgoaiNguCreate):
        db_trinh_do_nn = models.TrinhDoNgoaiNgu(**trinh_do_nn.model_dump())
        self.db.add(db_trinh_do_nn)
        await self.db.commit()
        await self.db.refresh(db_trinh_do_nn)
        return db_trinh_do_nn

    async def update(self, ma_nn: int, trinh_do_nn: syll_schemas.TrinhDoNgoaiNguUpdate):
        db_trinh_do_nn = await self.get(ma_nn)
        if db_trinh_do_nn is None:
            return None
        for key, value in trinh_do_nn.model_dump(exclude_unset=True).items():
            setattr(db_trinh_do_nn, key, value)
        await self.db.commit()
        await self.db.refresh(db_trinh_do_nn)
        return db_trinh_do_nn

    async def delete(self, ma_nn: int):
        db_trinh_do_nn = await self.get(ma_nn)
        if db_trinh_do_nn is None:
            return False
        await self.db.delete(db_trinh_do_nn)
        await self.db.commit()
        return True

    
# QuaTrinhCongTac Repository
class QuaTrinhCongTacRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_qtct: int):
        result = await self.db.execute(
            select(models.QuaTrinhCongTac).filter(models.QuaTrinhCongTac.ma_qtct == ma_qtct)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.QuaTrinhCongTac))
        return result.scalars().all()

    async def create(self, qua_trinh: syll_schemas.QuaTrinhCongTacCreate):
        db_qua_trinh = models.QuaTrinhCongTac(**qua_trinh.model_dump())
        self.db.add(db_qua_trinh)
        await self.db.commit()
        await self.db.refresh(db_qua_trinh)
        return db_qua_trinh

    async def update(self, ma_qtct: int, qua_trinh: syll_schemas.QuaTrinhCongTacUpdate):
        db_qua_trinh = await self.get(ma_qtct)
        if db_qua_trinh is None:
            return None
        for key, value in qua_trinh.model_dump(exclude_unset=True).items():
            setattr(db_qua_trinh, key, value)
        await self.db.commit()
        await self.db.refresh(db_qua_trinh)
        return db_qua_trinh

    async def delete(self, ma_qtct: int):
        db_qua_trinh = await self.get(ma_qtct)
        if db_qua_trinh is None:
            return False
        await self.db.delete(db_qua_trinh)
        await self.db.commit()
        return True

# SachBaoCongNghe Repository
class SachBaoCongNgheRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sach: int):
        result = await self.db.execute(
            select(models.SachBaoCongNghe).filter(models.SachBaoCongNghe.ma_sach == ma_sach)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.SachBaoCongNghe))
        return result.scalars().all()

    async def create(self, sach: syll_schemas.SachBaoCongNgheCreate):
        db_sach = models.SachBaoCongNghe(**sach.model_dump())
        self.db.add(db_sach)
        await self.db.commit()
        await self.db.refresh(db_sach)
        return db_sach

    async def update(self, ma_sach: int, sach: syll_schemas.SachBaoCongNgheUpdate):
        db_sach = await self.get(ma_sach)
        if db_sach is None:
            return None
        for key, value in sach.model_dump(exclude_unset=True).items():
            setattr(db_sach, key, value)
        await self.db.commit()
        await self.db.refresh(db_sach)
        return db_sach

    async def delete(self, ma_sach: int):
        db_sach = await self.get(ma_sach)
        if db_sach is None:
            return False
        await self.db.delete(db_sach)
        await self.db.commit()
        return True

# PhatMinhSangChe Repository
class PhatMinhSangCheRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_pmsc: int):
        result = await self.db.execute(
            select(models.PhatMinhSangChe).filter(models.PhatMinhSangChe.ma_pmsc == ma_pmsc)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.PhatMinhSangChe))
        return result.scalars().all()

    async def create(self, phat_minh: syll_schemas.PhatMinhSangCheCreate):
        db_phat_minh = models.PhatMinhSangChe(**phat_minh.model_dump())
        self.db.add(db_phat_minh)
        await self.db.commit()
        await self.db.refresh(db_phat_minh)
        return db_phat_minh

    async def update(self, ma_pmsc: int, phat_minh: syll_schemas.PhatMinhSangCheUpdate):
        db_phat_minh = await self.get(ma_pmsc)
        if db_phat_minh is None:
            return None
        for key, value in phat_minh.model_dump(exclude_unset=True).items():
            setattr(db_phat_minh, key, value)
        await self.db.commit()
        await self.db.refresh(db_phat_minh)
        return db_phat_minh

    async def delete(self, ma_pmsc: int):
        db_phat_minh = await self.get(ma_pmsc)
        if db_phat_minh is None:
            return False
        await self.db.delete(db_phat_minh)
        await self.db.commit()
        return True

# DeTaiKHCN Repository
class DeTaiKHCNRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sp: int):
        result = await self.db.execute(
            select(models.DeTaiKHCN).filter(models.DeTaiKHCN.ma_sp == ma_sp)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.DeTaiKHCN))
        return result.scalars().all()

    async def create(self, de_tai: syll_schemas.DeTaiKHCNCreate):
        db_de_tai = models.DeTaiKHCN(**de_tai.model_dump())
        self.db.add(db_de_tai)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def update(self, ma_sp: int, de_tai: syll_schemas.DeTaiKHCNUpdate):
        db_de_tai = await self.get(ma_sp)
        if db_de_tai is None:
            return None
        for key, value in de_tai.model_dump(exclude_unset=True).items():
            setattr(db_de_tai, key, value)
        await self.db.commit()
        await self.db.refresh(db_de_tai)
        return db_de_tai

    async def delete(self, ma_sp: int):
        db_de_tai = await self.get(ma_sp)
        if db_de_tai is None:
            return False
        await self.db.delete(db_de_tai)
        await self.db.commit()
        return True

# GiaiThuongKHCN Repository
class GiaiThuongKHCNRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_giai_thuong: int):
        result = await self.db.execute(
            select(models.GiaiThuongKHCN).filter(models.GiaiThuongKHCN.ma_giai_thuong == ma_giai_thuong)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.GiaiThuongKHCN))
        return result.scalars().all()

    async def create(self, giai_thuong: syll_schemas.GiaiThuongKHCNCreate):
        db_giai_thuong = models.GiaiThuongKHCN(**giai_thuong.model_dump())
        self.db.add(db_giai_thuong)
        await self.db.commit()
        await self.db.refresh(db_giai_thuong)
        return db_giai_thuong

    async def update(self, ma_giai_thuong: int, giai_thuong: syll_schemas.GiaiThuongKHCNUpdate):
        db_giai_thuong = await self.get(ma_giai_thuong)
        if db_giai_thuong is None:
            return None
        for key, value in giai_thuong.model_dump(exclude_unset=True).items():
            setattr(db_giai_thuong, key, value)
        await self.db.commit()
        await self.db.refresh(db_giai_thuong)
        return db_giai_thuong

    async def delete(self, ma_giai_thuong: int):
        db_giai_thuong = await self.get(ma_giai_thuong)
        if db_giai_thuong is None:
            return False
        await self.db.delete(db_giai_thuong)
        await self.db.commit()
        return True


# HoatDongCaoHoc Repository
class HoatDongCaoHocRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hdch: int):
        result = await self.db.execute(
            select(models.HoatDongCaoHoc).filter(models.HoatDongCaoHoc.ma_hdch == ma_hdch)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HoatDongCaoHoc))
        return result.scalars().all()

    async def create(self, hoat_dong: syll_schemas.HoatDongCaoHocCreate):
        db_hoat_dong = models.HoatDongCaoHoc(**hoat_dong.model_dump())
        self.db.add(db_hoat_dong)
        await self.db.commit()
        await self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    async def update(self, ma_hdch: int, hoat_dong: syll_schemas.HoatDongCaoHocUpdate):
        db_hoat_dong = await self.get(ma_hdch)
        if db_hoat_dong is None:
            return None
        for key, value in hoat_dong.model_dump(exclude_unset=True).items():
            setattr(db_hoat_dong, key, value)
        await self.db.commit()
        await self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    async def delete(self, ma_hdch: int):
        db_hoat_dong = await self.get(ma_hdch)
        if db_hoat_dong is None:
            return False
        await self.db.delete(db_hoat_dong)
        await self.db.commit()
        return True

# HoatDongGiangDay Repository
class HoatDongGiangDayRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hoat_dong: int):
        result = await self.db.execute(
            select(models.HoatDongGiangDay).filter(models.HoatDongGiangDay.ma_hoat_dong == ma_hoat_dong)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HoatDongGiangDay))
        return result.scalars().all()

    async def create(self, hoat_dong: syll_schemas.HoatDongGiangDayCreate):
        db_hoat_dong = models.HoatDongGiangDay(**hoat_dong.model_dump())
        self.db.add(db_hoat_dong)
        await self.db.commit()
        await self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    async def update(self, ma_hoat_dong: int, hoat_dong: syll_schemas.HoatDongGiangDayUpdate):
        db_hoat_dong = await self.get(ma_hoat_dong)
        if db_hoat_dong is None:
            return None
        for key, value in hoat_dong.model_dump(exclude_unset=True).items():
            setattr(db_hoat_dong, key, value)
        await self.db.commit()
        await self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    async def delete(self, ma_hoat_dong: int):
        db_hoat_dong = await self.get(ma_hoat_dong)
        if db_hoat_dong is None:
            return False
        await self.db.delete(db_hoat_dong)
        await self.db.commit()
        return True
