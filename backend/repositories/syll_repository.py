from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import syll_schemas

# HocVi Repository
class HocViRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_hoc_vi: int):
        return self.db.query(models.HocVi).filter(models.HocVi.ma_hoc_vi == ma_hoc_vi).first()

    def get_all(self):
        return self.db.query(models.HocVi).all()

    def create(self, hoc_vi: syll_schemas.HocViCreate):
        db_hoc_vi = models.HocVi(**hoc_vi.model_dump())
        self.db.add(db_hoc_vi)
        self.db.commit()
        self.db.refresh(db_hoc_vi)
        return db_hoc_vi

    def update(self, ma_hoc_vi: int, hoc_vi: syll_schemas.HocViUpdate):
        db_hoc_vi = self.get(ma_hoc_vi)
        if db_hoc_vi is None:
            return None
        for key, value in hoc_vi.model_dump(exclude_unset=True).items():
            setattr(db_hoc_vi, key, value)
        self.db.commit()
        self.db.refresh(db_hoc_vi)
        return db_hoc_vi

    def delete(self, ma_hoc_vi: int):
        db_hoc_vi = self.get(ma_hoc_vi)
        if db_hoc_vi is None:
            return False
        self.db.delete(db_hoc_vi)
        self.db.commit()
        return True

# ChucDanhKhoaHoc Repository
class ChucDanhKhoaHocRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_cdkh: int):
        return self.db.query(models.ChucDanhKhoaHoc).filter(models.ChucDanhKhoaHoc.ma_cdkh == ma_cdkh).first()

    def get_all(self):
        return self.db.query(models.ChucDanhKhoaHoc).all()

    def create(self, chuc_danh: syll_schemas.ChucDanhKhoaHocCreate):
        db_chuc_danh = models.ChucDanhKhoaHoc(**chuc_danh.model_dump())
        self.db.add(db_chuc_danh)
        self.db.commit()
        self.db.refresh(db_chuc_danh)
        return db_chuc_danh

    def update(self, ma_cdkh: int, chuc_danh: syll_schemas.ChucDanhKhoaHocUpdate):
        db_chuc_danh = self.get(ma_cdkh)
        if db_chuc_danh is None:
            return None
        for key, value in chuc_danh.model_dump(exclude_unset=True).items():
            setattr(db_chuc_danh, key, value)
        self.db.commit()
        self.db.refresh(db_chuc_danh)
        return db_chuc_danh

    def delete(self, ma_cdkh: int):
        db_chuc_danh = self.get(ma_cdkh)
        if db_chuc_danh is None:
            return False
        self.db.delete(db_chuc_danh)
        self.db.commit()
        return True

# TrinhDoHocVan Repository
class TrinhDoHocVanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_tdhv: int):
        return self.db.query(models.TrinhDoHocVan).filter(models.TrinhDoHocVan.ma_tdhv == ma_tdhv).first()

    def get_all(self):
        return self.db.query(models.TrinhDoHocVan).all()

    def create(self, trinh_do: syll_schemas.TrinhDoHocVanCreate):
        db_trinh_do = models.TrinhDoHocVan(**trinh_do.model_dump())
        self.db.add(db_trinh_do)
        self.db.commit()
        self.db.refresh(db_trinh_do)
        return db_trinh_do

    def update(self, ma_tdhv: int, trinh_do: syll_schemas.TrinhDoHocVanUpdate):
        db_trinh_do = self.get(ma_tdhv)
        if db_trinh_do is None:
            return None
        for key, value in trinh_do.model_dump(exclude_unset=True).items():
            setattr(db_trinh_do, key, value)
        self.db.commit()
        self.db.refresh(db_trinh_do)
        return db_trinh_do

    def delete(self, ma_tdhv: int):
        db_trinh_do = self.get(ma_tdhv)
        if db_trinh_do is None:
            return False
        self.db.delete(db_trinh_do)
        self.db.commit()
        return True

