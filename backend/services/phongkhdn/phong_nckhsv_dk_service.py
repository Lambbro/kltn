from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import joinedload

import schemas.base_schemas as schemas
from models.base_models import DangKyNCKH, NguyenVongDK
from schemas.detai_sv_schemas import DangKyNguyenVongResponse

class PhongDangKyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================== QUYỀN PHÒNG ==========================
    async def get_all(self) -> List[DangKyNguyenVongResponse]:
        try:
            # Lấy tất cả đăng ký có trạng thái == 1 với nguyện vọng
            result = await self.db.execute(
                select(DangKyNCKH)
                .filter(DangKyNCKH.trang_thai == 1)  # Lọc theo trang_thai = 1
                .options(joinedload(DangKyNCKH.nguyen_vong))  # Load danh sách nguyện vọng
            )
            db_dks = result.scalars().unique().all()  # Đảm bảo trả về các kết quả duy nhất

            if not db_dks:
                raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký.")

            return [
                DangKyNguyenVongResponse(
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
                        for nv in db_dk.nguyen_vong  # Trả về danh sách nguyện vọng
                    ]
                ) for db_dk in db_dks
            ]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn CSDL: {str(e)}")

    # LẤY CHI TIẾT ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
    async def get_by_id(self, ma_dk: int) -> DangKyNguyenVongResponse:
        try:
            # Lấy đăng ký theo ma_dk và trạng thái == 1 với nguyện vọng
            result = await self.db.execute(
                select(DangKyNCKH)
                .filter(DangKyNCKH.ma_dk == ma_dk)  # Lọc theo ma_dk và trang_thai = 1
                .options(joinedload(DangKyNCKH.nguyen_vong))  # Load danh sách nguyện vọng
            )
            db_dk = result.scalars().first()  # Lấy kết quả đầu tiên

            if not db_dk:
                raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký.")

            # Trả về DangKyNguyenVongResponse với chi tiết nguyện vọng
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
                    for nv in db_dk.nguyen_vong  # Trả về danh sách nguyện vọng
                ]
            )

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn CSDL: {str(e)}")

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

    # ========================== QUYỀN SINH VIÊN ==========================
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
        
    # CẬP NHẬT ĐĂNG KÝ + NGUYỆN VỌNG
    async def update(self, ma_dk: int, dang_ky: schemas.DangKyNCKHUpdate, list_nguyen_vong: List[schemas.NguyenVongDKUpdate]) -> dict:
        try:
            # Lấy đăng ký theo ma_dk
            db_dk = await self.db.execute(
                select(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
            )
            db_dk = db_dk.scalars().first()

            if not db_dk:
                raise HTTPException(status_code=404, detail="Đăng ký không tồn tại.")

            # Cập nhật thông tin đăng ký
            db_dk.trang_thai = dang_ky.trang_thai  # Ví dụ cập nhật trạng thái đăng ký
            self.db.add(db_dk)

            # Xóa các nguyện vọng cũ
            await self.db.execute(
                delete(NguyenVongDK).where(NguyenVongDK.ma_dk == ma_dk)
            )

            muc_uu_tien_set = set()
            ma_gv_set = set()
            
            # Thêm các nguyện vọng mới
            for nv in list_nguyen_vong:
                # Kiểm tra mức ưu tiên không trùng nhau
                if nv.muc_uu_tien in muc_uu_tien_set:
                    raise HTTPException(status_code=400, detail="Mức ưu tiên không được trùng nhau.")
                if nv.ma_gv in ma_gv_set:
                    raise HTTPException(status_code=400, detail="Giảng viên không được trùng nhau.")

                muc_uu_tien_set.add(nv.muc_uu_tien)
                ma_gv_set.add(nv.ma_gv)

                db_nv = NguyenVongDK(
                    ma_gv=nv.ma_gv,
                    muc_uu_tien=nv.muc_uu_tien,
                    trang_thai=nv.trang_thai,
                    ma_dk=ma_dk
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
                    for nv in db_dk.nguyen_vong
                ]
            }

            return DangKyNguyenVongResponse(**response_data)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")

    # XÓA ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
    async def delete(self, ma_dk: int) -> dict:
        try:
            # Lấy đăng ký theo ma_dk
            db_dk = await self.db.execute(
                select(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
            )
            db_dk = db_dk.scalars().first()

            if not db_dk:
                raise HTTPException(status_code=404, detail="Đăng ký không tồn tại.")

            # Xóa các nguyện vọng liên quan
            await self.db.execute(
                delete(NguyenVongDK).where(NguyenVongDK.ma_dk == ma_dk)
            )

            # Xóa đăng ký
            await self.db.execute(
                delete(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
            )

            await self.db.commit()

            return {"message": "Đăng ký và các nguyện vọng liên quan đã được xóa thành công."}

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
