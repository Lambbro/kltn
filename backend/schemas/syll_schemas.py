from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# Khoa Schemas
class KhoaBase(BaseModel):
    ma_khoa: str = Field(..., max_length=20, description="Mã khoa")
    ten_khoa: str = Field(..., max_length=255, description="Tên khoa")
    dia_chi: Optional[str] = Field(None, max_length=255, description="Địa chỉ khoa")

class KhoaCreate(KhoaBase):
    pass

class KhoaUpdate(BaseModel):
    ten_khoa: Optional[str] = Field(None, max_length=255, description="Tên khoa")
    dia_chi: Optional[str] = Field(None, max_length=255, description="Địa chỉ khoa")

class Khoa(KhoaBase):
    class Config:
        orm_mode = True

# HuongNghienCuu Schemas
class HuongNghienCuuBase(BaseModel):
    ten_huong_nc: str = Field(..., max_length=255, description="Tên hướng nghiên cứu")

class HuongNghienCuuCreate(HuongNghienCuuBase):
    pass

class HuongNghienCuuUpdate(BaseModel):
    ten_huong_nc: Optional[str] = Field(None, max_length=255, description="Tên hướng nghiên cứu")

class HuongNghienCuu(HuongNghienCuuBase):
    ma_huong_nc: int = Field(..., description="Mã hướng nghiên cứu")

    class Config:
        orm_mode = True

# TaiKhoan Schemas
class TaiKhoanBase(BaseModel):
    email: str = Field(..., max_length=50, description="Email tài khoản")
    mat_khau: str = Field(..., max_length=255, description="Mật khẩu (đã hash)")
    quyen_han: int = Field(..., description="Quyền hạn")

class TaiKhoanCreate(TaiKhoanBase):
    pass

class TaiKhoanUpdate(BaseModel):
    mat_khau: Optional[str] = Field(None, max_length=255, description="Mật khẩu (đã hash)")
    quyen_han: Optional[int] = Field(None, description="Quyền hạn")

class TaiKhoan(TaiKhoanBase):
    class Config:
        orm_mode = True

