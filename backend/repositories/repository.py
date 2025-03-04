from sqlalchemy.orm import Session
from models import models
from schemas import schemas

#Khoa Repository
class KhoaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, ma_khoa: str):
        return self.db.query(models.Khoa).filter(models.Khoa.ma_khoa == ma_khoa).first()
    
    def get_all(self):
        return self.db.query(models.Khoa).all()
    
    def create(self, khoa: schemas.KhoaCreate):
        """
        Tạo một bản ghi Khoa mới trong database
        Args:
            khoa là 1 schemas.KhoaCreate chứa dữ liệu của khoa cần tạo
            Returns 1 đối tượng models.Khoa đại diện cho bản ghi để lưu vào db

        """
        db_khoa = models.Khoa(**khoa.model_dump())
        """
        Thay vì dùng **khoa.dict(), dùng **khoa.model_dump()
        model_dump() có thêm các phương thức:
            include: chỉ bao gồm các trường được chỉ định
            exclude: bỏ đi các trường được chỉ định
            by_alias: sử dụng tên alias của trường thay vì tên gốc
            exclude_unset: loại trừ các trường không được set giá trị mặc định
            exclude_defaults: loại trừ các trường có giá trị mặc định
        """
        self.db.add(db_khoa)
        """
        Thêm object db_khoa vào session thông qua .add
        Session là 1 staging area nơi bạn có thể thực hiện các thay đổi với db
        """
        self.db.commit()
        """
        Commit các thay đổi vào db thông qua commit
        """
        self.db.refresh(db_khoa)
        """
        Sau khi thêm vào db thì refresh là mới đối tượng db_khoa để có giá trị được tạo tự động bởi db
        """
        return db_khoa
        """
        trả về db khoa đại diện cho bản ghi vừa được tạo
        """
    
    def update(self, ma_khoa: str, khoa: schemas.KhoaUpdate):
        db_khoa = self.get(ma_khoa)
        if db_khoa is None:
            return None
        for key, value in khoa.model_dump(exclude_unset=True).items():
            setattr(db_khoa, key, value)
        self.db.commit()
        self.db.refresh(db_khoa)
        return db_khoa
    
    def delete(self, ma_khoa: str):
        db_khoa = self.get(ma_khoa)
        if db_khoa is None:
            return False
        self.db.delete(db_khoa)
        self.db.commit()
        return True
    
#Huong Nghien Cuu Repository
class HuongNghienCuuRepository:
    def __init__ (self, db: Session):
        self.db = db
    
    def get(self, ma_huong_nc: int):
        return self.db.query(models.HuongNghienCuu).filter(models.HuongNghienCuu.ma_huong_nc == ma_huong_nc).first()
    
    def get_all(self):
        return self.db.query(models.HuongNghienCuu).all()
    
    def create(self, huong_nghien_cuu: schemas.HuongNghienCuuCreate):
        db_huong_nghien_cuu = models.HuongNghienCuu(**huong_nghien_cuu.model_dump())
        self.db.add(db_huong_nghien_cuu)
        self.db.commit()
        self.db.refresh(db_huong_nghien_cuu)
        return db_huong_nghien_cuu
    
    def update(self, ma_huong_nc: int, huong_nghien_cuu: schemas.HuongNghienCuuUpdate):
        db_huong_nghien_cuu = self.get(ma_huong_nc)
        if db_huong_nghien_cuu is None:
            return None
        for key, value in huong_nghien_cuu.model_dump(exclude_unset=True).items():
            setattr(db_huong_nghien_cuu, key, value)
        self.db.commit()
        self.db.refresh(db_huong_nghien_cuu)
        return db_huong_nghien_cuu

    def delete(self, ma_huong_nc: int):
        db_huong_nghien_cuu = self.get(ma_huong_nc)
        if db_huong_nghien_cuu is None:
            return False
        self.db.delete(db_huong_nghien_cuu)
        self.db.commit()
        return True
    
# TaiKhoan Repository
import hashlib
from sqlalchemy.exc import IntegrityError

class TaiKhoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, email: str):
        return self.db.query(models.TaiKhoan).filter(models.TaiKhoan.email == email).first()

    def get_all(self):
        return self.db.query(models.TaiKhoan).all()

    def create(self, tai_khoan: schemas.TaiKhoanCreate):
        """Tạo tài khoản mới, hash mật khẩu trước khi lưu."""
        hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        db_tai_khoan = models.TaiKhoan(
            email=tai_khoan.email,
            mat_khau=hashed_password,
            quyen_han=tai_khoan.quyen_han
        )
        self.db.add(db_tai_khoan)
        try:
            self.db.commit()
            self.db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError as e:
            self.db.rollback()  # Rollback để tránh làm hỏng session
            raise ValueError("Email đã tồn tại.") from e  # Ném ngoại lệ để endpoint xử lý

    def update(self, email: str, tai_khoan: schemas.TaiKhoanUpdate):
        """Cập nhật tài khoản, chỉ cập nhật quyền hạn và mật khẩu (nếu được cung cấp), hash mật khẩu trước khi lưu."""
        db_tai_khoan = self.get(email)
        if db_tai_khoan is None:
            return None

        if tai_khoan.quyen_han is not None:
            db_tai_khoan.quyen_han = tai_khoan.quyen_han

        if tai_khoan.mat_khau is not None:
            # Hash mật khẩu mới trước khi lưu
            hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
            db_tai_khoan.mat_khau = hashed_password

        self.db.commit()
        self.db.refresh(db_tai_khoan)
        return db_tai_khoan
    
    def update_matkhau(self, email: str, new_password: str):
        db_tai_khoan = self.get(email)
        if db_tai_khoan is None:
            return None
        
        hashed_password = hashlib.sha256(new_password.mat_khau.encode('utf-8')).hexdigest()
        db_tai_khoan.mat_khau = hashed_password
        self.db.commit()
        self.db.refresh(db_tai_khoan)
        return db_tai_khoan

    def delete(self, email: str):
        db_tai_khoan = self.get(email)
        if db_tai_khoan is None:
            return False
        self.db.delete(db_tai_khoan)
        self.db.commit()
        return True
# SinhVien Repository
class SinhVienRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_sv: str):
        return self.db.query(models.SinhVien).filter(models.SinhVien.ma_sv == ma_sv).first()

    def get_all(self):
        return self.db.query(models.SinhVien).all()

    def create(self, sinh_vien: schemas.SinhVienCreate):
        db_sinh_vien = models.SinhVien(**sinh_vien.model_dump())
        self.db.add(db_sinh_vien)
        self.db.commit()
        self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    def update(self, ma_sv: str, sinh_vien: schemas.SinhVienUpdate):
        db_sinh_vien = self.get(ma_sv)
        if db_sinh_vien is None:
            return None
        for key, value in sinh_vien.model_dump(exclude_unset=True).items():
            setattr(db_sinh_vien, key, value)
        self.db.commit()
        self.db.refresh(db_sinh_vien)
        return db_sinh_vien

    def delete(self, ma_sv: str):
        db_sinh_vien = self.get(ma_sv)
        if db_sinh_vien is None:
            return False
        self.db.delete(db_sinh_vien)
        self.db.commit()
        return True
# GiangVien Repository
class GiangVienRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ma_gv: str):
        return self.db.query(models.GiangVien).filter(models.GiangVien.ma_gv == ma_gv).first()

    def get_all(self):
        return self.db.query(models.GiangVien).all()

    def create(self, giang_vien: schemas.GiangVienCreate):
        db_giang_vien = models.GiangVien(**giang_vien.model_dump())
        self.db.add(db_giang_vien)
        self.db.commit()
        self.db.refresh(db_giang_vien)
        return db_giang_vien

    def update(self, ma_gv: str, giang_vien: schemas.GiangVienUpdate):
        db_giang_vien = self.get(ma_gv)
        if db_giang_vien is None:
            return None
        for key, value in giang_vien.model_dump(exclude_unset=True).items():
            setattr(db_giang_vien, key, value)
        self.db.commit()
        self.db.refresh(db_giang_vien)
        return db_giang_vien

    def delete(self, ma_gv: str):
        db_giang_vien = self.get(ma_gv)
        if db_giang_vien is None:
            return False
        self.db.delete(db_giang_vien)
        self.db.commit()
        return True