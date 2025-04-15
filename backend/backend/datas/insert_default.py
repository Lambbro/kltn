import hashlib
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, engine

import models.base_models as models
import datas.data as data

from datetime import date

# Hàm hash mật khẩu
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#Insert khoa
async def insert_khoa(session: AsyncSession):
    for khoa in data.get_list_khoa():
        session.add(models.Khoa(**khoa))
    await session.commit()

#Insert Hướng Nghiên Cứu
async def insert_huong_nc(session: AsyncSession):
    for hnc in data.get_list_hnc():
        session.add(models.HuongNghienCuu(ten_hnc=hnc))
    await session.commit()

#Insert sinh viên và tài khoản
async def insert_sinh_vien(session: AsyncSession, slg_sv=2500):
    slg = int(slg_sv/5)
    for i in range(18,23):    
        for j in range(slg):
            sv_data = data.create_sv(j+1,i)
            email = sv_data["email"]
            mat_khau = sv_data["cccd"]
            default_mat_khau = hash_password(mat_khau)
            # Tạo tài khoản trước
            tai_khoan = models.TaiKhoan(email=email, mat_khau=default_mat_khau, quyen_han=4)
            session.add(tai_khoan)
            
            # Tạo sinh viên sau khi tài khoản đã được thêm
            sinh_vien = models.SinhVien(**sv_data)
            session.add(sinh_vien)
    await session.commit()

# Insert giảng viên và tài khoản
async def insert_giang_vien(session: AsyncSession, slg_gv=250):
    for _ in range(slg_gv):
        gv_data = data.create_gv()
        email = gv_data["email"]
        
        # Tạo tài khoản trước với mật khẩu hashed
        hashed_password = hash_password(gv_data["cccd"])
        tai_khoan = models.TaiKhoan(email=email, mat_khau=hashed_password, quyen_han=3)
        session.add(tai_khoan)
        
        # Tạo giảng viên sau khi tài khoản đã được thêm
        giang_vien = models.GiangVien(**gv_data)
        session.add(giang_vien)
    
    for _ in range(50):
        gv_data = data.create_gv()
        email = gv_data["email"]
        
        # Tạo tài khoản trước với mật khẩu hashed
        hashed_password = hash_password(gv_data["cccd"])
        tai_khoan = models.TaiKhoan(email=email, mat_khau=hashed_password, quyen_han=2)
        session.add(tai_khoan)
        
        # Tạo giảng viên sau khi tài khoản đã được thêm
        giang_vien = models.GiangVien(**gv_data)
        session.add(giang_vien)

    for _ in range(5):
        gv_data = data.create_gv()
        email = gv_data["email"]
        
        # Tạo tài khoản trước với mật khẩu hashed
        hashed_password = hash_password(gv_data["cccd"])
        tai_khoan = models.TaiKhoan(email=email, mat_khau=hashed_password, quyen_han=1)
        session.add(tai_khoan)
        
        # Tạo giảng viên sau khi tài khoản đã được thêm
        giang_vien = models.GiangVien(**gv_data)
        session.add(giang_vien)

    await session.commit()

#insert admin

async def insert_admin(session: AsyncSession):
    # Dữ liệu cho giảng viên
    gv_data_list = [
        {
            "ma_gv": "ADMIN001",
            "ten_gv": "admin1",
            "cccd": "001234567890",
            "gioi_tinh": 1,
            "ngay_sinh": date(1999, 1, 1),
            "que_quan": "Hà Nội",
            "sdt": "0123456789",
            "don_vi_cong_tac": "Trường Đại học Mở Hà Nội",
            "dia_chi_cong_tac": "Hà Nội",
            "email": "admin@hou.edu.vn",
            "ma_khoa": "K07"
        },
        {
            "ma_gv": "ADMIN002",
            "ten_gv": "admin2",
            "cccd": "002234567890",
            "gioi_tinh": 0,
            "ngay_sinh": date(1985, 5, 10),
            "que_quan": "Hải Phòng",
            "sdt": "0987654321",
            "don_vi_cong_tac": "Trường Đại học Quốc gia Hà Nội",
            "dia_chi_cong_tac": "Hà Nội",
            "email": "tonckh@hou.edu.vn",
            "ma_khoa": "K07"
        },
        {
            "ma_gv": "ADMIN003",
            "ten_gv": "admin3",
            "cccd": "003234567890",
            "gioi_tinh": 1,
            "ngay_sinh": date(1990, 7, 20),
            "que_quan": "Đà Nẵng",
            "sdt": "0912345678",
            "don_vi_cong_tac": "Trường Đại học Bách khoa Hà Nội",
            "dia_chi_cong_tac": "Hà Nội",
            "email": "gv@hou.edu.vn",
            "ma_khoa": "K07"
        }
    ]

    # Tạo tài khoản và giảng viên cho mỗi người
    for gv_data in gv_data_list:
        email = gv_data["email"]
        
        # Tạo tài khoản với mật khẩu hashed cho mỗi người
        hashed_password = hash_password(gv_data["cccd"])
        tai_khoan = models.TaiKhoan(email=email, mat_khau=hashed_password, quyen_han=1)
        session.add(tai_khoan)
        
        # Tạo giảng viên cho mỗi tài khoản
        giang_vien = models.GiangVien(**gv_data)
        session.add(giang_vien)
    
    # Cam kết các thay đổi vào cơ sở dữ liệu
    await session.commit()


#Thêm khen thưởng
async def insert_khen_thuong(session: AsyncSession):
    for i in range(1, 3):
        for j in range(6):
            kt = models.KhenThuong(
                cap_do = i,
                muc_do = j
            )
            session.add(kt)
    await session.commit()

async def insert_db():
    async with AsyncSessionLocal() as session:
        try:
            await insert_khoa(session)
            await insert_huong_nc(session)
            await insert_sinh_vien(session)
            await insert_giang_vien(session)
            await insert_admin(session)
            await insert_khen_thuong(session)
        except Exception as e:
            print(e)
            await session.rollback()

async def main():
    try:
        await insert_db()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())