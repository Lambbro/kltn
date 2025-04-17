import os
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from models.base_models import NhomNCKH, DeTaiNCKHSV, TaiLieuNCKHSV
from schemas.base_schemas import TaiLieuNCKHSVResponse, DeTaiNCKHGVResponse
from typing import Optional, List
from datetime import datetime

ALLOWED_EXTENSIONS = {
    ".pdf": 10 * 1024 * 1024,     # 10MB
    ".docx": 10 * 1024 * 1024,    # 10MB
    ".doc": 10 * 1024 * 1024,    # 10MB
    ".pptx": 50 * 1024 * 1024     # 50MB
}

UPLOAD_DIR = "../uploads/sv"

class TaiLieuNCKHSVService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(
        self,
        ma_de_tai: int,
        loai_tai_lieu: int,
        file: UploadFile
    ):
        try:
            file_ext = os.path.splitext(file.filename)[1].lower()
            max_size = ALLOWED_EXTENSIONS.get(file_ext)

            if not max_size:
                raise HTTPException(status_code=400, detail="Chỉ chấp nhận file .pdf, .docx, .pptx")


            # Kiểm tra kích thước
            contents = await file.read()
            if len(contents) > max_size:
                size_mb = max_size // (1024 * 1024)
                raise HTTPException(status_code=400, detail=f"File vượt quá {size_mb}MB cho định dạng {file_ext}")
            file.file.seek(0)

            #Tìm kiếm đề tài
            result = await self.db.execute(select(DeTaiNCKHSV).where(DeTaiNCKHSV.ma_de_tai == ma_de_tai))
            de_tai = result.scalars().first()

            if not de_tai:
                raise HTTPException(status_code=404, detail="Không tìm thấy đề tài")
            #Tạo folder lưu file
            folder_name = f"{ma_de_tai}-{de_tai.dot_thuc_hien}"
            folder_path = os.path.join(UPLOAD_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            #Đặt tên mới cho file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{ma_de_tai}-{loai_tai_lieu}-{timestamp}{file_ext}"
            file_path = os.path.join(folder_path, new_filename)

            #Lưu file
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            # Ghi bản ghi vào DB
            tailieu = TaiLieuNCKHSV(
                loai_tai_lieu=loai_tai_lieu,
                link_tep=file_path,
                thoi_gian_nop=datetime.now(),
                trang_thai=1,
                ma_de_tai=ma_de_tai
            )
            self.db.add(tailieu)
            await self.db.commit()

            return {
                "message": "Nộp tài liệu thành công",
                "ten_file": new_filename,
                "duong_dan": file_path
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý file: " + str(e))