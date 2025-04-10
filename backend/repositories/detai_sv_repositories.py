from sqlalchemy.orm import Session
from models.base_models import DangKyNCKH, NguyenVongDK

class DangKyNCKHRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_dk_nckh(self, ma_sv: str):
        db_obj = DangKyNCKH(ma_sv=ma_sv)
        self.db.add(db_obj)
        self.db.flush()  # Chỉ flush, không commit
        return db_obj

    def get_dk_nckh(self, ma_dk: int):
        return self.db.query(DangKyNCKH).filter(DangKyNCKH.ma_dk == ma_dk).first()

    def update_dk_nckh(self, ma_dk: int, ma_sv: str):
        db_obj = self.get_dk_nckh(ma_dk)
        if db_obj:
            db_obj.ma_sv = ma_sv
            self.db.flush()
        return db_obj

    def delete_dk_nckh(self, ma_dk: int):
        db_obj = self.get_dk_nckh(ma_dk)
        if db_obj:
            self.db.delete(db_obj)
            self.db.flush()
            return True
        return False

class NguyenVongDKRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_nguyen_vong(self, ma_dk: int, ma_gv: str, muc_uu_tien: int, trang_thai: int):
        db_obj = NguyenVongDK(ma_dk=ma_dk, ma_gv=ma_gv, muc_uu_tien=muc_uu_tien, trang_thai=trang_thai)
        self.db.add(db_obj)
        self.db.flush()
        return db_obj

    def get_nguyen_vong_by_dk(self, ma_dk: int):
        return self.db.query(NguyenVongDK).filter(NguyenVongDK.ma_dk == ma_dk).all()

    def update_nguyen_vong(self, ma_dk: int, ma_gv: str, muc_uu_tien: int, trang_thai: int):
        db_obj = self.db.query(NguyenVongDK).filter(
            NguyenVongDK.ma_dk == ma_dk,
            NguyenVongDK.ma_gv == ma_gv
        ).first()
        if db_obj:
            db_obj.muc_uu_tien = muc_uu_tien
            db_obj.trang_thai = trang_thai
            self.db.flush()
        return db_obj

    def delete_nguyen_vong(self, ma_dk: int, ma_gv: str):
        db_obj = self.db.query(NguyenVongDK).filter(
            NguyenVongDK.ma_dk == ma_dk,
            NguyenVongDK.ma_gv == ma_gv
        ).first()
        if db_obj:
            self.db.delete(db_obj)
            self.db.flush()
            return True
        return False
