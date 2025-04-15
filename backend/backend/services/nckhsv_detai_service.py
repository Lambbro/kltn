from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from models.base_models import NhomNCKH, DeTaiNCKHSV, TaiLieuNCKHSV
from schemas.base_schemas import DeTaiNCKHSVCreate, TaiLieuNCKHSVResponse
from schemas.detai_sv_schemas import DeTaiNCKHSinhVienResponse, NhomNCKHSVResponse
from typing import Optional, List

class DeTaiNCKHSVService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(
        self,
        ma_nhom: int,
        detainckhsv_data: DeTaiNCKHSVCreate,
        mgv: Optional[str] = None,
        ma_khoa: Optional[str] = None
    ):
        try:
            query = select(NhomNCKH).where(NhomNCKH.ma_nhom == ma_nhom)

            result = await self.db.execute(query)
            nhom = result.scalar_one_or_none()
            
            if mgv and mgv!=nhom.ma_gv:
                raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập")
                
            if not nhom:
                raise HTTPException(status_code=404, detail="Không tìm thấy nhóm")
            
            if nhom.ma_de_tai is not None:
                raise HTTPException(status_code=400, detail="Nhóm này đã có đề tài")
            
            detai = DeTaiNCKHSV(**detainckhsv_data.model_dump())
            self.db.add(detai)
            await self.db.flush()

            nhom.ma_de_tai = detai.ma_de_tai

            await self.db.commit()

            await self.db.refresh(detai)
            await self.db.refresh(nhom)

            response = DeTaiNCKHSinhVienResponse(
                ma_de_tai=detai.ma_de_tai,
                ten_de_tai=detai.ten_de_tai,
                dot_thuc_hien=detai.dot_thuc_hien,
                trang_thai=detai.trang_thai,
                tien_do=detai.tien_do,
                diem_so=detai.diem_so,
                nhom=NhomNCKHSVResponse.model_validate(nhom),
                tai_lieu=[]  # Nếu có tài liệu thì bạn lấy từ DB rồi truyền vào đây
            )

            return response

        except HTTPException as http_err:
            raise http_err
        except OperationalError:
            await self.db.rollback()
            raise HTTPException(status_code=503, detail="Lỗi kết nối cơ sở dữ liệu")
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=409, detail="Lỗi ràng buộc dữ liệu")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

    async def get_all(
        self,
        mgv: Optional[str] = None,
        ma_khoa: Optional[str] = None,
        is_doing: Optional[bool] = None
    ) -> List[DeTaiNCKHSinhVienResponse]:
        try:
            query = select(DeTaiNCKHSV)
            result = await self.db.execute(query)
            detai_list = result.scalars().all()

            responses = []
            for detai in detai_list:
                # Truy vấn nhóm tương ứng với đề tài
                query_nhom = select(NhomNCKH).where(NhomNCKH.ma_de_tai == detai.ma_de_tai)
                result_nhom = await self.db.execute(query_nhom)
                nhom = result_nhom.scalar_one_or_none()

                # Truy vấn tài liệu nếu cần
                query_tai_lieu = select(TaiLieuNCKHSV).where(TaiLieuNCKHSV.ma_de_tai == detai.ma_de_tai)
                result_tai_lieu = await self.db.execute(query_tai_lieu)
                tai_lieu_list = result_tai_lieu.scalars().all()

                responses.append(DeTaiNCKHSinhVienResponse(
                    ma_de_tai=detai.ma_de_tai,
                    ten_de_tai=detai.ten_de_tai,
                    dot_thuc_hien=detai.dot_thuc_hien,
                    trang_thai=detai.trang_thai,
                    tien_do=detai.tien_do,
                    diem_so=detai.diem_so,
                    nhom=NhomNCKHSVResponse.model_validate(nhom) if nhom else None,
                    tai_lieu=[TaiLieuNCKHSVResponse.model_validate(tl) for tl in tai_lieu_list]
                ))

            return responses

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
