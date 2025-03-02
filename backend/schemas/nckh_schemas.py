from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

#NCKH Sinh Vien
#DangKyNCKH Schemas
class DangKyNCKHBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
class DangKyNCKHCreate(DangKyNCKHBase):
    pass
class DangKyNCKHUpdate(BaseModel):
    ma_sv: Optional[str] = Field(None, max_length=20, description="Mã sinh viên")
class DangKyNCKH(DangKyNCKHBase):
    ma_dk: int = Field(..., description="Mã đăng ký")

    class Config:
        orm_mode = True
#NguyenVongDangKyNCKH Schemas
class NguyenVongDangKyNCKHBase(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    muc_uu_tien: int = Field(..., description="Mức ưu tiên")
    trang_thai: int = Field(..., description="Trạng thái")
class NguyenVongDangKyNCKHCreate(NguyenVongDangKyNCKHBase):
    ma_dk: int = Field(..., description="Mã đăng ký")
class NguyenVongDangKyNCKHUpdate(BaseModel):
    muc_uu_tien: Optional[int] = Field(None, description="Mức ưu tiên")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
class NguyenVongDangKyNCKH(NguyenVongDangKyNCKHBase):
    ma_dk: int = Field(..., description="Mã đăng ký")

    class Config:
        orm_mode = True
#NhomNCKHSV Schemas
class NhomNCKHBase(BaseModel):
    trang_thai: int = Field(..., description="Trạng thái")
    ma_de_tai: int = Field(..., description="Mã đề tài")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
class NhomNCKHCreate(NhomNCKHBase):
    pass
class NhomNCKHUpdate(BaseModel):
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")
class NhomNCKH(NhomNCKHBase):
    ma_nhom: int = Field(..., description="Mã nhóm")

    class Config:
        orm_mode = True
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
#TaiLieuNCKHSV Schemas
class TaiLieuNCKHSVBase(BaseModel):
    loai_tai_lieu: int = Field(..., description="Loại tài liệu")
    tep_tai_lieu: str = Field(..., max_length=255, description="Tệp tài liệu")
    thoi_gian_nop: datetime = Field(..., description="Thời gian nộp")
    trang_thai: int = Field(..., description="Trạng thái")
    phan_hoi: Optional[str] = Field(None, max_length=255, description="Phản hồi")
    ma_de_tai: int = Field(..., description="Mã đề tài")
class TaiLieuNCKHSVCreate(TaiLieuNCKHSVBase):
    pass
class TaiLieuNCKHSVUpdate(BaseModel):
    loai_tai_lieu: Optional[int] = Field(None, description="Loại tài liệu")
    tep_tai_lieu: Optional[str] = Field(None, max_length=255, description="Tệp tài liệu")
    thoi_gian_nop: Optional[datetime] = Field(None, description="Thời gian nộp")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    phan_hoi: Optional[str] = Field(None, max_length=255, description="Phản hồi")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài")
class TaiLieuNCKHSV(TaiLieuNCKHSVBase):
    ma_tai_lieu: int = Field(..., description="Mã tài liệu")

    class Config:
        orm_mode = True
#NCKH Giang Vien
#DeTaiNCKHGV Schemas
class DeTaiNCKHGVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
    thoi_gian_bat_dau: date = Field(..., description="Thời gian bắt đầu")
    thoi_han_nghiem_thu: date = Field(..., description="Thời hạn nghiệm thu")
    thoi_gian_thuc_nghiem: Optional[date] = Field(None, description="Thời gian thực nghiệm")
    trang_thai: int = Field(..., description="Trạng thái")

class DeTaiNCKHGVCreate(DeTaiNCKHGVBase):
    pass
class DeTaiNCKHGVUpdate(BaseModel):
    ten_de_tai: Optional[str] = Field(None, max_length=255, description="Tên đề tài")
    thoi_gian_bat_dau: Optional[date] = Field(None, description="Thời gian bắt đầu")
    thoi_han_nghiem_thu: Optional[date] = Field(None, description="Thời hạn nghiệm thu")
    thoi_gian_thuc_nghiem: Optional[date] = Field(None, description="Thời gian thực nghiệm")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
class DeTaiNCKHGV(DeTaiNCKHGVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài")

    class Config:
        orm_mode = True
#TaiLieuNCKHGV Schemas
class TaiLieuNCKHGVBase(BaseModel):
    loai_tai_lieu: int = Field(..., description="Loại tài liệu")
    tep_tai_lieu: str = Field(..., max_length=255, description="Tệp tài liệu")
    thoi_gian_nop: datetime = Field(..., description="Thời gian nộp")
    trang_thai: int = Field(..., description="Trạng thái")
    phan_hoi: Optional[str] = Field(None, max_length=255, description="Phản hồi")
    ma_de_tai: int = Field(..., description="Mã đề tài")
class TaiLieuNCKHGVCreate(TaiLieuNCKHGVBase):
    pass
class TaiLieuNCKHGVUpdate(BaseModel):
    loai_tai_lieu: Optional[int] = Field(None, description="Loại tài liệu")
    tep_tai_lieu: Optional[str] = Field(None, max_length=255, description="Tệp tài liệu")
    thoi_gian_nop: Optional[datetime] = Field(None, description="Thời gian nộp")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    phan_hoi: Optional[str] = Field(None, max_length=255, description="Phản hồi")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài")
class TaiLieuNCKHGV(TaiLieuNCKHGVBase):
    ma_tai_lieu: int = Field(..., description="Mã tài liệu")

    class Config:
        orm_mode = True
#ThanhVienDeTaiNCKHGV Schemas
class ThanhVienDeTaiNCKHGVBase(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    vi_tri_tham_du: bool = Field(..., description="Vị trí tham dự")
class ThanhVienDeTaiNCKHGVCreate(ThanhVienDeTaiNCKHGVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài")
class ThanhVienDeTaiNCKHGVUpdate(BaseModel):
    vi_tri_tham_du: Optional[bool] = Field(None, description="Vị trí tham dự")
class ThanhVienDeTaiNCKHGV(ThanhVienDeTaiNCKHGVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài")

    class Config:
        orm_mode = True