# KhoaDaoTao Repository
class KhoaDaoTaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_khoa_dao_tao: int):
        return self.db.query(models.KhoaDaoTao).filter(models.KhoaDaoTao.ma_khoa_dao_tao == ma_khoa_dao_tao).first()

    def get_all(self):
        return self.db.query(models.KhoaDaoTao).all()

    def create(self, khoa_dao_tao: syll_schemas.KhoaDaoTaoCreate):
        db_khoa_dao_tao = models.KhoaDaoTao(**khoa_dao_tao.model_dump())
        self.db.add(db_khoa_dao_tao)
        self.db.commit()
        self.db.refresh(db_khoa_dao_tao)
        return db_khoa_dao_tao

    def update(self, ma_khoa_dao_tao: int, khoa_dao_tao: syll_schemas.KhoaDaoTaoUpdate):
        db_khoa_dao_tao = self.get(ma_khoa_dao_tao)
        if db_khoa_dao_tao is None:
            return None
        for key, value in khoa_dao_tao.model_dump(exclude_unset=True).items():
            setattr(db_khoa_dao_tao, key, value)
        self.db.commit()
        self.db.refresh(db_khoa_dao_tao)
        return db_khoa_dao_tao

    def delete(self, ma_khoa_dao_tao: int):
        db_khoa_dao_tao = self.get(ma_khoa_dao_tao)
        if db_khoa_dao_tao is None:
            return False
        self.db.delete(db_khoa_dao_tao)
        self.db.commit()
        return True

# TrinhDoNgoaiNgu Repository
class TrinhDoNgoaiNguRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_nn: int):
        return self.db.query(models.TrinhDoNgoaiNgu).filter(models.TrinhDoNgoaiNgu.ma_nn == ma_nn).first()

    def get_all(self):
        return self.db.query(models.TrinhDoNgoaiNgu).all()

    def create(self, trinh_do_nn: syll_schemas.TrinhDoNgoaiNguCreate):
        db_trinh_do_nn = models.TrinhDoNgoaiNgu(**trinh_do_nn.model_dump())
        self.db.add(db_trinh_do_nn)
        self.db.commit()
        self.db.refresh(db_trinh_do_nn)
        return db_trinh_do_nn

    def update(self, ma_nn: int, trinh_do_nn: syll_schemas.TrinhDoNgoaiNguUpdate):
        db_trinh_do_nn = self.get(ma_nn)
        if db_trinh_do_nn is None:
            return None
        for key, value in trinh_do_nn.model_dump(exclude_unset=True).items():
            setattr(db_trinh_do_nn, key, value)
        self.db.commit()
        self.db.refresh(db_trinh_do_nn)
        return db_trinh_do_nn

    def delete(self, ma_nn: int):
        db_trinh_do_nn = self.get(ma_nn)
        if db_trinh_do_nn is None:
            return False
        self.db.delete(db_trinh_do_nn)
        self.db.commit()
        return True
    
# QuaTrinhCongTac Repository
class QuaTrinhCongTacRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_qtct: int):
        return self.db.query(models.QuaTrinhCongTac).filter(models.QuaTrinhCongTac.ma_qtct == ma_qtct).first()

    def get_all(self):
        return self.db.query(models.QuaTrinhCongTac).all()

    def create(self, qua_trinh: syll_schemas.QuaTrinhCongTacCreate):
        db_qua_trinh = models.QuaTrinhCongTac(**qua_trinh.model_dump())
        self.db.add(db_qua_trinh)
        self.db.commit()
        self.db.refresh(db_qua_trinh)
        return db_qua_trinh

    def update(self, ma_qtct: int, qua_trinh: syll_schemas.QuaTrinhCongTacUpdate):
        db_qua_trinh = self.get(ma_qtct)
        if db_qua_trinh is None:
            return None
        for key, value in qua_trinh.model_dump(exclude_unset=True).items():
            setattr(db_qua_trinh, key, value)
        self.db.commit()
        self.db.refresh(db_qua_trinh)
        return db_qua_trinh

    def delete(self, ma_qtct: int):
        db_qua_trinh = self.get(ma_qtct)
        if db_qua_trinh is None:
            return False
        self.db.delete(db_qua_trinh)
        self.db.commit()
        return True

