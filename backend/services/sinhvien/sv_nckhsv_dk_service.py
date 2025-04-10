from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select

import schemas.base_schemas as schemas
from models.base_models import DangKyNCKH, NguyenVongDK
from schemas.detai_sv_schemas import DangKyNguyenVongResponse

class SVDangKyService:
    def __init__(self, db: AsyncSession):
        self.db = db
    # LẤY ĐĂNG KÝ ĐANG THỰC HIỆN THEO MÃ SINH VIÊN (KÈM NGUYỆN VỌNG)
    async def get_by_ma_sv(self, ma_sv: str) -> Optional[DangKyNguyenVongResponse]:
        db_dk = await self.db.execute(
            select(DangKyNCKH)
            .where(DangKyNCKH.ma_sv == ma_sv, DangKyNCKH.trang_thai == 1)
        )
        db_dk = db_dk.scalars().first()

        if not db_dk:
            raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký.")

        await self.db.refresh(db_dk, ["nguyen_vong"])  # Load danh sách nguyện vọng

        return DangKyNguyenVongResponse(
            ma_dk=db_dk.ma_dk,
            ma_sv=db_dk.ma_sv,
            trang_thai=db_dk.trang_thai,
            list_nguyen_vong=[
                schemas.NguyenVongDKResponse(
                    ma_dk=nv.ma_dk,
                    ma_gv=nv.ma_gv,
                    muc_uu_tien=nv.muc_uu_tien,
                    trang_thai=nv.trang_thai
                )
                for nv in db_dk.nguyen_vong
            ]
        )
    # TẠO ĐĂNG KÝ + NGUYỆN VỌNG
    async def add(self, dang_ky: schemas.DangKyNCKHCreate, list_nguyen_vong: List[schemas.NguyenVongDKCreate]) -> dict:
        existing_dang_ky = await self.db.execute(
            select(DangKyNCKH).where(DangKyNCKH.ma_sv == dang_ky.ma_sv, DangKyNCKH.trang_thai == 1)
        )
        existing_dang_ky = existing_dang_ky.scalars().first()

        if existing_dang_ky:
            raise HTTPException(status_code=400, detail="Sinh viên đã có một đăng ký đang chờ duyệt.")
        
        if len(list_nguyen_vong) > 2:
            raise HTTPException(status_code=400, detail="Mỗi đăng ký chỉ được có tối đa 2 nguyện vọng.")
        # ❗ Thêm kiểm tra: muc_uu_tien và ma_gv không trùng nhau
        muc_uu_tien_set = set()
        ma_gv_set = set()

        for nv in list_nguyen_vong:
            if nv.muc_uu_tien in muc_uu_tien_set:
                raise HTTPException(status_code=400, detail="Mức ưu tiên không được trùng nhau.")
            if nv.ma_gv in ma_gv_set:
                raise HTTPException(status_code=400, detail="Giảng viên không được trùng nhau.")

            muc_uu_tien_set.add(nv.muc_uu_tien)
            ma_gv_set.add(nv.ma_gv)
            
        try:
            # Chuyển đổi trạng thái từ chuỗi thành số nguyên trong schema đã xử lý rồi
            db_dk = DangKyNCKH(
                ma_sv=dang_ky.ma_sv,
                trang_thai=dang_ky.trang_thai  # Trạng thái đã được xử lý trong schema
            )
            self.db.add(db_dk)
            await self.db.flush()

            # Tạo nguyện vọng và thêm vào cơ sở dữ liệu
            for nv in list_nguyen_vong:
                db_nv = NguyenVongDK(
                    ma_gv=nv.ma_gv,
                    muc_uu_tien=nv.muc_uu_tien,
                    trang_thai=nv.trang_thai,
                    ma_dk=db_dk.ma_dk
                )
                self.db.add(db_nv)

            await self.db.commit()
            await self.db.refresh(db_dk, ["nguyen_vong"])

            response_data = {
                "ma_dk": db_dk.ma_dk,
                "ma_sv": db_dk.ma_sv,
                "trang_thai": db_dk.trang_thai,
                "list_nguyen_vong": [
                    schemas.NguyenVongDKResponse(
                        ma_dk=nv.ma_dk,
                        ma_gv=nv.ma_gv,
                        muc_uu_tien=nv.muc_uu_tien,
                        trang_thai=nv.trang_thai
                    )
                    for nv in db_dk.nguyen_vong  # Lấy từ quan hệ đã lưu
                ]
            }

            return DangKyNguyenVongResponse(**response_data)

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Dữ liệu không hợp lệ hoặc bị trùng.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")

