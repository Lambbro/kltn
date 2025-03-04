import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import models
from schemas import schemas

class TaiKhoanService:
    @staticmethod
    def dang_ky(db: Session, tai_khoan: schemas.TaiKhoanCreate):
        hashed_password = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        db_tai_khoan = models.TaiKhoan(
            email=tai_khoan.email,
            mat_khau=hashed_password,
            quyen_han=tai_khoan.quyen_han
        )
        db.add(db_tai_khoan)
        try:
            db.commit()
            db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError:
            db.rollback()
            raise ValueError("Email đã tồn tại.")
    
    @staticmethod
    def dang_nhap(db: Session, email: str, mat_khau: str):
        hashed_password = hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()
        user = db.query(models.TaiKhoan).filter_by(email=email, mat_khau=hashed_password).first()
        if user:
            return user
        return None

    @staticmethod
    def get_all(db: Session):
        return db.query(models.TaiKhoan).all()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(models.TaiKhoan).filter(models.TaiKhoan.email == email).first()

    @staticmethod
    def update(db: Session, email: str, tai_khoan: schemas.TaiKhoanUpdate):
        user = db.query(models.TaiKhoan).filter(models.TaiKhoan.email == email).first()
        if not user:
            return None
        
        if tai_khoan.quyen_han is not None:
            user.quyen_han = tai_khoan.quyen_han
        
        if tai_khoan.mat_khau is not None:
            user.mat_khau = hashlib.sha256(tai_khoan.mat_khau.encode('utf-8')).hexdigest()
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, email: str):
        user = db.query(models.TaiKhoan).filter(models.TaiKhoan.email == email).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True