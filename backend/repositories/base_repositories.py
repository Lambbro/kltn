from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

#Khoa Repository
class KhoaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khoa: str):
        result = await self.db.execute(select(models.Khoa).where(models.Khoa.ma_khoa == ma_khoa))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.Khoa))
        return result.scalars().all()

    async def create(self, khoa_data: dict):
        try:
            async with self.db.begin():  # Bắt đầu transaction
                db_khoa = models.Khoa(**khoa_data)
                self.db.add(db_khoa)
                await self.db.flush()  # Đảm bảo dữ liệu được đẩy vào DB
                await self.db.refresh(db_khoa)
            return db_khoa
        except IntegrityError:
            raise ValueError("Dữ liệu vi phạm ràng buộc (ví dụ: trùng mã khoa).")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_khoa: str, update_data: dict):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return None
        try:
            async with self.db.begin():  # Transaction
                for key, value in update_data.items():
                    setattr(db_khoa, key, value)
                await self.db.flush()
                await self.db.refresh(db_khoa)
            return db_khoa
        except IntegrityError:
            raise ValueError("Dữ liệu vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def delete(self, ma_khoa: str):
        db_khoa = await self.get(ma_khoa)
        if db_khoa is None:
            return False
        try:
            async with self.db.begin():  # Transaction
                await self.db.delete(db_khoa)
                await self.db.flush()
            return True
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa: {str(e)}")

    
#Hướng nghiên cứu Repository
class HuongNghienCuuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_hnc: int):
        result = await self.db.execute(
            select(models.HuongNghienCuu).where(models.HuongNghienCuu.ma_hnc == ma_hnc)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.HuongNghienCuu))
        return result.scalars().all()

    async def create(self, hnc_data: dict):
        try:
            async with self.db.begin():  # Transaction đảm bảo tính nhất quán
                db_hnc = models.HuongNghienCuu(**hnc_data)
                self.db.add(db_hnc)
                await self.db.flush()  # Đẩy dữ liệu vào DB mà không commit ngay
                await self.db.refresh(db_hnc)  # Làm mới đối tượng sau khi flush
            return db_hnc  # Commit tự động khi rời khỏi async with
        except IntegrityError:
            raise ValueError("Dữ liệu vi phạm ràng buộc, có thể mã hướng nghiên cứu đã tồn tại.")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu: {str(e)}")

    async def update(self, ma_hnc: int, update_data: dict):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return None
        try:
            async with self.db.begin():
                for key, value in update_data.items():
                    setattr(db_hnc, key, value)
                await self.db.flush()
                await self.db.refresh(db_hnc)
            return db_hnc
        except IntegrityError:
            raise ValueError("Dữ liệu vi phạm ràng buộc khi cập nhật.")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật: {str(e)}")

    async def delete(self, ma_hnc: int):
        db_hnc = await self.get(ma_hnc)
        if db_hnc is None:
            return False
        try:
            async with self.db.begin():
                await self.db.delete(db_hnc)
            return True
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa: {str(e)}")
    
#Tài khoản Repository
class TaiKhoanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, email: str):
        result = await self.db.execute(
            select(models.TaiKhoan).where(models.TaiKhoan.email == email)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.TaiKhoan))
        return result.scalars().all()

    async def create(self, tai_khoan_data: dict):
        try:
            async with self.db.begin():  # Transaction đảm bảo tính nhất quán
                db_tai_khoan = models.TaiKhoan(**tai_khoan_data)
                self.db.add(db_tai_khoan)
                await self.db.flush()  # Đảm bảo dữ liệu được gửi vào DB
                await self.db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError:
            raise ValueError("Tài khoản đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo tài khoản: {str(e)}")

    async def update(self, email: str, update_data: dict):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return None
        try:
            async with self.db.begin():
                for key, value in update_data.items():
                    setattr(db_tai_khoan, key, value)
                await self.db.flush()
                await self.db.refresh(db_tai_khoan)
            return db_tai_khoan
        except IntegrityError:
            raise ValueError("Dữ liệu cập nhật vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật tài khoản: {str(e)}")

    async def delete(self, email: str):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return False
        try:
            async with self.db.begin():
                await self.db.delete(db_tai_khoan)
                await self.db.flush()
            return True
        except SQLAlchemyError as e:
            raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa tài khoản: {str(e)}")
class KhenThuongRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_khen_thuong: int):
        result = await self.db.execute(
            select(models.KhenThuong).where(models.KhenThuong.ma_khen_thuong == ma_khen_thuong)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.KhenThuong))
        return result.scalars().all()

    async def create(self, khen_thuong_data: dict):
        async with self.db.begin():
            try:
                db_khen_thuong = models.KhenThuong(**khen_thuong_data)
                self.db.add(db_khen_thuong)
                await self.db.flush()  # Đẩy dữ liệu vào DB mà không commit ngay
                await self.db.refresh(db_khen_thuong)
                return db_khen_thuong
            except IntegrityError:
                raise ValueError("Phần thưởng đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo khen thưởng: {str(e)}")

    async def update(self, ma_khen_thuong: int, update_data: dict):
        async with self.db.begin():
            db_khen_thuong = await self.get(ma_khen_thuong)
            if db_khen_thuong is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_khen_thuong, key, value)
                await self.db.flush()
                await self.db.refresh(db_khen_thuong)
                return db_khen_thuong
            except IntegrityError:
                raise ValueError("Dữ liệu cập nhật vi phạm ràng buộc.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật khen thưởng: {str(e)}")

    async def delete(self, ma_khen_thuong: int):
        async with self.db.begin():
            db_khen_thuong = await self.get(ma_khen_thuong)
            if db_khen_thuong is None:
                return False
            try:
                await self.db.delete(db_khen_thuong)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa khen thưởng: {str(e)}")

#Sinh Viên Repository
class SinhVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_sv: str):
        result = await self.db.execute(select(models.SinhVien).where(models.SinhVien.ma_sv == ma_sv))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.SinhVien))
        return result.scalars().all()

    async def create(self, sinh_vien_data: dict):
        async with self.db.begin():
            try:
                db_sinh_vien = models.SinhVien(**sinh_vien_data)
                self.db.add(db_sinh_vien)
                await self.db.flush()
                await self.db.refresh(db_sinh_vien)
                return db_sinh_vien
            except IntegrityError:
                raise ValueError("Sinh viên đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo sinh viên: {str(e)}")

    async def update(self, ma_sv: str, update_data: dict):
        async with self.db.begin():
            db_sinh_vien = await self.get(ma_sv)
            if db_sinh_vien is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_sinh_vien, key, value)
                await self.db.flush()
                await self.db.refresh(db_sinh_vien)
                return db_sinh_vien
            except IntegrityError:
                raise ValueError("Dữ liệu cập nhật vi phạm ràng buộc.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật sinh viên: {str(e)}")

    async def delete(self, ma_sv: str):
        async with self.db.begin():
            db_sinh_vien = await self.get(ma_sv)
            if db_sinh_vien is None:
                return False
            try:
                await self.db.delete(db_sinh_vien)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa sinh viên: {str(e)}")
                
#Giảng Viên Repository
class GiangVienRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_gv: str):
        result = await self.db.execute(select(models.GiangVien).where(models.GiangVien.ma_gv == ma_gv))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.GiangVien))
        return result.scalars().all()

    async def create(self, giang_vien_data: dict):
        async with self.db.begin():
            try:
                db_giang_vien = models.GiangVien(**giang_vien_data)
                self.db.add(db_giang_vien)
                await self.db.flush()
                await self.db.refresh(db_giang_vien)
                return db_giang_vien
            except IntegrityError:
                raise ValueError("Giảng viên đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo giảng viên: {str(e)}")

    async def update(self, ma_gv: str, update_data: dict):
        async with self.db.begin():
            db_giang_vien = await self.get(ma_gv)
            if db_giang_vien is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_giang_vien, key, value)
                await self.db.flush()
                await self.db.refresh(db_giang_vien)
                return db_giang_vien
            except IntegrityError:
                raise ValueError("Dữ liệu cập nhật vi phạm ràng buộc.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật giảng viên: {str(e)}")

    async def delete(self, ma_gv: str):
        async with self.db.begin():
            db_giang_vien = await self.get(ma_gv)
            if db_giang_vien is None:
                return False
            try:
                await self.db.delete(db_giang_vien)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa giảng viên: {str(e)}")