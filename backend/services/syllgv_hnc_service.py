from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from typing import List
from models.base_models import giangvien_hnc_table, GiangVien, HuongNghienCuu
from schemas.base_schemas import GiangVienResponse, HuongNghienCuuResponse
from schemas.detai_sv_schemas import HNCvaGV

class SYLLHuongNghienCuuService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_giangvien_exists(self, ma_gv: str):
        gv = await self.db.get(GiangVien, ma_gv)
        if not gv:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")

    async def _check_huongnghiencuu_exists(self, ma_hnc: int):
        hnc = await self.db.get(HuongNghienCuu, ma_hnc)
        if not hnc:
            raise HTTPException(status_code=404, detail="Hướng nghiên cứu không tồn tại")

    async def add(self, ma_gv: str, ma_hnc: int, mgv: str):
        if mgv != ma_gv:
            raise HTTPException(status_code=403, detail=f"Bạn không có quyền truy cập {ma_gv} và {mgv}")

        await self._check_giangvien_exists(ma_gv=ma_gv)
        await self._check_huongnghiencuu_exists(ma_hnc=ma_hnc)

        # Kiểm tra xem bản ghi đã tồn tại chưa
        check_query = select(giangvien_hnc_table).where(
            (giangvien_hnc_table.c.ma_gv == ma_gv) &
            (giangvien_hnc_table.c.ma_hnc == ma_hnc)
        )
        result = await self.db.execute(check_query)
        existing = result.first()

        if existing:
            raise HTTPException(status_code=400, detail="Giảng viên đã có hướng nghiên cứu này")

        # Nếu chưa tồn tại, thì thêm mới
        query = insert(giangvien_hnc_table).values(ma_gv=ma_gv, ma_hnc=ma_hnc)

        try:
            await self.db.execute(query)
            await self.db.commit()
            return {"message": "Thêm hướng nghiên cứu cho giảng viên thành công"}
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Lỗi ràng buộc dữ liệu. Kiểm tra lại.")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi thêm: {str(e)}")
    
    async def delete(self, ma_gv: str, ma_hnc: int, mgv: str):
        query = delete(giangvien_hnc_table).where(
            giangvien_hnc_table.c.ma_gv == ma_gv,
            giangvien_hnc_table.c.ma_hnc == ma_hnc
        )
        result = await self.db.execute(query)
        await self.db.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu để xóa")
        
    async def get_hnc_by_gv(self, ma_gv: str):
        await self._check_giangvien_exists(ma_gv=ma_gv)

        query = (
            select(HuongNghienCuu)
            .join(giangvien_hnc_table)
            .where(giangvien_hnc_table.c.ma_gv == ma_gv)
        )
        try:
            result = await self.db.execute(query)
            hncs = result.scalars().all()
            response_data = [HuongNghienCuuResponse.model_validate(hnc) for hnc in hncs]
            if not hncs:
                raise HTTPException(status_code=404, detail="Không có dữ liệu hướng nghiên cứu theo giảng viên này")
            return response_data
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn CSDL: {str(e)}")
        
    async def get_gv_by_hnc(self, ma_hnc: int):
        await self._check_huongnghiencuu_exists(ma_hnc)

        query = (
            select(GiangVien)
            .join(giangvien_hnc_table)
            .where(giangvien_hnc_table.c.ma_hnc == ma_hnc)
        )
        try:
            result = await self.db.execute(query)
            giangviens = result.scalars().all()
            response_data = [GiangVienResponse.model_validate(gv) for gv in giangviens]
            if not giangviens:
                raise HTTPException(status_code=404, detail="Không có dữ liệu giảng viên theo hướng nghiên cứu này")
            return response_data
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn CSDL: {str(e)}")
    
    # async def get_all_hnc_gv(self, ma_khoa: str = None) -> List[HNCvaGV]:
    #     try:
    #         if ma_khoa:
    #             query = (
    #                 select(HuongNghienCuu)
    #                 .distinct()
    #                 .join(giangvien_hnc_table, giangvien_hnc_table.c.ma_hnc == HuongNghienCuu.ma_hnc)
    #                 .join(GiangVien, GiangVien.ma_gv == giangvien_hnc_table.c.ma_gv)
    #                 .where(GiangVien.ma_khoa == ma_khoa)
    #             )
    #         else:
    #             query = select(HuongNghienCuu).distinct()

    #         result = await self.db.execute(query)
    #         ds_hnc = result.scalars().all()