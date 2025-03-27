import hashlib
import asyncio

import models.models as models
import datas.data as data

from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, engine
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
        session.add(models.HuongNghienCuu(ten_huong_nc=hnc))
    await session.commit()

#Insert sinh viên và tài khoản
async def insert_sinh_vien(session: AsyncSession, slg_sv=500):
    slg = int(slg_sv/5)
    for i in range(18,23):    
        for j in range(slg):
            sv_data = data.create_sv(j+1,i)
            email = sv_data["email"]
            print(email, '\n')
            default_mat_khau = hash_password("88888888")
            # Tạo tài khoản trước
            tai_khoan = models.TaiKhoan(email=email, mat_khau=default_mat_khau, quyen_han=4)
            session.add(tai_khoan)
            
            # Tạo sinh viên sau khi tài khoản đã được thêm
            sinh_vien = models.SinhVien(**sv_data)
            session.add(sinh_vien)
    await session.commit()
    
# Insert giảng viên và tài khoản
async def insert_giang_vien(session: AsyncSession, slg_gv=50):
    for _ in range(slg_gv):
        gv_data = data.create_gv()
        email = gv_data["email"]
        
        # Tạo tài khoản trước với mật khẩu hashed
        hashed_password = hash_password("88888888")
        tai_khoan = models.TaiKhoan(email=email, mat_khau=hashed_password, quyen_han=3)
        session.add(tai_khoan)
        
        # Tạo giảng viên sau khi tài khoản đã được thêm
        giang_vien = models.GiangVien(**gv_data)
        session.add(giang_vien)
    
    await session.commit()
        
async def insert_db():
    async with AsyncSessionLocal() as session:
        try:
            await insert_khoa(session)
            await insert_huong_nc(session)
            # Thêm sinh viên và tài khoản
            await insert_sinh_vien(session, slg_sv=500) 

            # Thêm giảng viên và tài khoản
            await insert_giang_vien(session, slg_gv=50) 
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")
            await session.rollback()

async def main():
    try:
        await insert_db()
    finally:
        await engine.dispose()  # Đóng engine để giải phóng tất cả kết nối

if __name__ == "__main__":
    asyncio.run(main())