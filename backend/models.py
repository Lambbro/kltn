from sqlalchemy import Column, Enum, Integer, String, Date, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Bảng trung gian
gv_hnc_table = Table(
    "GVHuongNghienCuu", Base.metadata,
    Column("ma_gv", String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True),
    Column("ma_huong_nc", String(20), ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True)
)

thanhvien_nhomNCKH_table = Table(
    "ThanhVienNhomNCKH", Base.metadata,
    Column("ma_nhom", String(20), ForeignKey("NhomNCKH.ma_nhom"), primary_key=True),
    Column("ma_sv", String(20), ForeignKey("SinhVien.ma_sv"), primary_key=True)
)

hnc_dangkynckh_table = Table(
    "HuongNghienCuuDangKyNCKH", Base.metadata,
    Column("ma_dk", String(20), ForeignKey("DangKyNCKH.ma_dk"), primary_key=True),
    Column("ma_huong_nc", String(20), ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True)
)

hnc_detaisv_table = Table(
    "HuongNghienCuuDeTaiSV", Base.metadata,
    Column("ma_huong_nc", String(20), ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True),
    Column("ma_de_tai", String(20), ForeignKey("DeTaiNCKHSV.ma_de_tai"), primary_key=True)
)

hnc_detaigv_table = Table(
    "HuongNghienCuuDeTaiGV", Base.metadata,
    Column("ma_huong_nc", String(20), ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True),
    Column("ma_de_tai", String(20), ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
)

# MODEL CHÍNH
class Khoa(Base):
    __tablename__ = "Khoa"

    ma_khoa = Column(String(20), primary_key=True)
    ten_khoa = Column(String(100), nullable=False)
    dia_chi = Column(String(150), nullable=True)

    sinh_vien = relationship("SinhVien", back_populates="khoa")
    giang_vien = relationship("GiangVien", back_populates="khoa")
    de_tai_nckh_sv = relationship("DeTaiNCKHSV", back_populates="khoa")

class HuongNghienCuu(Base):
    __tablename__ = "HuongNghienCuu"

    ma_huong_nc = Column(String(20), primary_key=True)
    ten_huong_nc = Column(String(150), nullable=False)

    dang_ky_nckh = relationship("DangKyNCKH", secondary=hnc_dangkynckh_table, back_populates="huong_nghien_cuu")
    de_tai_sv = relationship("DeTaiNCKHSV", secondary=hnc_detaisv_table, back_populates="huong_nghien_cuu")
    de_tai_gv = relationship("DeTaiNCKHGV", secondary=hnc_detaigv_table, back_populates="huong_nghien_cuu")
    giang_vien = relationship("GiangVien", secondary=gv_hnc_table, back_populates="huong_nghien_cuu")

class TaiKhoan(Base):
    __tablename__ = "TaiKhoan"

    email = Column(String(50), primary_key=True)
    mat_khau = Column(String(255), nullable=False)  # hashed
    quyen_han = Column(Enum("admin", "phong_qlkh_dn", "to_nckh", "giang_vien", "sinh_vien"), nullable=False)

    sinh_vien = relationship("SinhVien", back_populates="tai_khoan")
    giang_vien = relationship("GiangVien", back_populates="tai_khoan")

class SinhVien(Base):
    __tablename__ = "SinhVien"
    
    ma_sv = Column(String(20), primary_key=True)
    ten_sv = Column(String(100), nullable=False)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String(150), nullable=True)
    sdt = Column(String(15), unique=True, nullable=True)
    lop_hanh_chinh = Column(String(50), nullable=False)
    khoa_hoc = Column(String(10), nullable=False)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="sinh_vien")
    tai_khoan = relationship("TaiKhoan", back_populates="sinh_vien")
    dang_ky_nckh = relationship("DangKyNCKH", back_populates="sinh_vien")
    nhom_nckh = relationship("NhomNCKH", secondary=thanhvien_nhomNCKH_table, back_populates="thanh_vien")

