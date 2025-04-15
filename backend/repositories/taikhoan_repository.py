from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import TaiKhoan

# Tài khoản Repository
class TaiKhoanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, email: str):
        result = await self.db.execute(
            select(TaiKhoan).where(TaiKhoan.email == email)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(TaiKhoan))
        return result.scalars().all()

    async def create(self, tai_khoan_data: dict):
        db_tai_khoan = TaiKhoan(**tai_khoan_data)
        self.db.add(db_tai_khoan)
        await self.db.flush()  # Chỉ flush, không commit
        await self.db.refresh(db_tai_khoan)  # Làm mới dữ liệu từ DB
        return db_tai_khoan

    async def update(self, email: str, update_data: dict):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return None
        for key, value in update_data.items():
            setattr(db_tai_khoan, key, value)
        await self.db.flush()  # Chỉ flush, không commit
        await self.db.refresh(db_tai_khoan)  # Làm mới dữ liệu từ DB
        return db_tai_khoan

    async def delete(self, email: str):
        db_tai_khoan = await self.get(email)
        if db_tai_khoan is None:
            return False
        await self.db.delete(db_tai_khoan)
        await self.db.flush()  # Không cần try-except hay rollback
        return True
