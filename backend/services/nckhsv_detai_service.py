from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from models.base_models import NhomNCKH, DeTaiNCKHSV
from schemas.base_schemas import DeTaiNCKHSVCreate

class DeTaiNCKHSVService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(
        self,
        ma_nhom: int,
        detainckhsv_data: DeTaiNCKHSVCreate,
        mgv: str = None
    ):
        try:
            result = await self.db.execute(
                select(NhomNCKH).where(NhomNCKH.ma_nhom == ma_nhom)
            )
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

            nhom.ma_de_tai == detai.ma_de_tai

            await self.db.commit()

            return {
                "message": "Tạo đề tài và gán cho nhóm thành công",
                "ma_nhom": ma_nhom,
                "ma_de_tai": detai.ma_de_tai,
                "ten_de_tai": detai.ten_de_tai
            }

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

