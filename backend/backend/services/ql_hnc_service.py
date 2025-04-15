from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, distinct
from models.base_models import giangvien_hnc_table, GiangVien, HuongNghienCuu
from repositories.base_repositories import HuongNghienCuuRepository
from schemas.base_schemas import HuongNghienCuuCreate, HuongNghienCuuResponse, HuongNghienCuuUpdate

class QLHuongNghienCuuService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = HuongNghienCuuRepository(db)

    #Lấy tất cả hướng nghiên cứu
    async def get_all(self, ma_khoa: str = None) -> list[HuongNghienCuuResponse]:
        try:
            if ma_khoa:
                query = (
                    select(HuongNghienCuu).distinct()
                    .join(giangvien_hnc_table, giangvien_hnc_table.c.ma_hnc == HuongNghienCuu.ma_hnc)
                    .join(GiangVien, GiangVien.ma_gv == giangvien_hnc_table.c.ma_gv)
                    .where(GiangVien.ma_khoa == ma_khoa)
                )
                result = await self.db.execute(query)
                danh_sach_hnc = result.scalars().all() 
            else:
                danh_sach_hnc = await self.repo.get_all()
            return [HuongNghienCuuResponse.model_validate(hnc) for hnc in danh_sach_hnc]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách hướng nghiên cứu: {str(e)}")

    #Lấy thông tin hướng nghiên cứu theo mã
    async def get(self, ma_huong_nghien_cuu: int) -> HuongNghienCuuResponse:   
        try:
            huong_nghien_cuu = await self.repo.get(ma_huong_nghien_cuu)
            if huong_nghien_cuu is None:
                raise HTTPException(status_code=404, detail=f"Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
            return HuongNghienCuuResponse.model_validate(huong_nghien_cuu)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi lấy thông tin hướng nghiên cứu: {str(e)}")

    #Tạo mới hướng nghiên cứu
    async def add(self, huong_nghien_cuu_data: HuongNghienCuuCreate) -> HuongNghienCuuResponse:
        
        try:
            hnc_moi = await self.repo.create(huong_nghien_cuu_data.model_dump())
            await self.db.commit()  # ✅ Commit tại service
            return HuongNghienCuuResponse.model_validate(hnc_moi)
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Hướng nghiên cứu đã tồn tại hoặc vi phạm ràng buộc dữ liệu.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo hướng nghiên cứu: {str(e)}")

    #Cập nhật thông tin hướng nghiên cứu
    async def update(self, ma_huong_nghien_cuu: int, huong_nghien_cuu_data: HuongNghienCuuUpdate) -> HuongNghienCuuResponse:
        try:
            update_data = huong_nghien_cuu_data.model_dump(exclude_unset=True)
            hnc_cap_nhat = await self.repo.update(ma_huong_nghien_cuu, update_data)
            if hnc_cap_nhat is None:
                raise HTTPException(status_code=404, detail=f"Không thể cập nhật. Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
            await self.db.commit()  # ✅ Commit tại service
            return HuongNghienCuuResponse.model_validate(hnc_cap_nhat)
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Dữ liệu cập nhật vi phạm ràng buộc.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật hướng nghiên cứu: {str(e)}")

    #Xóa hướng nghiên cứu
    async def delete(self, ma_huong_nghien_cuu: int) -> dict:
        try:
            success = await self.repo.delete(ma_huong_nghien_cuu)
            if not success:
                raise HTTPException(status_code=404, detail=f"Không thể xóa. Hướng nghiên cứu với mã '{ma_huong_nghien_cuu}' không tồn tại.")
            await self.db.commit()  # ✅ Commit tại service
            return {"success": True, "message": "Xóa hướng nghiên cứu thành công."}
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi xóa hướng nghiên cứu: {str(e)}")