class GiangVien(Base):
    __tablename__ = "GiangVien"

    ma_gv = Column(String(20), primary_key=True)
    ten_gv = Column(String(100), nullable=False)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String(150), nullable=True)
    sdt = Column(String(15), unique=True, nullable=True)
    don_vi_cong_tac = Column(String(150), nullable=True)
    dia_chi_cong_tac = Column(String(150), nullable=True)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="giang_vien")
    tai_khoan = relationship("TaiKhoan", back_populates="giang_vien")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=gv_hnc_table, back_populates="giang_vien")
    nhom_nckh = relationship("NhomNCKH", back_populates="giang_vien")
    nguyen_vong_dk = relationship("NguyenVongDangKyNCKH", back_populates="giang_vien")
    de_tai_gv_thanh_vien = relationship("ThanhVienDeTaiNCKHGV", back_populates="giang_vien")
    hoc_vi = relationship("HocVi", back_populates="giang_vien")
    chuc_danh_kh = relationship("ChucDanhKhoaHoc", back_populates="giang_vien")
    trinh_do_hv = relationship("TrinhDoHocVan", back_populates="giang_vien")
    khoa_dao_tao = relationship("KhoaDaoTao", back_populates="giang_vien")
    trinh_do_nn = relationship("TrinhDoNgoaiNgu", back_populates="giang_vien")
    qua_trinh_ct = relationship("QuaTrinhCongTac", back_populates="giang_vien")
    sach_bao_cn = relationship("SachBaoCongNghe", back_populates="giang_vien")
    phat_minh_sc = relationship("PhatMinhSangChe", back_populates="giang_vien")
    de_tai_khcn = relationship("DeTaiKHCN", back_populates="giang_vien")
    giai_thuong_khcn = relationship("GiaiThuongKHCN", back_populates="giang_vien")
    hoat_dong_ch = relationship("HoatDongCaoHoc", back_populates="giang_vien")
    hoat_dong_gd = relationship("HoatDongGiangDay", back_populates="giang_vien")

# MODEL ĐỀ TÀI NCKH SINH VIÊN
class DeTaiNCKHSV(Base):
    __tablename__ = "DeTaiNCKHSV"

    ma_de_tai = Column(String(20), primary_key=True)
    ten_de_tai = Column(String(150), nullable=False)
    thuong_cap_khoa = Column(String(150), nullable=True)
    thuong_cap_truong = Column(String(150), nullable=True)
    dot_thuc_hien = Column(String(50), nullable=False)
    trang_thai = Column(Enum("dang cho", "da huy", "dang thuc hien", "da hoan thanh"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="de_tai_nckh_sv")
    tai_lieu_sv = relationship("TaiLieuNCKHSinhVien", back_populates="de_tai_sv", cascade="all, delete-orphan")
    nhom_nckh = relationship("NhomNCKH", back_populates="de_tai")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaisv_table, back_populates="de_tai_sv")

class TaiLieuNCKHSinhVien(Base):
    __tablename__ = "TaiLieuNCKHSinhVien"

    ma_tai_lieu = Column(String(20), primary_key=True)
    loai_tai_lieu = Column(Enum("DeCuong", "BaoCao"), nullable=False)
    tep_tai_lieu = Column(String(150), nullable=False)
    thoi_gian_nop = Column(DateTime, nullable=False)
    trang_thai = Column(Enum("DangCho", "Duyet", "ChinhSua", "Huy"), nullable=False)
    phan_hoi = Column(String(250), nullable=True)
    ma_de_tai = Column(String(20), ForeignKey("DeTaiNCKHSV.ma_de_tai"), nullable=False)    

    de_tai_sv = relationship("DeTaiNCKHSV", back_populates="tai_lieu_sv")

class DangKyNCKH(Base):
    __tablename__ = "DangKyNCKH"

    ma_dk = Column(String(20), primary_key=True)
    ma_sv = Column(String(20), ForeignKey("SinhVien.ma_sv"), nullable=False)

    sinh_vien = relationship("SinhVien", back_populates="dang_ky_nckh")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_dangkynckh_table, back_populates="dang_ky_nckh")
    nguyen_vong = relationship("NguyenVongDangKyNCKH", back_populates="dang_ky_nckh")

class NhomNCKH(Base):
    __tablename__ = "NhomNCKH"
    
    ma_nhom = Column(String(20), primary_key=True)
    trang_thai = Column(Enum("DangCho", "DangThucHien", "DaHuy", "DaHoanThanh"), nullable=False)
    ma_de_tai = Column(String(20), ForeignKey("DeTaiNCKHSV.ma_de_tai"), nullable=False)    
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    de_tai = relationship("DeTaiNCKHSV", back_populates="nhom_nckh")
    giang_vien = relationship("GiangVien", back_populates="nhom_nckh")
    thanh_vien = relationship("SinhVien", secondary=thanhvien_nhomNCKH_table, back_populates="nhom_nckh")

