from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

#NCKH Sinh Vien
#DangKyNCKH Schemas
#HuongNghienCuuDangKyNCKH Schemas
#NguyenVongDangKyNCKH Schemas
#NhomNCKHSV Schemas
#ThanhVienNhomNCKH Schemas
#DeTaiNCKHSV Schemas
class DeTaiNCKHSVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên Đề Tài NCKH Sinh Viên")
    thuong_cap_khoa: Optional[str] = Field(None, max_length=255, description="Thưởng cấp khoa")
    thuong_cap_truong: Optional[str] = Field(None, max_length=255, description="Thưởng cấp trường")
    dot_thuc_hien: int = Field(..., description="Đợt thực hiện")
    trang_thai: int = Field(..., description="Trạng thái")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
class DeTaiNCKHSVCreate(DeTaiNCKHSVBase):
    pass
class DeTaiNCKHSVUpdate(BaseModel):
    ten_de_tai: Optional[str] = Field(None, max_length=255, description="Tên đề tài")
    thuong_cap_khoa: Optional[str] = Field(None, max_length=255, description="Thưởng cấp khoa")
    thuong_cap_truong: Optional[str] = Field(None, max_length=255, description="Thưởng cấp trường")
    dot_thuc_hien: Optional[int] = Field(None, description="Đợt thực hiện")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")
class DeTaiNCKHSV(DeTaiNCKHSVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài")

    class Config:
        orm_mode = True
#HuongNghienCuuDeTaiSV Schemas
#TaiLieuNCKHSV Schemas
#NCKH Giang Vien