from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

#Hội Đồng Khoa schemas
class HoiDongKhoaBase(BaseModel):
    so_hd: Optional[int] = Field(None, description="Số hội đồng")
    loai_hd: int = Field(..., description="Loại hội đồng")
    ngay_bao_cao: Optional[date] = Field(None, description="Ngày báo cáo")
    dia_diem: Optional[str] = Field(None, description="Địa điểm")
    trang_thai: Optional[int] = Field(None, description="Trạng thái hội đồng")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")

class HoiDongKhoaCreate(HoiDongKhoaBase):
    pass

class HoiDongKhoaUpdate(BaseModel):
    so_hd: Optional[int] = Field(None, description="Số hội đồng")
    loai_hd: Optional[int] = Field(None, description="Loại hội đồng")
    ngay_bao_cao: Optional[date] = Field(None, description="Ngày báo cáo")
    dia_diem: Optional[str] = Field(None, description="Địa điểm tổ chức")
    trang_thai: Optional[int] = Field(None, description="Trạng thái hội đồng")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class HoiDongKhoaResponse(HoiDongKhoaBase):
    ma_hd: int = Field(..., description="Mã hội đồng")

    class Config:
        from_attributes = True

#TVHDKhoa schemas
class TVHDKhoaBase(BaseModel):
    ma_hd: int = Field(..., description="Mã hội đồng")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    tu_cach: int = Field(..., description="Tư cách trong hội đồng")

# Schema để tạo mới TVHDKhoa
class TVHDKhoaCreate(TVHDKhoaBase):
    pass

# Schema để cập nhật TVHDKhoa (cho phép cập nhật từng trường)
class TVHDKhoaUpdate(BaseModel):
    ma_hd: Optional[int] = Field(None, description="Mã hội đồng")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")
    tu_cach: Optional[int] = Field(None, description="Tư cách trong hội đồng")

# Schema để đọc dữ liệu TVHDKhoa từ DB
class TVHDKhoaResponse(TVHDKhoaBase):
    class Config:
        from_attributes = True

#Hội Đồng Trường schemas
class HoiDongTruongBase(BaseModel):
    so_hd: Optional[int] = Field(None, description="Số hội đồng")
    loai_hd: int = Field(..., description="Loại hội đồng")
    ngay_bao_cao: Optional[date] = Field(None, description="Ngày báo cáo")
    dia_diem: Optional[str] = Field(None, description="Địa điểm")
    trang_thai: Optional[int] = Field(None, description="Trạng thái hội đồng")

class HoiDongTruongCreate(HoiDongTruongBase):
    pass

class HoiDongTruongUpdate(BaseModel):
    so_hd: Optional[int] = Field(None, description="Số hội đồng")
    loai_hd: Optional[int] = Field(None, description="Loại hội đồng")
    ngay_bao_cao: Optional[date] = Field(None, description="Ngày báo cáo")
    dia_diem: Optional[str] = Field(None, description="Địa điểm tổ chức")
    trang_thai: Optional[int] = Field(None, description="Trạng thái hội đồng")

class HoiDongTruongResponse(HoiDongTruongBase):
    ma_hd: int = Field(..., description="Mã hội đồng")

    class Config:
        from_attributes = True

#TVHD Trường schemas
class TVHDTruongBase(BaseModel):
    gmail: Optional[str] = Field(None, max_length=50, description="Gmail của thành viên")
    ten_tv: str = Field(..., max_length=255, description="Tên thành viên")
    noi_cong_tac: str = Field(..., description="Nơi công tác")
    tu_cach: int = Field(..., description="Tư cách của thành viên")
    ma_hd: int = Field(..., description="Mã hội đồng")

class TVHDTruongCreate(TVHDTruongBase):
    pass

class TVHDTruongUpdate(BaseModel):
    gmail: Optional[str] = Field(None, max_length=50, description="Gmail của thành viên")
    ten_tv: Optional[str] = Field(None, max_length=255, description="Tên thành viên")
    noi_cong_tac: Optional[str] = Field(None, description="Nơi công tác")
    tu_cach: Optional[int] = Field(None, description="Tư cách của thành viên")
    ma_hd: Optional[int] = Field(None, description="Mã hội đồng")

class TVHDTruongResponse(TVHDTruongBase):
    ma_tv: int = Field(..., description="Mã thành viên hội đồng")

    class Config:
        from_attributes = True