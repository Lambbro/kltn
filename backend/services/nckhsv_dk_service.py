from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional

import schemas.base_schemas as schemas
from models.base_models import DangKyNCKH, SinhVien, NguyenVongDK, hnc_dknckh_table, HuongNghienCuu
from schemas.detai_sv_schemas import DangKyNCKHSVResponse

class DangKyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # LẤY ĐĂNG KÝ ĐANG THỰC HIỆN THEO MÃ SINH VIÊN (KÈM NGUYỆN VỌNG)
    async def get(
        self,
        ma_dk: Optional[int] = None,
        ma_sv: Optional[str] = None,
        ma_khoa: Optional[str] = None
    ) -> Optional[DangKyNCKHSVResponse]:
        try:
            if not ma_dk and not ma_sv:
                raise HTTPException(status_code=400, detail="Thiếu dữ kiện")

            query = (
                select(DangKyNCKH)
                .join(DangKyNCKH.sinh_vien)
                .options(joinedload(DangKyNCKH.sinh_vien))
            )

            conditions = [DangKyNCKH.trang_thai == 1]

            if ma_dk:
                conditions.append(DangKyNCKH.ma_dk == ma_dk)
            if ma_sv:
                conditions.append(DangKyNCKH.ma_sv == ma_sv)
            if ma_khoa:
                conditions.append(SinhVien.ma_khoa == ma_khoa)

            query = query.where(*conditions)

            result = await self.db.execute(query)
            db_dk = result.scalars().first()

            if not db_dk:
                raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký.")

            # Truy vấn list nguyện vọng
            ngv_query = select(NguyenVongDK).where(NguyenVongDK.ma_dk == db_dk.ma_dk)
            ngv_result = await self.db.execute(ngv_query)
            list_ngv = ngv_result.scalars().all()

            # Truy vấn list hướng nghiên cứu
            hnc_query = (
                select(HuongNghienCuu)
                .join(hnc_dknckh_table)
                .where(hnc_dknckh_table.c.ma_dk == db_dk.ma_dk)
            )
            hnc_result = await self.db.execute(hnc_query)
            list_hnc = hnc_result.scalars().all()

            return DangKyNCKHSVResponse(
                ma_dk=db_dk.ma_dk,
                ma_sv=db_dk.ma_sv,
                ten_sv=db_dk.sinh_vien.ten_sv,
                trang_thai=db_dk.trang_thai,
                list_nguyen_vong=[
                    schemas.NguyenVongDKResponse(
                        ma_dk=nv.ma_dk,
                        ma_gv=nv.ma_gv,
                        muc_uu_tien=nv.muc_uu_tien,
                        trang_thai=nv.trang_thai,
                    )
                    for nv in list_ngv
                ],
                list_hnc=[
                    schemas.HuongNghienCuuResponse(
                        ma_hnc=hnc.ma_hnc,
                        ten_hnc=hnc.ten_hnc,
                    )
                    for hnc in list_hnc
                ]
            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
    
    # LẤY TOÀN BỘ ĐĂNG KÝ (KÈM NGUYỆN VỌNG)
    async def get_all(self, skip: int = 0, limit: int = 100, ma_khoa: Optional[str] = None) -> List[DangKyNCKHSVResponse]:
        try:
            if ma_khoa:
                query = (
                    select(DangKyNCKH)
                    .join(DangKyNCKH.sinh_vien)
                    .options(
                        joinedload(DangKyNCKH.sinh_vien),
                        joinedload(DangKyNCKH.nguyen_vong),
                        joinedload(DangKyNCKH.huong_nghien_cuu),
                    )
                    .where(
                        DangKyNCKH.trang_thai == 1, 
                        SinhVien.ma_khoa == ma_khoa
                    )
                    .offset(skip).limit(limit)
                )
            else:
                query = (
                    select(DangKyNCKH)
                    .options(
                        joinedload(DangKyNCKH.sinh_vien),
                        joinedload(DangKyNCKH.nguyen_vong),
                        joinedload(DangKyNCKH.huong_nghien_cuu),
                    )
                    .where(DangKyNCKH.trang_thai == 1)
                    .offset(skip).limit(limit)
                )

            db_dk = await self.db.execute(query)
            db_dk_list = db_dk.unique().scalars().all()

            if not db_dk_list:
                raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký nào.")

            dang_ky_list = [
                DangKyNCKHSVResponse(
                    ma_dk=db_dk.ma_dk,
                    ma_sv=db_dk.ma_sv,
                    ten_sv=db_dk.sinh_vien.ten_sv,
                    trang_thai=db_dk.trang_thai,
                    list_nguyen_vong=[
                        schemas.NguyenVongDKResponse(
                            ma_dk=nv.ma_dk,
                            ma_gv=nv.ma_gv,
                            muc_uu_tien=nv.muc_uu_tien,
                            trang_thai=nv.trang_thai
                        )
                        for nv in db_dk.nguyen_vong
                    ],
                    list_hnc=[
                        schemas.HuongNghienCuuResponse(
                            ma_hnc=hnc.ma_hnc,
                            ten_hnc=hnc.ten_hnc
                        )
                        for hnc in db_dk.huong_nghien_cuu
                    ]
                )
                for db_dk in db_dk_list
            ]

            return dang_ky_list
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
  
    # TẠO ĐĂNG KÝ + NGUYỆN VỌNG
    async def add(
            self,
            dang_ky: schemas.DangKyNCKHCreate, 
            list_nguyen_vong: List[schemas.NguyenVongDKCreate],
            list_hnc: List[int]
    ) -> DangKyNCKHSVResponse:
        try:
            resist = select(DangKyNCKH).where(DangKyNCKH.ma_sv==dang_ky.ma_sv, DangKyNCKH.trang_thai==1)
            result = await self.db.execute(resist)
            db_resist = result.scalars().first()
            if db_resist:
                raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký tham gia.")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
        
        #Check list nguyện vọng
        if len(list_nguyen_vong) > 2:
            raise HTTPException(status_code=400, detail="Mỗi đăng ký chỉ được có tối đa 2 nguyện vọng.")
        #Check list hướng nghiên cứu
        if not list_hnc:
            raise HTTPException(status_code=400, detail="Danh sách hướng nghiên cứu không được để trống.")
        #Check mã sinh viên đã có đăng ký chưa
        existing_dang_ky = await self.db.execute(
            select(DangKyNCKH)
            .where(
                DangKyNCKH.ma_sv == dang_ky.ma_sv, 
                DangKyNCKH.trang_thai == 1
            )
        )
        existing_dang_ky = existing_dang_ky.scalars().first()
        if existing_dang_ky:
            raise HTTPException(status_code=400, detail="Sinh viên đã có một đăng ký đang chờ duyệt.")
        #Check mã giảng viên có bị trùng không
        muc_uu_tien_set = set()
        ma_gv_set = set()

        for nv in list_nguyen_vong:
            if nv.muc_uu_tien in muc_uu_tien_set:
                raise HTTPException(status_code=400, detail="Mức ưu tiên không được trùng nhau.")
            if nv.ma_gv in ma_gv_set:
                raise HTTPException(status_code=400, detail="Giảng viên không được trùng nhau.")
            muc_uu_tien_set.add(nv.muc_uu_tien)
            ma_gv_set.add(nv.ma_gv)
        #Check mã hướng nghiên cứu có bị trùng không
        ma_hnc_set = set()
        for ma_hnc in list_hnc:
            if ma_hnc in ma_hnc_set:
                raise HTTPException(status_code=400, detail="Hướng nghiên cứu không được trùng nhau.")
            ma_hnc_set.add(ma_hnc)
        #Xử lý dữ liệu

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
            
            # Truy vấn tất cả HNC có trong danh sách
            hnc_records = await self.db.execute(
                select(HuongNghienCuu).where(HuongNghienCuu.ma_hnc.in_(list_hnc))
            )
            hnc_list = hnc_records.scalars().all()
            # Validate HNC tồn tại
            if len(hnc_list) != len(list_hnc):
                missing = set(list_hnc) - {h.ma_hnc for h in hnc_list}
                raise HTTPException(404, f"Mã HNC không tồn tại: {missing}")

            # Thêm vào bảng trung gian
            if hnc_list:
                await self.db.execute(
                    insert(hnc_dknckh_table),
                    [{"ma_dk": db_dk.ma_dk, "ma_hnc": h.ma_hnc} for h in hnc_list]
                )

            await self.db.commit()

            result = await self.db.execute(
                select(DangKyNCKH)
                .options(
                    selectinload(DangKyNCKH.nguyen_vong),
                    selectinload(DangKyNCKH.huong_nghien_cuu),
                    selectinload(DangKyNCKH.sinh_vien)
                )
                .where(DangKyNCKH.ma_dk == db_dk.ma_dk)
            )

            db_dk = result.scalars().first()
            if not db_dk:
                raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký vừa tạo.")

            sinh_vien = db_dk.sinh_vien
            if not sinh_vien:
                raise HTTPException(status_code=404, detail="Không tìm thấy thông tin sinh viên.")

            add_data = DangKyNCKHSVResponse(
                    ma_dk=db_dk.ma_dk,
                    ma_sv=db_dk.ma_sv,
                    ten_sv=sinh_vien.ten_sv,
                    trang_thai=db_dk.trang_thai,
                    list_nguyen_vong=[
                        schemas.NguyenVongDKResponse(
                            ma_dk=nv.ma_dk,
                            ma_gv=nv.ma_gv,
                            muc_uu_tien=nv.muc_uu_tien,
                            trang_thai=nv.trang_thai
                        )
                        for nv in db_dk.nguyen_vong
                    ],
                    list_hnc=[
                        schemas.HuongNghienCuuResponse(
                            ma_hnc=hnc.ma_hnc,
                            ten_hnc=hnc.ten_hnc
                        )
                        for hnc in db_dk.huong_nghien_cuu
                    ]
                )

            return add_data

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Dữ liệu không hợp lệ hoặc bị trùng.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")

    #Update đăng ký
    async def update(
        self,
        ma_dk: int,
        dang_ky_update: schemas.DangKyNCKHUpdate,
        list_nguyen_vong: List[schemas.NguyenVongDKCreate],
        list_hnc: List[int]
    ) -> DangKyNCKHSVResponse:
        query = await self.db.execute(
            select(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
        )
        db_dk = query.scalars().first()

        if not db_dk:
            raise HTTPException(status_code=404, detail="Đăng ký không tồn tại.")
        
        #Check list nguyện vọng
        if len(list_nguyen_vong) > 2:
            raise HTTPException(status_code=400, detail="Mỗi đăng ký chỉ được có tối đa 2 nguyện vọng.")
        
        #Kiểm tra trùng lặp
        muc_uu_tien_set = set()
        ma_gv_set = set()
        for nv in list_nguyen_vong:
            if nv.muc_uu_tien in muc_uu_tien_set:
                raise HTTPException(status_code=400, detail="Mức ưu tiên không được trùng nhau.")
            if nv.ma_gv in ma_gv_set:
                raise HTTPException(status_code=400, detail="Giảng viên không được trùng nhau.")
            muc_uu_tien_set.add(nv.muc_uu_tien)
            ma_gv_set.add(nv.ma_gv)

        if not list_hnc:
            raise HTTPException(status_code=400, detail="Danh sách hướng nghiên cứu không được để trống.")
        
        # Kiểm tra trùng HNC
        if len(list_hnc) != len(set(list_hnc)):
            raise HTTPException(status_code=400, detail="Hướng nghiên cứu bị trùng.")
        
        try:
            db_dk.trang_thai = dang_ky_update.trang_thai

            #Xóa hết nguyện vọng cũ
            await self.db.execute(
                delete(NguyenVongDK).where(NguyenVongDK.ma_dk == ma_dk)
            )

            for nv in list_nguyen_vong:
                db_nv = NguyenVongDK(
                    ma_gv=nv.ma_gv,
                    muc_uu_tien=nv.muc_uu_tien,
                    trang_thai=nv.trang_thai,
                    ma_dk=db_dk.ma_dk
                )
                self.db.add(db_nv)

            # Cập nhật hướng nghiên cứu
            hnc_records = await self.db.execute(
                select(HuongNghienCuu).where(HuongNghienCuu.ma_hnc.in_(list_hnc))
            )

            hnc_list = hnc_records.scalars().all()

            found_hnc_ids = {hnc.ma_hnc for hnc in hnc_list}
            missing = set(list_hnc) - found_hnc_ids
            if missing:
                raise HTTPException(status_code=404, detail=f"Hướng nghiên cứu không tồn tại: {', '.join(map(str, missing))}")

            db_dk.huong_nghien_cuu = hnc_list

            await self.db.commit()
            result = await self.db.execute(
                select(DangKyNCKH)
                .options(
                    selectinload(DangKyNCKH.nguyen_vong),
                    selectinload(DangKyNCKH.huong_nghien_cuu),
                    selectinload(DangKyNCKH.sinh_vien)
                )
                .where(DangKyNCKH.ma_dk == db_dk.ma_dk)
            )
            db_dk = result.scalars().first()

            sinh_vien = await self.db.execute(
                select(SinhVien).where(SinhVien.ma_sv == dang_ky_update.ma_sv)
            )

            sinh_vien = sinh_vien.scalars().first()
            if not sinh_vien:
                raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")

            return DangKyNCKHSVResponse(
                ma_dk=db_dk.ma_dk,
                ma_sv=db_dk.ma_sv,
                ten_sv=db_dk.sinh_vien.ten_sv,
                trang_thai=db_dk.trang_thai,
                list_nguyen_vong=[
                    schemas.NguyenVongDKResponse(
                        ma_dk=nv.ma_dk,
                        ma_gv=nv.ma_gv,
                        muc_uu_tien=nv.muc_uu_tien,
                        trang_thai=nv.trang_thai
                    )
                    for nv in db_dk.nguyen_vong
                ],
                list_hnc=[
                    schemas.HuongNghienCuuResponse(
                        ma_hnc=hnc.ma_hnc,
                        ten_hnc=hnc.ten_hnc
                    ) for hnc in db_dk.huong_nghien_cuu
                ]
            )
        
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Dữ liệu không hợp lệ hoặc bị trùng.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
        
    #Xóa đăng ký
    async def delete(self, ma_dk: int) -> dict:
        db_dk_query = await self.db.execute(
            select(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
        )
        db_dk = db_dk_query.scalars().first()

        if not db_dk:
            raise HTTPException(status_code=404, detail="Đăng ký không tồn tại.")
        
        try:
            await self.db.execute(
                delete(NguyenVongDK).where(NguyenVongDK.ma_dk == ma_dk)
            )
            await self.db.execute(
                delete(hnc_dknckh_table).where(hnc_dknckh_table.c.ma_dk == ma_dk)
            )
            await self.db.execute(
                delete(DangKyNCKH).where(DangKyNCKH.ma_dk == ma_dk)
            )
            await self.db.commit()
            return {"message": "Xóa đăng ký thành công."}
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Lỗi khi xóa đăng ký.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")