from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

#Đề tài NCKH giảng viên schemas
class DeTaiNCKHGVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài NCKH của giảng viên")
    tg_bat_dau: datetime = Field(..., description="Thời gian bắt đầu đề tài")
    tg_nghiem_thu: datetime = Field(..., description="Thời gian nghiệm thu đề tài")
    tg_thuc_nghiem: datetime = Field(..., description="Thời gian thực nghiệm đề tài")
    trang_thai: int = Field(2, description="Trạng thái đề tài")
    tien_do: int = Field(1, description="Tiến độ đề tài")

class DeTaiNCKHGVCreate(DeTaiNCKHGVBase):
    pass

class DeTaiNCKHGVUpdate(BaseModel):
    ten_de_tai: Optional[str] = Field(None, max_length=255, description="Tên đề tài NCKH của giảng viên")
    tg_bat_dau: Optional[datetime] = Field(None, description="Thời gian bắt đầu đề tài")
    tg_nghiem_thu: Optional[datetime] = Field(None, description="Thời gian nghiệm thu đề tài")
    tg_thuc_nghiem: Optional[datetime] = Field(None, description="Thời gian thực nghiệm đề tài")
    trang_thai: Optional[int] = Field(None, description="Trạng thái đề tài")
    tien_do: Optional[int] = Field(None, description="Tiến độ đề tài")

class DeTaiNCKHGVResponse(DeTaiNCKHGVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài NCKH của giảng viên")

    class Config:
        from_attributes = True

#Thành Viên NCKH Giảng Viên schemas
class ThanhVienNCKHGVBase(BaseModel):
    ma_de_tai: int = Field(..., description="Mã đề tài NCKH của giảng viên")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    vi_tri_tham_gia: int = Field(..., description="Vị trí tham gia trong đề tài")

class ThanhVienNCKHGVCreate(ThanhVienNCKHGVBase):
    pass

class ThanhVienNCKHGVUpdate(BaseModel):
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài NCKH của giảng viên")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")
    vi_tri_tham_gia: Optional[int] = Field(None, description="Vị trí tham gia trong đề tài")

class ThanhVienNCKHGVResponse(ThanhVienNCKHGVBase):
    class Config:
        from_attributes = True

#Tài liệu NCKH giảng viên schemas
class TaiLieuNCKHGVBase(BaseModel):
    loai_tai_lieu: int = Field(..., description="Loại tài liệu NCKH giảng viện")
    link_tep: str = Field(..., description="Đường dẫn tới tệp tài liệu")
    thoi_gian_nop: datetime = Field(..., description="Thời gian nộp tài liệu")
    trang_thai: int = Field(1, description="Trạng thái đề tài")
    phan_hoi: Optional[str] = Field(None, description="Phản hồi góp ý từ hội đồng")
    ma_de_tai: int = Field(..., description="Mã đề tài")
    ma_hd: Optional[int] = Field(None, description="Mã hội đồng trường")

class TaiLieuNCKHGVCreate(TaiLieuNCKHGVBase):
    pass

class TaiLieuNCKHGVUpdate(BaseModel):
    loai_tai_lieu: Optional[int] = Field(None, description="Loại tài liệu NCKH giảng viên")
    link_tep: Optional[str] = Field(None, description="Đường dẫn tới tệp tài liệu")
    thoi_gian_nop: Optional[datetime] = Field(None, description="Thời gian nộp tài liệu")
    trang_thai: Optional[int] = Field(None, description="Trạng thái tài liệu")
    phan_hoi: Optional[str] = Field(None, description="Phản hồi góp ý từ hội đồng")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài")
    ma_hd: Optional[int] = Field(None, description="Mã hội đồng trường")

class TaiLieuNCKHGVResponse(TaiLieuNCKHGVBase):
    ma_tai_lieu: int = Field(..., description="Mã tài liệu (ID)")
    class Config:
        from_attributes = True