# SachBaoCongNghe Repository
class SachBaoCongNgheRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_sach: int):
        return self.db.query(models.SachBaoCongNghe).filter(models.SachBaoCongNghe.ma_sach == ma_sach).first()

    def get_all(self):
        return self.db.query(models.SachBaoCongNghe).all()

    def create(self, sach: syll_schemas.SachBaoCongNgheCreate):
        db_sach = models.SachBaoCongNghe(**sach.model_dump())
        self.db.add(db_sach)
        self.db.commit()
        self.db.refresh(db_sach)
        return db_sach

    def update(self, ma_sach: int, sach: syll_schemas.SachBaoCongNgheUpdate):
        db_sach = self.get(ma_sach)
        if db_sach is None:
            return None
        for key, value in sach.model_dump(exclude_unset=True).items():
            setattr(db_sach, key, value)
        self.db.commit()
        self.db.refresh(db_sach)
        return db_sach

    def delete(self, ma_sach: int):
        db_sach = self.get(ma_sach)
        if db_sach is None:
            return False
        self.db.delete(db_sach)
        self.db.commit()
        return db_sach

# PhatMinhSangChe Repository
class PhatMinhSangCheRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_pmsc: int):
        return self.db.query(models.PhatMinhSangChe).filter(models.PhatMinhSangChe.ma_pmsc == ma_pmsc).first()

    def get_all(self):
        return self.db.query(models.PhatMinhSangChe).all()

    def create(self, phat_minh: syll_schemas.PhatMinhSangCheCreate):
        db_phat_minh = models.PhatMinhSangChe(**phat_minh.model_dump())
        self.db.add(db_phat_minh)
        self.db.commit()
        self.db.refresh(db_phat_minh)
        return db_phat_minh

    def update(self, ma_pmsc: int, phat_minh: syll_schemas.PhatMinhSangCheUpdate):
        db_phat_minh = self.get(ma_pmsc)
        if db_phat_minh is None:
            return None
        for key, value in phat_minh.model_dump(exclude_unset=True).items():
            setattr(db_phat_minh, key, value)
        self.db.commit()
        self.db.refresh(db_phat_minh)
        return db_phat_minh

    def delete(self, ma_pmsc: int):
        db_phat_minh = self.get(ma_pmsc)
        if db_phat_minh is None:
            return False
        self.db.delete(db_phat_minh)
        self.db.commit()
        return db_phat_minh

# DeTaiKHCN Repository
class DeTaiKHCNRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_sp: int):
        return self.db.query(models.DeTaiKHCN).filter(models.DeTaiKHCN.ma_sp == ma_sp).first()

    def get_all(self):
        return self.db.query(models.DeTaiKHCN).all()

    def create(self, de_tai: syll_schemas.DeTaiKHCNCreate):
        db_de_tai = models.DeTaiKHCN(**de_tai.model_dump())
        self.db.add(db_de_tai)
        self.db.commit()
        self.db.refresh(db_de_tai)
        return db_de_tai

    def update(self, ma_sp: int, de_tai: syll_schemas.DeTaiKHCNUpdate):
        db_de_tai = self.get(ma_sp)
        if db_de_tai is None:
            return None
        for key, value in de_tai.model_dump(exclude_unset=True).items():
            setattr(db_de_tai, key, value)
        self.db.commit()
        self.db.refresh(db_de_tai)
        return db_de_tai

    def delete(self, ma_sp: int):
        db_de_tai = self.get(ma_sp)
        if db_de_tai is None:
            return False
        self.db.delete(db_de_tai)
        self.db.commit()
        return db_de_tai

