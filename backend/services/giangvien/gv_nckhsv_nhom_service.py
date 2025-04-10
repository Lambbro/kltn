from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError

from models.base_models import NhomNCKH, GiangVien, thanhvien_nhomSV_table
from schemas.detai_sv_schemas import NhomNCKHSVResponse, ThanhVienNhomResponse
from schemas.base_schemas import NhomNCKHCreate

class GVNhomNCKHSVService:
    def __init__ (self, db: AsyncSession):
        self.db = db

    #Tạo nhóm nghiên cứu khoa học
    async def add(self, nhom_data: NhomNCKHCreate, dssv: list[str]):
        try:
            nhom = NhomNCKH(**nhom_data.model_dump())
            self.db.add(nhom)
            await self.db.flush()  
            # Gán sinh viên vào nhóm
            for ma_sv in dssv:
                stmt = insert(thanhvien_nhomSV_table).values(ma_nhom=nhom.ma_nhom, ma_sv=ma_sv)
                await self.db.execute(stmt)

            await self.db.commit()

            return nhom
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
                    trang_thai=nhom.trang_thai,
                    ma_gv=nhom.ma_gv,
                    ma_de_tai=nhom.ma_de_tai,
                    thanh_vien=[
                        ThanhVienNhomResponse(ma_sv=sv.ma_sv, ten_sv=sv.ten_sv) 
                        for sv in nhom.sinh_vien
                    ]
                ))

            return res
        except HTTPException as http_err:
            raise http_err
        except OperationalError as e:
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError as e:
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
                trang_thai=nhom.trang_thai,
                ma_gv=nhom.ma_gv,
                ma_de_tai=nhom.ma_de_tai,
                thanh_vien=[
                    ThanhVienNhomResponse(ma_sv=sv.ma_sv, ten_sv=sv.ten_sv) 
                    for sv in nhom.sinh_vien
                ]
            )
        except HTTPException as http_err:
            raise http_err
        except OperationalError as e:
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError as e:
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
    async def update(self, ma_nhom: int, nhom_data: NhomNCKHCreate, dssv: list[str], ma_khoa: str):
        try:
            result = await self.db.execute(
                select(NhomNCKH)
                .join(NhomNCKH.giang_vien)
                .where(NhomNCKH.ma_nhom == ma_nhom, GiangVien.ma_khoa == ma_khoa)
            )
            nhom = result.scalars().first()

            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm với mã này")
            
            for key, value in nhom_data.model_dump().items():
                setattr(nhom, key, value)

            # Xóa tất cả sinh viên hiện tại trong nhóm
            nhom.sinh_vien.clear()

            # Thêm sinh viên mới vào nhóm
            for ma_sv in dssv:
                stmt = insert(thanhvien_nhomSV_table).values(ma_nhom=nhom.ma_nhom, ma_sv=ma_sv)
                await self.db.execute(stmt)

            await self.db.commit()
            return nhom
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
        
    