# MODEL ĐỀ TÀI NCKH GIẢNG VIÊN
class DeTaiNCKHGV(Base):
    __tablename__ = "DeTaiNCKHGiangVien"

    ma_de_tai = Column(String(20), primary_key=True)
    ten_de_tai = Column(String(150), nullable=False)
    thoi_gian_bat_dau = Column(Date, nullable=False)
    thoi_han_nghiem_thu = Column(Date, nullable=False)
    thoi_gian_thuc_nghiem = Column(Date, nullable=True)
    trang_thai = Column(Enum("dang thuc hien", "da huy", "qua han", "da nghiem thu"), nullable=False)

    tai_lieu_gv = relationship("TaiLieuNCKHGV", back_populates="de_tai_gv")
    thanh_vien = relationship("ThanhVienDeTaiNCKHGV", back_populates="de_tai_gv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaigv_table, back_populates="de_tai_gv")

class TaiLieuNCKHGV(Base):
    __tablename__ = "TaiLieuNCKHGiangVien"
    
    ma_tai_lieu = Column(String(20), primary_key=True)
    loai_tai_lieu = Column(Enum("DeCuong", "ThuyetMinh", "BaoCaoTienDo", "HoSoNghiemThu"), nullable=False)
    tep_tai_lieu = Column(String(150), nullable=False)
    thoi_gian_nop = Column(DateTime, nullable=False)
    trang_thai = Column(Enum("DangCho", "Duyet", "ChinhSua", "Huy"), nullable=False)
    phan_hoi = Column(String(250), nullable=True)
    ma_de_tai = Column(String(20), ForeignKey("DeTaiNCKHGiangVien.ma_de_tai"), nullable=False)    

    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="tai_lieu_gv")

# MODEL THÔNG TIN SƠ YẾU LÝ LỊCH KHOA HỌC
class HocVi(Base):
    __tablename__ = "HocVi"

    ma_hoc_vi = Column(String(20), primary_key=True)
    hoc_vi = Column(Enum("CuNhan", "KySu", "ThacSi", "TienSi", "TienSiKhoaHoc"), nullable=False)
    nam_dat = Column(Integer, nullable=False)
    nganh = Column(String(100), nullable=False)
    chuyen_nganh = Column(String(100), nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoc_vi")

class ChucDanhKhoaHoc(Base):
    __tablename__ = "ChucDanhKhoaHoc"

    ma_cdkh = Column(String(20), primary_key=True)  # Sửa primary_key=False thành True
    chuc_danh = Column(String(25), nullable=False)
    chuc_vu = Column(String(50), nullable=True)
    nam_pgs = Column(Integer, nullable=True)
    nam_gs = Column(Integer, nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="chuc_danh_kh")

class TrinhDoHocVan(Base):
    __tablename__ = "TrinhDoHocVan"

    ma_tdhv = Column(String(20), primary_key=True)
    bac_dao_tao = Column(Enum("CuNhan", "KySu", "ThacSi", "TienSi", "TienSiKhoaHoc"), nullable=False)
    chuyen_nganh = Column(String(50), nullable=False)
    noi_dao_tao = Column(String(150), nullable=False)
    nam_tot_nghiep = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="trinh_do_hv")

class KhoaDaoTao(Base):
    __tablename__ = "KhoaDaoTao"

    ma_khoa_dao_tao = Column(String(20), primary_key=True)
    ten_khoa = Column(String(100), nullable=False)
    noi_dao_tao = Column(String(150), nullable=False)
    thoi_gian_dao_tao = Column(String(20), nullable=False)
    chung_chi = Column(String(20), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="khoa_dao_tao")

class TrinhDoNgoaiNgu(Base):
    __tablename__ = "TrinhDoNgoaiNgu"

    ma_nn = Column(String(20), primary_key=True)
    ngoai_ngu = Column(String(20), nullable=False)
    nghe = Column(Enum("Kem", "Kha", "Tot"), nullable=False)
    noi = Column(Enum("Kem", "Kha", "Tot"), nullable=False)
    doc = Column(Enum("Kem", "Kha", "Tot"), nullable=False)
    viet = Column(Enum("Kem", "Kha", "Tot"), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="trinh_do_nn")