# GiaiThuongKHCN Repository
class GiaiThuongKHCNRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_giai_thuong: int):
        return self.db.query(models.GiaiThuongKHCN).filter(models.GiaiThuongKHCN.ma_giai_thuong == ma_giai_thuong).first()

    def get_all(self):
        return self.db.query(models.GiaiThuongKHCN).all()

    def create(self, giai_thuong: syll_schemas.GiaiThuongKHCNCreate):
        db_giai_thuong = models.GiaiThuongKHCN(**giai_thuong.model_dump())
        self.db.add(db_giai_thuong)
        self.db.commit()
        self.db.refresh(db_giai_thuong)
        return db_giai_thuong

    def update(self, ma_giai_thuong: int, giai_thuong: syll_schemas.GiaiThuongKHCNUpdate):
        db_giai_thuong = self.get(ma_giai_thuong)
        if db_giai_thuong is None:
            return None
        for key, value in giai_thuong.model_dump(exclude_unset=True).items():
            setattr(db_giai_thuong, key, value)
        self.db.commit()
        self.db.refresh(db_giai_thuong)
        return db_giai_thuong

    def delete(self, ma_giai_thuong: int):
        db_giai_thuong = self.get(ma_giai_thuong)
        if db_giai_thuong is None:
            return False
        self.db.delete(db_giai_thuong)
        self.db.commit()
        return db_giai_thuong

# HoatDongCaoHoc Repository
class HoatDongCaoHocRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_hdch: int):
        return self.db.query(models.HoatDongCaoHoc).filter(models.HoatDongCaoHoc.ma_hdch == ma_hdch).first()

    def get_all(self):
        return self.db.query(models.HoatDongCaoHoc).all()

    def create(self, hoat_dong: syll_schemas.HoatDongCaoHocCreate):
        db_hoat_dong = models.HoatDongCaoHoc(**hoat_dong.model_dump())
        self.db.add(db_hoat_dong)
        self.db.commit()
        self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    def update(self, ma_hdch: int, hoat_dong: syll_schemas.HoatDongCaoHocUpdate):
        db_hoat_dong = self.get(ma_hdch)
        if db_hoat_dong is None:
            return None
        for key, value in hoat_dong.model_dump(exclude_unset=True).items():
            setattr(db_hoat_dong, key, value)
        self.db.commit()
        self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    def delete(self, ma_hdch: int):
        db_hoat_dong = self.get(ma_hdch)
        if db_hoat_dong is None:
            return False
        self.db.delete(db_hoat_dong)
        self.db.commit()
        return db_hoat_dong

# HoatDongGiangDay Repository
class HoatDongGiangDayRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_hoat_dong: int):
        return self.db.query(models.HoatDongGiangDay).filter(models.HoatDongGiangDay.ma_hoat_dong == ma_hoat_dong).first()

    def get_all(self):
        return self.db.query(models.HoatDongGiangDay).all()

    def create(self, hoat_dong: syll_schemas.HoatDongGiangDayCreate):
        db_hoat_dong = models.HoatDongGiangDay(**hoat_dong.model_dump())
        self.db.add(db_hoat_dong)
        self.db.commit()
        self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    def update(self, ma_hoat_dong: int, hoat_dong: syll_schemas.HoatDongGiangDayUpdate):
        db_hoat_dong = self.get(ma_hoat_dong)
        if db_hoat_dong is None:
            return None
        for key, value in hoat_dong.model_dump(exclude_unset=True).items():
            setattr(db_hoat_dong, key, value)
        self.db.commit()
        self.db.refresh(db_hoat_dong)
        return db_hoat_dong

    def delete(self, ma_hoat_dong: int):
        db_hoat_dong = self.get(ma_hoat_dong)
        if db_hoat_dong is None:
            return False
        self.db.delete(db_hoat_dong)
        self.db.commit()
        return db_hoat_dong