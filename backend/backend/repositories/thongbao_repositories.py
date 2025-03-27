from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base_models import ThongBao
class ThongBaoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tb: int):
        result = await self.db.execute(
            select(ThongBao).where(ThongBao.ma_tb == ma_tb)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(ThongBao))
        return result.scalars().all()

    async def create(self, thong_bao_data: dict):
        db_thong_bao = ThongBao(**thong_bao_data)
        self.db.add(db_thong_bao)
        await self.db.flush()  # Chỉ flush, không commit
        await self.db.refresh(db_thong_bao)  # Làm mới dữ liệu từ DB
        return db_thong_bao

    async def update(self, ma_tb: int, update_data: dict):
        db_thong_bao = await self.get(ma_tb)
        if db_thong_bao is None:
            return None
        for key, value in update_data.items():
            setattr(db_thong_bao, key, value)
        await self.db.flush()  # Chỉ flush, không commit
        await self.db.refresh(db_thong_bao)  # Làm mới dữ liệu từ DB
        return db_thong_bao

    async def delete(self, ma_tb: int):
        db_thong_bao = await self.get(ma_tb)
        if db_thong_bao is None:
            return False
        await self.db.delete(db_thong_bao)
        await self.db.flush()  # Không cần try-except hay rollback
        return True