class QuaTrinhCongTac(Base):
    __tablename__ = "QuaTrinhCongTac"

    ma_qtct = Column(String(20), primary_key=True)
    thoi_gian = Column(String(20), nullable=False)
    vi_tri_cong_tac = Column(String(255), nullable=False)
    linh_vuc_chuyen_mon = Column(String(255), nullable=False)
    co_quan_cong_tac = Column(String(255), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="qua_trinh_ct")

class SachBaoCongNghe(Base):
    __tablename__ = "SachBaoCongNghe"

    ma_sach = Column(String(20), primary_key=True)
    ten_sach = Column(String(50), nullable=False)
    vi_tri = Column(Enum("TacGia", "DongTG"), nullable=False)
    noi_xuat_ban = Column(String(150), nullable=False)
    nam_xuat_ban = Column(Integer, nullable=False)
    loai_sach = Column(Enum("SachChuyenKhao", "GiaoTrinh", "SachThamKhao", "SachHuongDan", "BaoTrongNuoc", "BaoNgoaiNuoc"), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="sach_bao_cn")

class PhatMinhSangChe(Base):
    __tablename__ = "PhatMinhSangChe"

    ma_pmsc = Column(String(20), primary_key=True)
    ten_pmsc = Column(String(100), nullable=False)
    thong_tin = Column(String(255), nullable=False)
    loai_phat_minh = Column(String(10), nullable=False)
    thoi_gian = Column(Date, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="phat_minh_sc")

class DeTaiKHCN(Base):
    __tablename__ = "DeTaiKHCN"

    ma_sp = Column(Integer, primary_key=True, autoincrement=True)
    ten_sp = Column(String(100), nullable=False)
    cap_co_quan_ql = Column(String(255), nullable=True)
    thoi_gian_thuc_hien = Column(Integer, nullable=True)
    trang_thai = Column(Enum("DangThucHien", "DaHuy", "DaHoanThanh"), nullable=True)
    ket_qua = Column(Enum("Dat", "KhongDat"), nullable=True)
    loai_de_tai = Column(Enum("DeTaiNhiemVu", "DeAnDuAn", "ChuongTrinh", "DuAnQuocTe"), nullable=True)
    tu_cach_tham_gia = Column(String(50), nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="de_tai_khcn")

class GiaiThuongKHCN(Base):
    __tablename__ = "GiaiThuongKHCN"

    ma_giai_thuong = Column(Integer, primary_key=True, autoincrement=True)
    noi_dung = Column(String(255), nullable=False)
    nam_tang_thuong = Column(Integer, nullable=True)
    loai_giai_thuong = Column(Enum("TrongNuoc", "QuocTe"), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="giai_thuong_khcn")

class HoatDongCaoHoc(Base):
    __tablename__ = "HoatDongCaoHoc"

    ma_hdch = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(100), nullable=False)
    vai_tro_huong_dan = Column(Enum("HD", "HD1", "HD2"), nullable=False)
    ten_nguoi_hoc = Column(String(100), nullable=False)
    co_so_dao_tao = Column(String(255), nullable=False)
    hoc_vi = Column(Enum("ThacSi", "TienSi"), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoat_dong_ch")

class HoatDongGiangDay(Base):
    __tablename__ = "HoatDongGiangDay"

    ma_hoat_dong = Column(Integer, primary_key=True, autoincrement=True)
    ten_hoc_phan = Column(String(100), nullable=False)
    chuyen_nganh = Column(String(255), nullable=False)
    trinh_do = Column(String(20), nullable=False)
    so_nam = Column(Integer, nullable=False)
    noi_day = Column(String(255), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoat_dong_gd")

# BẢNG TRUNG GIAN
class ThanhVienDeTaiNCKHGV(Base):
    __tablename__ = "ThanhVienDeTaiNCKHGV"

    ma_de_tai = Column(String(20), ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    vi_tri_tham_du = Column(Boolean, nullable=False)

    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="thanh_vien")
    giang_vien = relationship("GiangVien", back_populates="de_tai_gv_thanh_vien")

class NguyenVongDangKyNCKH(Base):
    __tablename__ = "NguyenVongDangKyNCKH"

    ma_dk = Column(String(20), ForeignKey("DangKyNCKH.ma_dk"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    muc_uu_tien = Column(Integer, nullable=False)
    trang_thai = Column(Enum("DangCho", "DaTaoNhom", "DaHuy"), nullable=False)

    dang_ky_nckh = relationship("DangKyNCKH", back_populates="nguyen_vong")
    giang_vien = relationship("GiangVien", back_populates="nguyen_vong_dk")