# SinhVien Schemas
class SinhVienBase(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=100, description="Tên sinh viên")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính")
    ngay_sinh: date = Field(..., description="Ngày sinh")
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
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[date] = Field(None, description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    lop_hanh_chinh: Optional[str] = Field(None, max_length=15, description="Lớp hành chính")
    khoa_hoc: Optional[int] = Field(None, description="Khóa học")
    email: Optional[str] = Field(None, max_length=50, description="Email")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class SinhVien(SinhVienBase):
    class Config:
        orm_mode = True

# GiangVien Schemas
class GiangVienBase(BaseModel):
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")
    ten_gv: str = Field(..., max_length=100, description="Tên giảng viên")
    cccd: str = Field(..., max_length=12, description="Căn cước công dân")
    gioi_tinh: bool = Field(..., description="Giới tính")
    ngay_sinh: date = Field(..., description="Ngày sinh")
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
    gioi_tinh: Optional[bool] = Field(None, description="Giới tính")
    ngay_sinh: Optional[date] = Field(None, description="Ngày sinh")
    que_quan: Optional[str] = Field(None, max_length=255, description="Quê quán")
    sdt: Optional[int] = Field(None, description="Số điện thoại")
    don_vi_cong_tac: Optional[str] = Field(None, max_length=255, description="Đơn vị công tác")
    dia_chi_cong_tac: Optional[str] = Field(None, max_length=255, description="Địa chỉ công tác")
    email: Optional[str] = Field(None, max_length=50, description="Email")
    ma_khoa: Optional[str] = Field(None, max_length=20, description="Mã khoa")

class GiangVien(GiangVienBase):
    class Config:
        orm_mode = True

# DeTaiNCKHSV Schemas
class DeTaiNCKHSVBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
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

# TaiLieuNCKHSV Schemas
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

# DangKyNCKH Schemas
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

# NhomNCKH Schemas
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

# DeTaiNCKHGV Schemas
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

# TaiLieuNCKHGV Schemas
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

# HocVi Schemas
class HocViBase(BaseModel):
    hoc_vi: int = Field(..., description="Học vị")
    nam_dat: int = Field(..., description="Năm đạt")
    nganh: str = Field(..., max_length=255, description="Ngành")
    chuyen_nganh: Optional[str] = Field(None, max_length=255, description="Chuyên ngành")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class HocViCreate(HocViBase):
    pass

class HocViUpdate(BaseModel):
    hoc_vi: Optional[int] = Field(None, description="Học vị")
    nam_dat: Optional[int] = Field(None, description="Năm đạt")
    nganh: Optional[str] = Field(None, max_length=255, description="Ngành")
    chuyen_nganh: Optional[str] = Field(None, max_length=255, description="Chuyên ngành")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class HocVi(HocViBase):
    ma_hoc_vi: int = Field(..., description="Mã học vị")

    class Config:
        orm_mode = True

# ChucDanhKhoaHoc Schemas
class ChucDanhKhoaHocBase(BaseModel):
    chuc_danh: str = Field(..., max_length=255, description="Chức danh")
    chuc_vu: Optional[str] = Field(None, max_length=255, description="Chức vụ")
    nam_pgs: Optional[int] = Field(None, description="Năm PGS")
    nam_gs: Optional[int] = Field(None, description="Năm GS")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class ChucDanhKhoaHocCreate(ChucDanhKhoaHocBase):
    pass

class ChucDanhKhoaHocUpdate(BaseModel):
    chuc_danh: Optional[str] = Field(None, max_length=255, description="Chức danh")
    chuc_vu: Optional[str] = Field(None, max_length=255, description="Chức vụ")
    nam_pgs: Optional[int] = Field(None, description="Năm PGS")
    nam_gs: Optional[int] = Field(None, description="Năm GS")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class ChucDanhKhoaHoc(ChucDanhKhoaHocBase):
    ma_cdkh: int = Field(..., description="Mã chức danh khoa học")

    class Config:
        orm_mode = True

# TrinhDoHocVan Schemas
class TrinhDoHocVanBase(BaseModel):
    bac_dao_tao: int = Field(..., description="Bậc đào tạo")
    chuyen_nganh: str = Field(..., max_length=255, description="Chuyên ngành")
    noi_dao_tao: str = Field(..., max_length=255, description="Nơi đào tạo")
    nam_tot_nghiep: int = Field(..., description="Năm tốt nghiệp")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class TrinhDoHocVanCreate(TrinhDoHocVanBase):
    pass

class TrinhDoHocVanUpdate(BaseModel):
    bac_dao_tao: Optional[int] = Field(None, description="Bậc đào tạo")
    chuyen_nganh: Optional[str] = Field(None, max_length=255, description="Chuyên ngành")
    noi_dao_tao: Optional[str] = Field(None, max_length=255, description="Nơi đào tạo")
    nam_tot_nghiep: Optional[int] = Field(None, description="Năm tốt nghiệp")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class TrinhDoHocVan(TrinhDoHocVanBase):
    ma_tdhv: int = Field(..., description="Mã trình độ học vấn")

    class Config:
        orm_mode = True

# KhoaDaoTao Schemas
class KhoaDaoTaoBase(BaseModel):
    ten_khoa: str = Field(..., max_length=100, description="Tên khóa")
    noi_dao_tao: str = Field(..., max_length=255, description="Nơi đào tạo")
    thoi_gian_dao_tao: str = Field(..., max_length=255, description="Thời gian đào tạo")
    chung_chi: int = Field(..., description="Chứng chỉ")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class KhoaDaoTaoCreate(KhoaDaoTaoBase):
    pass

class KhoaDaoTaoUpdate(BaseModel):
    ten_khoa: Optional[str] = Field(None, max_length=100, description="Tên khóa")
    noi_dao_tao: Optional[str] = Field(None, max_length=255, description="Nơi đào tạo")
    thoi_gian_dao_tao: Optional[str] = Field(None, max_length=255, description="Thời gian đào tạo")
    chung_chi: Optional[int] = Field(None, description="Chứng chỉ")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class KhoaDaoTao(KhoaDaoTaoBase):
    ma_khoa_dao_tao: int = Field(..., description="Mã khóa đào tạo")

    class Config:
        orm_mode = True

# TrinhDoNgoaiNgu Schemas
class TrinhDoNgoaiNguBase(BaseModel):
    ngoai_ngu: str = Field(..., max_length=100, description="Ngoại ngữ")
    nghe: int = Field(..., description="Nghe")
    noi: int = Field(..., description="Nói")
    doc: int = Field(..., description="Đọc")
    viet: int = Field(..., description="Viết")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class TrinhDoNgoaiNguCreate(TrinhDoNgoaiNguBase):
    pass

class TrinhDoNgoaiNguUpdate(BaseModel):
    ngoai_ngu: Optional[str] = Field(None, max_length=100, description="Ngoại ngữ")
    nghe: Optional[int] = Field(None, description="Nghe")
    noi: Optional[int] = Field(None, description="Nói")
    doc: Optional[int] = Field(None, description="Đọc")
    viet: Optional[int] = Field(None, description="Viết")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class TrinhDoNgoaiNgu(TrinhDoNgoaiNguBase):
    ma_nn: int = Field(..., description="Mã ngoại ngữ")

    class Config:
        orm_mode = True

# QuaTrinhCongTac Schemas
class QuaTrinhCongTacBase(BaseModel):
    thoi_gian: str = Field(..., max_length=255, description="Thời gian")
    vi_tri_cong_tac: str = Field(..., max_length=255, description="Vị trí công tác")
    linh_vuc_chuyen_mon: str = Field(..., max_length=255, description="Lĩnh vực chuyên môn")
    co_quan_cong_tac: str = Field(..., max_length=255, description="Cơ quan công tác")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class QuaTrinhCongTacCreate(QuaTrinhCongTacBase):
    pass

class QuaTrinhCongTacUpdate(BaseModel):
    thoi_gian: Optional[str] = Field(None, max_length=255, description="Thời gian")
    vi_tri_cong_tac: Optional[str] = Field(None, max_length=255, description="Vị trí công tác")
    linh_vuc_chuyen_mon: Optional[str] = Field(None, max_length=255, description="Lĩnh vực chuyên môn")
    co_quan_cong_tac: Optional[str] = Field(None, max_length=255, description="Cơ quan công tác")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class QuaTrinhCongTac(QuaTrinhCongTacBase):
    ma_qtct: int = Field(..., description="Mã quá trình công tác")

    class Config:
        orm_mode = True

# SachBaoCongNghe Schemas
class SachBaoCongNgheBase(BaseModel):
    ten_sach: str = Field(..., max_length=100, description="Tên sách")
    vi_tri: bool = Field(..., description="Vị trí")
    noi_xuat_ban: str = Field(..., max_length=255, description="Nơi xuất bản")
    nam_xuat_ban: int = Field(..., description="Năm xuất bản")
    loai_sach: int = Field(..., description="Loại sách")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class SachBaoCongNgheCreate(SachBaoCongNgheBase):
    pass

class SachBaoCongNgheUpdate(BaseModel):
    ten_sach: Optional[str] = Field(None, max_length=100, description="Tên sách")
    vi_tri: Optional[bool] = Field(None, description="Vị trí")
    noi_xuat_ban: Optional[str] = Field(None, max_length=255, description="Nơi xuất bản")
    nam_xuat_ban: Optional[int] = Field(None, description="Năm xuất bản")
    loai_sach: Optional[int] = Field(None, description="Loại sách")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class SachBaoCongNghe(SachBaoCongNgheBase):
    ma_sach: int = Field(..., description="Mã sách")

    class Config:
        orm_mode = True

# PhatMinhSangChe Schemas
class PhatMinhSangCheBase(BaseModel):
    ten_pmsc: str = Field(..., max_length=100, description="Tên phát minh sáng chế")
    loai_phat_minh: str = Field(..., max_length=10, description="Loại phát minh")
    thong_tin: str = Field(..., max_length=255, description="Thông tin")
    thoi_gian: date = Field(..., description="Thời gian")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class PhatMinhSangCheCreate(PhatMinhSangCheBase):
    pass

class PhatMinhSangCheUpdate(BaseModel):
    ten_pmsc: Optional[str] = Field(None, max_length=100, description="Tên phát minh sáng chế")
    loai_phat_minh: Optional[str] = Field(None, max_length=10, description="Loại phát minh")
    thong_tin: Optional[str] = Field(None, max_length=255, description="Thông tin")
    thoi_gian: Optional[date] = Field(None, description="Thời gian")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class PhatMinhSangChe(PhatMinhSangCheBase):
    ma_pmsc: int = Field(..., description="Mã phát minh sáng chế")

    class Config:
        orm_mode = True

# DeTaiKHCN Schemas
class DeTaiKHCNBase(BaseModel):
    ten_sp: str = Field(..., max_length=255, description="Tên sản phẩm")
    cap_co_quan_ql: Optional[str] = Field(None, max_length=255, description="Cấp cơ quan quản lý")
    thoi_gian_thuc_hien: Optional[str] = Field(None, max_length=255, description="Thời gian thực hiện")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    ket_qua: Optional[int] = Field(None, description="Kết quả")
    loai_de_tai: Optional[int] = Field(None, description="Loại đề tài")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class DeTaiKHCNCreate(DeTaiKHCNBase):
    pass

class DeTaiKHCNUpdate(BaseModel):
    ten_sp: Optional[str] = Field(None, max_length=255, description="Tên sản phẩm")
    cap_co_quan_ql: Optional[str] = Field(None, max_length=255, description="Cấp cơ quan quản lý")
    thoi_gian_thuc_hien: Optional[str] = Field(None, max_length=255, description="Thời gian thực hiện")
    trang_thai: Optional[int] = Field(None, description="Trạng thái")
    ket_qua: Optional[int] = Field(None, description="Kết quả")
    loai_de_tai: Optional[int] = Field(None, description="Loại đề tài")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")
# GiaiThuongKHCN Schemas
class GiaiThuongKHCNBase(BaseModel):
    noi_dung: str = Field(..., max_length=255, description="Nội dung")
    nam_tang_thuong: Optional[int] = Field(None, description="Năm tặng thưởng")
    loai_giai_thuong: bool = Field(..., description="Loại giải thưởng")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class GiaiThuongKHCNCreate(GiaiThuongKHCNBase):
    pass

class GiaiThuongKHCNUpdate(BaseModel):
    noi_dung: Optional[str] = Field(None, max_length=255, description="Nội dung")
    nam_tang_thuong: Optional[int] = Field(None, description="Năm tặng thưởng")
    loai_giai_thuong: Optional[bool] = Field(None, description="Loại giải thưởng")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class GiaiThuongKHCN(GiaiThuongKHCNBase):
    ma_giai_thuong: int = Field(..., description="Mã giải thưởng")

    class Config:
        orm_mode = True

# HoatDongCaoHoc Schemas
class HoatDongCaoHocBase(BaseModel):
    ten_de_tai: str = Field(..., max_length=100, description="Tên đề tài")
    vai_tro_huong_dan: int = Field(..., description="Vai trò hướng dẫn")
    ten_nguoi_hoc: str = Field(..., max_length=100, description="Tên người học")
    co_so_dao_tao: str = Field(..., max_length=255, description="Cơ sở đào tạo")
    hoc_vi: int = Field(..., description="Học vị")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class HoatDongCaoHocCreate(HoatDongCaoHocBase):
    pass

class HoatDongCaoHocUpdate(BaseModel):
    ten_de_tai: Optional[str] = Field(None, max_length=100, description="Tên đề tài")
    vai_tro_huong_dan: Optional[int] = Field(None, description="Vai trò hướng dẫn")
    ten_nguoi_hoc: Optional[str] = Field(None, max_length=100, description="Tên người học")
    co_so_dao_tao: Optional[str] = Field(None, max_length=255, description="Cơ sở đào tạo")
    hoc_vi: Optional[int] = Field(None, description="Học vị")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class HoatDongCaoHoc(HoatDongCaoHocBase):
    ma_hdch: int = Field(..., description="Mã hoạt động cao học")

    class Config:
        orm_mode = True

# HoatDongGiangDay Schemas
class HoatDongGiangDayBase(BaseModel):
    ten_hoc_phan: str = Field(..., max_length=100, description="Tên học phần")
    chuyen_nganh: str = Field(..., max_length=255, description="Chuyên ngành")
    trinh_do: int = Field(..., description="Trình độ")
    so_nam: int = Field(..., description="Số năm")
    noi_day: str = Field(..., max_length=255, description="Nơi dạy")
    ma_gv: str = Field(..., max_length=20, description="Mã giảng viên")

class HoatDongGiangDayCreate(HoatDongGiangDayBase):
    pass

class HoatDongGiangDayUpdate(BaseModel):
    ten_hoc_phan: Optional[str] = Field(None, max_length=100, description="Tên học phần")
    chuyen_nganh: Optional[str] = Field(None, max_length=255, description="Chuyên ngành")
    trinh_do: Optional[int] = Field(None, description="Trình độ")
    so_nam: Optional[int] = Field(None, description="Số năm")
    noi_day: Optional[str] = Field(None, max_length=255, description="Nơi dạy")
    ma_gv: Optional[str] = Field(None, max_length=20, description="Mã giảng viên")

class HoatDongGiangDay(HoatDongGiangDayBase):
    ma_hoat_dong: int = Field(..., description="Mã hoạt động")

    class Config:
        orm_mode = True