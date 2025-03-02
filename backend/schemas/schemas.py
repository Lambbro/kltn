from pydantic import BaseModel, Field
from typing import Optional

#Khoa Schemas
class KhoaBase(BaseModel):
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
    ten_khoa: str = Field(..., max_length=255, description="Tên Khoa")
    dia_chi: Optional[str] = Field(None, max_length=255, description="Địa Chỉ Khoa")
class KhoaCreate(KhoaBase):
    pass
class KhoaUpdate(BaseModel):
    ten_khoa: Optional[str] = Field(None, max_length=255, description="Tên Khoa")
    dia_chi: Optional[str] = Field(None, max_length=255, description="Địa Chỉ Khoa")
class Khoa(KhoaBase):
    class Config:
        orm_mode = True
#HuongNC Schemas
class HuongNghienCuuBase(BaseModel):
    ten_huong_nc = Field(..., max_length=255, description="Tên Hướng Nghiên Cứu")
class HuongNghienCuuCreate(HuongNghienCuuBase):
    pass
class HuongNghienCuuUpdate(BaseModel):
    ten_huong_nc: Optional[str] = Field(None, max_length=255, description="Tên Hướng Nghiên Cứu")
class HuongNghienCuu(HuongNghienCuuBase):
    ma_huong_nc: int = Field(..., description="Mã Hướng Nghiên Cứu")

    class Config:
        orm_mode = True
#TaiKhoan Schemas
class TaiKhoanBase(BaseModel):
    email: str = Field(..., max_length=50, description="Email Tài Khoản")
    quyen_han: int = Field(..., description="Quyền hạn (ví dụ: 0: Admin, 1: PhongQLKHDN, 2: ToNCKH, 3: GV, 4: SV)")
class TaiKhoanCreate(TaiKhoanBase):
    mat_khau: str = Field(..., min_length=8, description="Mật khẩu (chưa hash)")  # Yêu cầu mật khẩu chưa hash để tạo tài khoản
class TaiKhoanUpdate(BaseModel):
    quyen_han: Optional[int] = Field(None, description="Quyền hạn (ví dụ: 1-Admin, 2-Giảng viên, 3-Sinh viên)")
    mat_khau: Optional[str] = Field(None, min_length=8, description="Mật khẩu mới (chưa hash)")  # Cho phép cập nhật mật khẩu
class TaiKhoan(TaiKhoanBase):
    # Không bao gồm mật khẩu (đã hash hay chưa)
    class Config:
        orm_mode = True
#SinhVien Schemas
class SinhVienBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=100, description="Tên sinh viên")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính (True: Nam, False: Nữ)")
    ngay_sinh: str = Field(..., description="Ngày sinh (YYYY-MM-DD)")#Sửa kiểu Date thành str
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    lop_hanh_chinh: str = Field(..., max_length=15, description="Lớp hành chính")
    khoa_hoc: int = Field(..., description="Khóa học")
    email: str = Field(..., max_length=50, description="Email")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
class SinhVienCreate(SinhVienBase):
    pass
class SinhVienUpdate(BaseModel):
    ten_sv: Optional[str] = Field(None, max_length=100, description="Tên sinh viên")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính (True: Nam, False: Nữ)")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh (YYYY-MM-DD)")#Sửa kiểu Date thành str
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    lop_hanh_chinh: Optional[str] = Field(None, max_length=15, description="Lớp hành chính")
    khoa_hoc: Optional[int] = Field(None, description="Khóa học")
    email: Optional[str] = Field(None, max_length=50, description="Email")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class SinhVien(SinhVienBase):
    class Config:
        orm_mode = True
#GiangVien Schemas
class GiangVienBase(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    ten_gv: str = Field(..., max_length=100, description="Tên giảng viên")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính (True: Nam, False: Nữ)")
    ngay_sinh: str = Field(..., description="Ngày sinh (YYYY-MM-DD)") #Sửa kiểu Date thành str
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    don_vi_cong_tac: Optional[str] = Field(None, max_length=255, description="Đơn vị công tác")
    dia_chi_cong_tac: Optional[str] = Field(None, max_length=255, description="Địa chỉ công tác")
    email: str = Field(..., max_length=50, description="Email")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
class GiangVienCreate(GiangVienBase):
    pass
class GiangVienUpdate(BaseModel):
    ten_gv: Optional[str] = Field(None, max_length=100, description="Tên giảng viên")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính (True: Nam, False: Nữ)")
    ngay_sinh: Optional[str] = Field(None, description="Ngày sinh (YYYY-MM-DD)")#Sửa kiểu Date thành str
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    don_vi_cong_tac: Optional[str] = Field(None, max_length=255, description="Đơn vị công tác")
    dia_chi_cong_tac: Optional[str] = Field(None, max_length=255, description="Địa chỉ công tác")
    email: Optional[str] = Field(None, max_length=50, description="Email")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")
class GiangVien(GiangVienBase):
    class Config:
        orm_mode = True