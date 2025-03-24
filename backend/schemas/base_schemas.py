from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#Khoa Schemas
class KhoaBase(BaseModel):
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
    ten_khoa: str = Field(..., max_length=255, description="Tên Khoa")
    dia_chi: Optional[str] = Field(None, description="Địa Chỉ Khoa")
class KhoaCreate(KhoaBase):
    pass
class KhoaUpdate(BaseModel):
    ten_khoa: Optional[str] = Field(None, max_length=255, description="Tên Khoa")
    dia_chi: Optional[str] = Field(None, description="Địa Chỉ Khoa")
class KhoaResponse(KhoaBase):
    class Config:
        from_attributes = True

#Hướng Nghiên Cứu schemas
class HuongNghienCuuBase(BaseModel):
    ten_hnc: str = Field(..., max_length=255, description="Tên Hướng Nghiên Cứu")
class HuongNghienCuuCreate(HuongNghienCuuBase):
    pass
class HuongNghienCuuUpdate(BaseModel):
    ten_hnc: Optional[str] = Field(None, max_length=255, description="Tên Hướng Nghiên Cứu")
class HuongNghienCuuResponse(HuongNghienCuuBase):
    ma_hnc: int = Field(..., description="Mã Hướng Nghiên Cứu")
    
    class Config:
        from_attributes = True

#Tài Khoản Schemas
class TaiKhoanBase(BaseModel):
    email: str = Field(..., max_length=50, description="Email tài khoản")
    quyen_han: int = Field(..., description="Quyền hạn (ví dụ: 1: PhongKHDN, 2: ToNCKH, 3: GV, 4: SV)")

class TaiKhoanCreate(TaiKhoanBase):
    mat_khau: str = Field(..., min_length=8, max_length=255, description="Mật khẩu (chưa hash)")

class TaiKhoanUpdate(BaseModel):
    mat_khau: Optional[str] = Field(None, min_length=8, max_length=255, description="Mật khẩu (chưa hash)")
    quyen_han: Optional[int] = Field(None, description="Quyền hạn (ví dụ: 1: PhongKHDN, 2: ToNCKH, 3: GV, 4: SV)")

class TaiKhoanResponse(TaiKhoanBase):
    class Config:
        from_attributes = True

#Khen Thưởng schemas
class KhenThuongBase(BaseModel):
    cap_do: int = Field(..., description="Cấp độ khen thưởng")
    muc_do: int = Field(..., description="Mức độ khen thưởng")

class KhenThuongCreate(KhenThuongBase):
    pass

class KhenThuongUpdate(BaseModel):
    cap_do: Optional[int] = Field(None, description="Cấp độ khen thưởng")
    muc_do: Optional[int] = Field(None, description="Mức độ khen thưởng")

class KhenThuongResponse(KhenThuongBase):
    ma_khen_thuong: int = Field(..., description="Mã khen thưởng")
    
    class Config:
        from_attributes = True

#Sinh Viên schemas
class SinhVienBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=255, description="Tên sinh viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính")
    ngay_sinh: str = Field(..., description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    lop_hc: str = Field(..., max_length=15, description="Lớp hành chính")
    khoa_hoc: int = Field(..., description="Khóa học")
    email: str = Field(..., max_length=50, description="Email tài khoản")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")

class SinhVienCreate(SinhVienBase):
    pass

class SinhVienUpdate(BaseModel):
    ten_sv: Optional[str] = Field(None, max_length=255, description="Tên sinh viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    lop_hc: Optional[str] = Field(None, max_length=15, description="Lớp hành chính")
    khoa_hoc: Optional[int] = Field(None, description="Khóa học")
    email: Optional[str] = Field(None, max_length=50, description="Email tài khoản")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class SinhVienResponse(SinhVienBase):
    class Config:
        from_attributes = True

#Giảng Viên schemas
class GiangVienBase(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    ten_gv: str = Field(..., max_length=255, description="Tên giảng viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính")
    ngay_sinh: str = Field(..., description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    email: str = Field(..., max_length=50, description="Email tài khoản")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")

class GiangVienCreate(GiangVienBase):
    pass

class GiangVienUpdate(BaseModel):
    ten_gv: Optional[str] = Field(None, max_length=255, description="Tên giảng viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    email: Optional[str] = Field(None, max_length=50, description="Email tài khoản")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class GiangVienResponse(GiangVienBase):
    class Config:
        from_attributes = True

#Thông Báo
class ThongBaoBase(BaseModel):
    tieu_de: str = Field(..., max_length=255, description="Tiêu đề thông báo")
    noi_dung: str = Field(..., description="Nội dung thông báo")
    link_tep: Optional[str] = Field(None, description="Đường dẫn tệp đính kèm")
    anh_dinh_kem: Optional[str] = Field(None, description="Ảnh đính kèm")
    thoi_gian_gui: datetime = Field(..., description="Thời gian gửi thông báo")
    email: str = Field(..., max_length=50, description="Email người gửi")

class ThongBaoCreate(ThongBaoBase):
    pass

class ThongBaoResponse(ThongBaoBase):
    ma_tb: int = Field(..., description="Mã thông báo")

    class Config:
        from_attributes = True