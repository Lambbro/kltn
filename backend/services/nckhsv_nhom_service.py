from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from typing import Optional
from models.base_models import NhomNCKH, SinhVien, GiangVien, thanhvien_nhomSV_table, DeTaiNCKHSV
from schemas.detai_sv_schemas import NhomNCKHSVResponse, ThanhVienNhomResponse
from schemas.base_schemas import NhomNCKHCreate, DeTaiNCKHSVCreate

class NhomNCKHSVService:
    def __init__ (self, db: AsyncSession):
        self.db = db

    async def add(
        self,
        ma_gv: str, 
        dssv: list[str],
        detainckhsv_data: Optional[DeTaiNCKHSVCreate] = None
    ):
        if len(dssv) > 3:
            raise HTTPException(status_code=400, detail="Nhóm tối đa 3 thành viên")
        try:
            nhom_data = NhomNCKHCreate(ma_gv=ma_gv)
            active_groups_result = await self.db.execute(
                select(NhomNCKH)
                .where(NhomNCKH.ma_gv == nhom_data.ma_gv, NhomNCKH.trang_thai == 1)
            )
            active_groups = active_groups_result.scalars().all()
            if len(active_groups) >= 2:
                raise HTTPException(status_code=400, detail="Giảng viên này đã có 2 nhóm đang hoạt động")
            # Kiểm tra sinh viên đã có trong nhóm cùng giảng viên và trạng thái 1 chưa
            if active_groups:
                active_group_ids = [g.ma_nhom for g in active_groups]

                sv_in_other_group_result = await self.db.execute(
                    select(thanhvien_nhomSV_table.c.ma_sv)
                    .where(thanhvien_nhomSV_table.c.ma_nhom.in_(active_group_ids))
                )
                existing_svs = {row[0] for row in sv_in_other_group_result.fetchall()}

                conflict_svs = set(dssv) & existing_svs
                if conflict_svs:
                    raise HTTPException(
                    status_code=400,
                    detail=f"Sinh viên {', '.join(conflict_svs)} đã thuộc nhóm khác của giảng viên này đang hoạt động"
                )
            # Tạo đề tài
            if detainckhsv_data:
                detai = DeTaiNCKHSV(**detainckhsv_data.model_dump())
                self.db.add(detai)
                await self.db.flush()  # Đảm bảo rằng ID của đề tài đã được tạo

                # Tạo nhóm nghiên cứu khoa học
                nhom = NhomNCKH(**nhom_data.model_dump(), ma_de_tai=detai.ma_de_tai)
            else:
                nhom = NhomNCKH(**nhom_data.model_dump())

            self.db.add(nhom)
            await self.db.flush()  # Đảm bảo rằng ID của nhóm đã được tạo

            # Gán sinh viên vào nhóm
            for ma_sv in dssv:
                stmt = insert(thanhvien_nhomSV_table).values(ma_nhom=nhom.ma_nhom, ma_sv=ma_sv)
                await self.db.execute(stmt)

            await self.db.commit()

            # Truy vấn lại nhóm vừa tạo kèm danh sách thành viên
            query = (
                select(NhomNCKH)
                .options(selectinload(NhomNCKH.sinh_vien))  # Load quan hệ thành viên
                .where(NhomNCKH.ma_nhom == nhom.ma_nhom)
            )
            result = await self.db.execute(query)
            nhom_full = result.scalar_one()

            # Tạo dữ liệu phản hồi
            response = NhomNCKHSVResponse(
                ma_nhom=nhom_full.ma_nhom,
                ma_gv=nhom_full.ma_gv,
                ma_de_tai=nhom_full.ma_de_tai,
                ten_de_tai=nhom_full.de_tai_sv.ten_de_tai if nhom_full.de_tai_sv else None,
                thanh_vien=[
                    ThanhVienNhomResponse(
                        ma_sv=sv.ma_sv,
                        ten_sv=sv.ten_sv
                    )
                    for sv in nhom_full.sinh_vien
                ]
            )
            return response
        
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo nhóm: {str(e)}")

    #Lấy tất cả nhóm nghiên cứu khoa học
    async def get_all(self, ma_khoa: str):
        try:
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .options(
                    selectinload(NhomNCKH.sinh_vien),
                    joinedload(NhomNCKH.giang_vien),
                    joinedload(NhomNCKH.de_tai_sv),
                )
                .where(GiangVien.ma_khoa == ma_khoa)
            )
            nhom_list = result.scalars().all()

            if not nhom_list:
                raise HTTPException(status_code=404, detail="Không có nhóm nào được tìm thấy")

            res = []
            for nhom in nhom_list:
                res.append(NhomNCKHSVResponse(
                    ma_nhom=nhom.ma_nhom,
                    ma_gv=nhom.ma_gv,
                    ma_de_tai=nhom.ma_de_tai,
                    ten_de_tai=nhom.de_tai_sv.ten_de_tai if nhom.de_tai_sv else None,
                    thanh_vien=[
                        ThanhVienNhomResponse(
                            ma_sv=sv.ma_sv,
                            ten_sv=sv.ten_sv
                        ) for sv in nhom.sinh_vien
                    ]
                ))

            return res

        except HTTPException as http_err:
            raise http_err
        except OperationalError:
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa hoặc foreign key)")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

        
    async def get_by_ma_nhom(self, ma_nhom: int, ma_khoa: str):
        try:
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .options(
                    selectinload(NhomNCKH.sinh_vien),
                    joinedload(NhomNCKH.giang_vien),
                    joinedload(NhomNCKH.de_tai_sv),
                )
                .where(GiangVien.ma_khoa == ma_khoa, NhomNCKH.ma_nhom == ma_nhom)
            )
            nhom = result.scalars().first()

            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã này")

            return NhomNCKHSVResponse(
                ma_nhom=nhom.ma_nhom,
                ma_gv=nhom.ma_gv,
                ma_de_tai=nhom.ma_de_tai,
                ten_de_tai=nhom.de_tai_sv.ten_de_tai if nhom.de_tai_sv else None,
                thanh_vien=[
                    ThanhVienNhomResponse(
                        ma_sv=sv.ma_sv,
                        ten_sv=sv.ten_sv
                    ) for sv in nhom.sinh_vien
                ]
            )

        except HTTPException as http_err:
            raise http_err
        except OperationalError:
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa hoặc foreign key)")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

        
    # Xóa nhóm nghiên cứu khoa học
    async def delete(self, ma_nhom: int, ma_khoa: str):
        try:
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .where(NhomNCKH.ma_nhom == ma_nhom, GiangVien.ma_khoa == ma_khoa)
            )
            nhom = result.scalars().first()
            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã này")
            
            await self.db.delete(nhom)
            await self.db.commit()
            return {"detail": "Xóa nhóm thành công"}
        except HTTPException as http_err:
            raise http_err
        except OperationalError as e:
            await self.db.rollback()
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa hoặc foreign key)")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
        
    # Cập nhật nhóm nghiên cứu khoa học
    async def update(
            self, 
            ma_nhom: int, 
            nhom_data: NhomNCKHCreate, 
            ma_khoa: str,
            dssv: Optional[list[str]] = None, 
    ):
        if len(dssv) > 3:
            raise HTTPException(status_code=400, detail="Nhóm tối đa 3 thành viên")
        try:
            # Kiểm tra sự tồn tại của nhóm
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .where(NhomNCKH.ma_nhom == ma_nhom, GiangVien.ma_khoa == ma_khoa)
            )
            nhom = result.scalars().first()

            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã này")

            # Kiểm tra giảng viên đã có 2 nhóm đang hoạt động
            active_groups_result = await self.db.execute(
                select(NhomNCKH)
                .where(NhomNCKH.ma_gv == nhom.ma_gv, NhomNCKH.trang_thai == 1)
            )
            active_groups = active_groups_result.scalars().all()

            if len(active_groups) >= 2:
                raise HTTPException(status_code=400, detail="Giảng viên này đã có 2 nhóm đang hoạt động")

            # Cập nhật thông tin nhóm
            for key, value in nhom_data.model_dump().items():
                setattr(nhom, key, value)

            if dssv is not None:
                # Kiểm tra sinh viên có tồn tại trong cơ sở dữ liệu
                existing_students = await self.db.execute(
                    select(SinhVien).where(SinhVien.ma_sv.in_(dssv))
                )
                students_in_db = existing_students.scalars().all()

                if len(students_in_db) != len(dssv):
                    raise HTTPException(status_code=400, detail="Một hoặc nhiều sinh viên không tồn tại trong cơ sở dữ liệu")

                # Xóa tất cả sinh viên hiện tại trong nhóm
                nhom.sinh_vien.clear()

                # Thêm sinh viên mới vào nhóm
                for ma_sv in dssv:
                    stmt = insert(thanhvien_nhomSV_table).values(ma_nhom=nhom.ma_nhom, ma_sv=ma_sv)
                    await self.db.execute(stmt)

            await self.db.commit()

            # Truy vấn lại nhóm vừa cập nhật kèm danh sách thành viên
            query = (
                select(NhomNCKH)
                .options(selectinload(NhomNCKH.sinh_vien))  # Load quan hệ thành viên
                .where(NhomNCKH.ma_nhom == nhom.ma_nhom)
            )
            result = await self.db.execute(query)
            nhom_full = result.scalar_one()

            # Tạo dữ liệu phản hồi
            response = NhomNCKHSVResponse(
                ma_nhom=nhom_full.ma_nhom,
                ma_gv=nhom_full.ma_gv,
                ma_de_tai=nhom_full.ma_de_tai,
                ten_de_tai=nhom_full.de_tai_sv.ten_de_tai if nhom_full.de_tai_sv else None,
                thanh_vien=[
                    ThanhVienNhomResponse(
                        ma_sv=sv.ma_sv,
                        ten_sv=sv.ten_sv
                    )
                    for sv in nhom_full.sinh_vien
                ]
            )
            return response

        except HTTPException as http_err:
            raise http_err
        except OperationalError:
            await self.db.rollback()
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa hoặc foreign key)")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
    
    async def get_by_ma_gv(self, ma_gv: str, ma_khoa: str):
        try:
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .options(
                    selectinload(NhomNCKH.sinh_vien),
                    joinedload(NhomNCKH.giang_vien),
                    joinedload(NhomNCKH.de_tai_sv),
                )
                .where(
                    GiangVien.ma_khoa == ma_khoa,
                    NhomNCKH.ma_gv == ma_gv,
                    NhomNCKH.trang_thai == 1
                )
            )
            nhom = result.scalars().first()
            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã giảng viên này")

            return NhomNCKHSVResponse(
                ma_nhom=nhom.ma_nhom,
                ma_gv=nhom.ma_gv,
                ma_de_tai=nhom.ma_de_tai,
                ten_de_tai=nhom.de_tai_sv.ten_de_tai if nhom.de_tai_sv else None,
                thanh_vien=[
                    ThanhVienNhomResponse(
                        ma_sv=sv.ma_sv,
                        ten_sv=sv.ten_sv
                    ) for sv in nhom.sinh_vien
                ]
            )
        except HTTPException as http_err:
            raise http_err
        except OperationalError:
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu (có thể trùng khóa hoặc foreign key)")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
