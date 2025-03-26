from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

#Đăng Ký NCKH schemas
class DangKyNCKHBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên đăng ký")

class DangKyNCKHCreate(DangKyNCKHBase):
    pass

class DangKyNCKHUpdate(BaseModel):
    ma_sv: Optional[str] = Field(None, max_length=20, description="Mã sinh viên đăng ký")

class DangKyNCKHResponse(DangKyNCKHBase):
    ma_dk: int = Field(..., description="Mã đăng ký nghiên cứu khoa học")

    class Config:
        from_attributes = True

#Nguyện vọng đăng ký schemas
class NguyenVongDKBase(BaseModel):
    ma_dk: int = Field(..., description="Mã đăng ký NCKH")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên hướng dẫn")
    muc_uu_tien: int = Field(..., description="Mức ưu tiên đăng ký")
    trang_thai: int = Field(1, description="Trạng thái đăng ký (1: Đang xét duyệt, 2: Được duyệt, 3: Bị từ chối)")

class NguyenVongDKCreate(NguyenVongDKBase):
    pass

class NguyenVongDKUpdate(BaseModel):
    ma_gv: Optional[str] = Field(None, max_length=20, description="Cập nhật mã giảng viên khác")
    muc_uu_tien: Optional[int] = Field(None, description="Mức ưu tiên đăng ký")
    trang_thai: Optional[int] = Field(None, description="Trạng thái đăng ký")

class NguyenVongDKResponse(NguyenVongDKBase):
    class Config:
        from_attributes = True

#Đề tài NCKH sinh viên schemas
class DeTaiNCKHSVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
    dot_thuc_hien: int = Field(..., description="Đợt thực hiện")
    trang_thai: int = Field(..., description="Trạng thái đề tài")
    tien_do: int = Field(..., description="Tiến độ thực hiện")
    diem_so: Optional[int] = Field(None, description="Điểm số của đề tài") 

class DeTaiNCKHSVCreate(DeTaiNCKHSVBase):
    pass

class DeTaiNCKHSVUpdate(BaseModel):
    ten_de_tai: Optional[str] = Field(None, max_length=255, description="Tên đề tài")
    dot_thuc_hien: Optional[int] = Field(None, description="Đợt thực hiện")
    trang_thai: Optional[int] = Field(None, description="Trạng thái đề tài")
    tien_do: Optional[int] = Field(None, description="Tiến độ thực hiện")
    diem_so: Optional[int] = Field(None, description="Điểm số của đề tài")

class DeTaiNCKHSVResponse(DeTaiNCKHSVBase):
    ma_de_tai: int = Field(..., description="Mã đề tài")

    class Config:
        from_attributes = True

#Tài liệu nckh sinh viên schemas
class TaiLieuNCKHSVBase(BaseModel):
    loai_tai_lieu: int = Field(..., description="Loại tài liệu")
    link_tep: Optional[str] = Field(None, description="Đường dẫn file")
    thoi_gian_nop: datetime = Field(..., description="Thời gian nộp tài liệu")
    trang_thai: int = Field(0, description="Trạng thái tài liệu")
    phan_hoi: Optional[str] = Field(None, description="Phản hồi từ hội đồng")
    ma_hd_khoa: Optional[int] = Field(None, description="Mã hội đồng khoa")
    ma_hd_truong: Optional[int] = Field(None, description="Mã hội đồng trường")
    ma_de_tai: int = Field(..., description="Mã đề tài NCKHSV")

class TaiLieuNCKHSVCreate(TaiLieuNCKHSVBase):
    pass

class TaiLieuNCKHSVUpdate(BaseModel):
    loai_tai_lieu: Optional[int] = Field(None, description="Loại tài liệu")
    link_tep: Optional[str] = Field(None, description="Đường dẫn file")
    thoi_gian_nop: Optional[datetime] = Field(None, description="Thời gian nộp tài liệu")
    trang_thai: Optional[int] = Field(None, description="Trạng thái tài liệu")
    phan_hoi: Optional[str] = Field(None, description="Phản hồi từ hội đồng")
    ma_hd_khoa: Optional[int] = Field(None, description="Mã hội đồng khoa")
    ma_hd_truong: Optional[int] = Field(None, description="Mã hội đồng trường")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài NCKHSV")

class TaiLieuNCKHSVResponse(TaiLieuNCKHSVBase):
    ma_tai_lieu: int = Field(..., description="Mã tài liệu")

    class Config:
        from_attributes = True

#Nhóm NCKH schemas
class NhomNCKHBase(BaseModel):
    trang_thai: int = Field(1, description="Trạng thái nhóm NCKH")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên hướng dẫn")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài NCKH")

class NhomNCKHCreate(NhomNCKHBase):
    pass

class NhomNCKHUpdate(BaseModel):
    trang_thai: Optional[int] = Field(None, description="Trạng thái nhóm NCKH")
    ma_gv: Optional[str] = Field(None, description="Mã giảng viên hướng dẫn")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài NCKH")

class NhomNCKHResponse(NhomNCKHBase):
    ma_nhom: int = Field(..., description="Mã nhóm NCKH")

    class Config:
        from_attributes = True