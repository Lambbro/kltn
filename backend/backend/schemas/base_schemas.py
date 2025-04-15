from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

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

class TaiKhoanLogin(BaseModel):
    email: str = Field(..., max_length=50, description="Email tài khoản")
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
    ngay_sinh: date = Field(..., description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    lop_hc: str = Field(..., max_length=15, description="Lớp hành chính")
    khoa_hoc: int = Field(..., description="Khóa học")
    email: Optional[str] = Field(None, max_length=50, description="Email tài khoản")  
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")
class SinhVienCreate(SinhVienBase):
    pass

class SinhVienCreateReal(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=255, description="Tên sinh viên")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính")
    ngay_sinh: date = Field(..., description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    lop_hc: str = Field(..., max_length=15, description="Lớp hành chính")
    khoa_hoc: int = Field(..., description="Khóa học")
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")

class SinhVienUpdate(BaseModel):
    ten_sv: Optional[str] = Field(None, max_length=255, description="Tên sinh viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[date] = Field(None, description="Ngày sinh")
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
    ngay_sinh: date = Field(..., description="Ngày sinh") 
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    don_vi_cong_tac: Optional[str] = Field(None, max_length=255, description="Đơn vị công tác")
    dia_chi_cong_tac: Optional[str] = Field(None, description="Địa chỉ công tác")
    email: Optional[str] = Field(None, max_length=50, description="Email tài khoản")  
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")  

class GiangVienCreate(GiangVienBase):
    quyen_han: int = Field(..., description="Quyền hạn (ví dụ: 1: PhongKHDN, 2: ToNCKH, 3: GV, 4: SV)")
    pass

class GiangVienUpdate(BaseModel):
    ten_gv: Optional[str] = Field(None, max_length=255, description="Tên giảng viên")
    anh_dai_dien: Optional[str] = Field(None, description="Ảnh đại diện")
    cccd: Optional[str] = Field(None, max_length=12, description="Căn cước công dân")
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[date] = Field(None, description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[str] = Field(None, max_length=10, description="Số điện thoại")
    don_vi_cong_tac: Optional[str] = Field(None, max_length=255, description="Đơn vị công tác")
    dia_chi_cong_tac: Optional[str] = Field(None, description="Địa chỉ công tác")
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


'''
Schemas đề tài sinh viên
'''
# Schema cho Nguyện Vọng Đăng Ký
class NguyenVongDKBase(BaseModel):
    ma_gv: str = Field(..., min_length=1, max_length=20, description="Mã giảng viên")
    muc_uu_tien: int = Field(..., ge=1, le=5, description="Mức ưu tiên từ 1 đến 5")
    trang_thai: int = Field(1, description="Trạng thái")

class NguyenVongDKCreate(NguyenVongDKBase):
    pass

class NguyenVongDKUpdate(BaseModel):
    ma_gv: Optional[str] = Field(..., min_length=1, max_length=20, description="Mã giảng viên")
    muc_uu_tien: Optional[int] = Field(None, ge=1, le=5, description="Mức ưu tiên từ 1 đến 5")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")

class NguyenVongDKResponse(NguyenVongDKBase):
    ma_dk: int = Field(..., description="Mã đăng ký NCKH")

    class Config:
        from_attributes = True

# Schema cho Đăng Ký NCKH
class DangKyNCKHBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    trang_thai: int = Field(1, description="Trạng thái đăng ký")
class DangKyNCKHCreate(DangKyNCKHBase):
    pass

class DangKyNCKHUpdate(DangKyNCKHBase):
    trang_thai: Optional[int] = Field(None, description="Trạng thái đăng ký")

class DangKyNCKHResponse(DangKyNCKHBase):
    ma_dk: int = Field(..., description="Mã đăng ký")

    class Config:
        from_attributes = True

#Đề tài NCKH sinh viên schemas
class DeTaiNCKHSVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
    dot_thuc_hien: int = Field(..., description="Đợt thực hiện")
    trang_thai: int = Field(1, description="Trạng thái đề tài")
    tien_do: int = Field(1, description="Tiến độ thực hiện")
    diem_so: Optional[int] = Field(None, description="Điểm số của đề tài") 

class DeTaiNCKHSVCreate(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
    dot_thuc_hien: int = Field(default_factory=lambda: datetime.now().year, description="Đợt thực hiện")
    trang_thai: int = Field(default=1, description="Trạng thái đề tài")
    tien_do: int = Field(default=1, description="Tiến độ thực hiện")

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
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên hướng dẫn")
    trang_thai: int = Field(1, description="Trạng thái nhóm NCKH")
    ma_de_tai: Optional[int] = Field(None, description="Mã đề tài NCKH")

class NhomNCKHCreate(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên hướng dẫn")

class NhomNCKHUpdate(BaseModel):
    trang_thai: Optional[int] = Field(1, description="Trạng thái nhóm NCKH")

class NhomNCKHResponse(NhomNCKHBase):
    ma_nhom: int = Field(..., description="Mã nhóm NCKH")

    class Config:
        from_attributes = True

'''
Đề tài giảng viên
'''
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

'''
Hội đồng nghiên cứu khoa học các cấp
'''
#Hội Đồng Khoa schemas
class HoiDongKhoaBase(BaseModel):
    so_hd: Optional[int] = Field(None, description="Số hội đồng")
    loai_hd: int = Field(..., description="Loại hội đồng")
    ngay_bao_cao: Optional[date] = Field(None, description="Ngày báo cáo")
    dia_diem: Optional[str] = Field(None, description="Địa điểm")
    trang_thai: Optional[int] = Field(None, description="Trạng thái hội đồng")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

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