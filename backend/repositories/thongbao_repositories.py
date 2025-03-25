from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ThongBaoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, ma_tb: int):
        result = await self.db.execute(
            select(models.ThongBao).where(models.ThongBao.ma_tb == ma_tb)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(models.ThongBao))
        return result.scalars().all()

    async def create(self, thong_bao_data: dict):
        async with self.db.begin():
            try:
                db_thong_bao = models.ThongBao(**thong_bao_data)
                self.db.add(db_thong_bao)
                await self.db.flush()
                await self.db.refresh(db_thong_bao)
                return db_thong_bao
            except IntegrityError:
                raise ValueError("Thông báo đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi tạo thông báo: {str(e)}")

    async def update(self, ma_tb: int, update_data: dict):
        async with self.db.begin():
            db_thong_bao = await self.get(ma_tb)
            if db_thong_bao is None:
                return None
            try:
                for key, value in update_data.items():
                    setattr(db_thong_bao, key, value)
                await self.db.flush()
                await self.db.refresh(db_thong_bao)
                return db_thong_bao
            except IntegrityError:
                raise ValueError("Dữ liệu cập nhật vi phạm ràng buộc.")
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi cập nhật thông báo: {str(e)}")

    async def delete(self, ma_tb: int):
        async with self.db.begin():
            db_thong_bao = await self.get(ma_tb)
            if db_thong_bao is None:
                return False
            try:
                await self.db.delete(db_thong_bao)
                return True
            except SQLAlchemyError as e:
                raise RuntimeError(f"Lỗi cơ sở dữ liệu khi xóa thông báo: {str(e)}")