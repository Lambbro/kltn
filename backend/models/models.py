from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base

# Bảng trung gian
#done
gv_hnc_table = Table(
    "GVHuongNghienCuu", Base.metadata,
    Column("ma_gv", String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True),
    Column("ma_huong_nc", Integer, ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True)
)
#done
thanhvien_nhomNCKH_table = Table(
    "ThanhVienNhomNCKH", Base.metadata,
    Column("ma_nhom", Integer, ForeignKey("NhomNCKH.ma_nhom"), primary_key=True),
    Column("ma_sv", String(20), ForeignKey("SinhVien.ma_sv"), primary_key=True)
)
#done
hnc_dangkynckh_table = Table(
    "HuongNghienCuuDangKyNCKH", Base.metadata,
    Column("ma_dk", Integer, ForeignKey("DangKyNCKH.ma_dk"), primary_key=True),
    Column("ma_huong_nc", Integer, ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True)
)
#done
hnc_detaisv_table = Table(
    "HuongNghienCuuDeTaiSV", Base.metadata,
    Column("ma_huong_nc", Integer, ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True),
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"), primary_key=True)
)
#done
hnc_detaigv_table = Table(
    "HuongNghienCuuDeTaiGV", Base.metadata,
    Column("ma_huong_nc", Integer, ForeignKey("HuongNghienCuu.ma_huong_nc"), primary_key=True),
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
)

# MODEL CHÍNH

class Khoa(Base):
    __tablename__ = "Khoa"
    # done
    ma_khoa = Column(String(20), primary_key=True)
    ten_khoa = Column(String, nullable=False)
    dia_chi = Column(String, nullable=True)
    #done
    sinh_vien = relationship("SinhVien", back_populates="khoa")
    giang_vien = relationship("GiangVien", back_populates="khoa")
    de_tai_nckh_sv = relationship("DeTaiNCKHSV", back_populates="khoa")

class HuongNghienCuu(Base):
    __tablename__ = "HuongNghienCuu"
    # done
    ma_huong_nc = Column(Integer, primary_key=True, autoincrement=True)
    ten_huong_nc = Column(String, nullable=False)

    dang_ky_nckh = relationship("DangKyNCKH", secondary=hnc_dangkynckh_table, back_populates="huong_nghien_cuu")
    de_tai_sv = relationship("DeTaiNCKHSV", secondary=hnc_detaisv_table, back_populates="huong_nghien_cuu")
    de_tai_gv = relationship("DeTaiNCKHGV", secondary=hnc_detaigv_table, back_populates="huong_nghien_cuu")
    giang_vien = relationship("GiangVien", secondary=gv_hnc_table, back_populates="huong_nghien_cuu")

class TaiKhoan(Base):
    __tablename__ = "TaiKhoan"
    # done
    email = Column(String(50), primary_key=True)
    mat_khau = Column(String(255), nullable=False)  # hashed
    quyen_han = Column(Integer, nullable=False)

    sinh_vien = relationship("SinhVien", back_populates="tai_khoan")
    giang_vien = relationship("GiangVien", back_populates="tai_khoan")

class SinhVien(Base):
    __tablename__ = "SinhVien"
    # done
    ma_sv = Column(String(20), primary_key=True)
    ten_sv = Column(String(100), nullable=False)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String, nullable=True)
    sdt = Column(Integer, unique=True, nullable=True)
    lop_hanh_chinh = Column(String(15), nullable=False)
    khoa_hoc = Column(Integer, nullable=False)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="sinh_vien")
    tai_khoan = relationship("TaiKhoan", back_populates="sinh_vien")
    dang_ky_nckh = relationship("DangKyNCKH", back_populates="sinh_vien")
    nhom_nckh = relationship("NhomNCKH", secondary=thanhvien_nhomNCKH_table, back_populates="thanh_vien")

class GiangVien(Base):
    __tablename__ = "GiangVien"
    # done
    ma_gv = Column(String(20), primary_key=True)
    ten_gv = Column(String(100), nullable=False)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String, nullable=True)
    sdt = Column(Integer, unique=True, nullable=True)
    don_vi_cong_tac = Column(String, nullable=True)
    dia_chi_cong_tac = Column(String, nullable=True)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="giang_vien")
    tai_khoan = relationship("TaiKhoan", back_populates="giang_vien")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=gv_hnc_table, back_populates="giang_vien")
    nhom_nckh = relationship("NhomNCKH", back_populates="giang_vien")
    nguyen_vong_dk = relationship("NguyenVongDangKyNCKH", back_populates="giang_vien")
    de_tai_gv_thanh_vien = relationship("ThanhVienDeTaiNCKHGV", back_populates="giang_vien")
    hoc_vi = relationship("HocVi", back_populates="giang_vien", cascade="all, delete-orphan")
    chuc_danh_kh = relationship("ChucDanhKhoaHoc", back_populates="giang_vien", cascade="all, delete-orphan")
    trinh_do_hv = relationship("TrinhDoHocVan", back_populates="giang_vien", cascade="all, delete-orphan")
    khoa_dao_tao = relationship("KhoaDaoTao", back_populates="giang_vien", cascade="all, delete-orphan")
    trinh_do_nn = relationship("TrinhDoNgoaiNgu", back_populates="giang_vien", cascade="all, delete-orphan")
    qua_trinh_ct = relationship("QuaTrinhCongTac", back_populates="giang_vien", cascade="all, delete-orphan")
    sach_bao_cn = relationship("SachBaoCongNghe", back_populates="giang_vien", cascade="all, delete-orphan")
    phat_minh_sc = relationship("PhatMinhSangChe", back_populates="giang_vien", cascade="all, delete-orphan")
    de_tai_khcn = relationship("DeTaiKHCN", back_populates="giang_vien", cascade="all, delete-orphan")
    giai_thuong_khcn = relationship("GiaiThuongKHCN", back_populates="giang_vien", cascade="all, delete-orphan")
    hoat_dong_ch = relationship("HoatDongCaoHoc", back_populates="giang_vien", cascade="all, delete-orphan")
    hoat_dong_gd = relationship("HoatDongGiangDay", back_populates="giang_vien", cascade="all, delete-orphan")

# MODEL ĐỀ TÀI NCKH SINH VIÊN
class DeTaiNCKHSV(Base):
    __tablename__ = "DeTaiNCKHSV"
    # done
    ma_de_tai = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String, nullable=False)
    thuong_cap_khoa = Column(String, nullable=True)
    thuong_cap_truong = Column(String, nullable=True)
    dot_thuc_hien = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)

    khoa = relationship("Khoa", back_populates="de_tai_nckh_sv")
    tai_lieu_sv = relationship("TaiLieuNCKHSV", back_populates="de_tai_sv", cascade="all, delete-orphan")
    nhom_nckh = relationship("NhomNCKH", back_populates="de_tai")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaisv_table, back_populates="de_tai_sv")

class TaiLieuNCKHSV(Base):
    __tablename__ = "TaiLieuNCKHSV"
    # done
    ma_tai_lieu = Column(Integer, primary_key=True, autoincrement=True)
    loai_tai_lieu = Column(Integer, nullable=False)
    tep_tai_lieu = Column(String(255), nullable=False)
    thoi_gian_nop = Column(DateTime, nullable=False)
    trang_thai = Column(Integer, nullable=False)
    phan_hoi = Column(String(255), nullable=True)
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"), nullable=False)    

    de_tai_sv = relationship("DeTaiNCKHSV", back_populates="tai_lieu_sv")

class DangKyNCKH(Base):
    __tablename__ = "DangKyNCKH"
    # done
    ma_dk = Column(Integer, primary_key=True, autoincrement=True)
    ma_sv = Column(String(20), ForeignKey("SinhVien.ma_sv"), nullable=False)

    sinh_vien = relationship("SinhVien", back_populates="dang_ky_nckh")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_dangkynckh_table, back_populates="dang_ky_nckh")
    nguyen_vong = relationship("NguyenVongDangKyNCKH", back_populates="dang_ky_nckh")

class NhomNCKH(Base):
    __tablename__ = "NhomNCKH"
    # done
    ma_nhom = Column(Integer, primary_key=True, autoincrement=True)
    trang_thai = Column(Integer, nullable=False)
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"), nullable=False)    
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    de_tai = relationship("DeTaiNCKHSV", back_populates="nhom_nckh")
    giang_vien = relationship("GiangVien", back_populates="nhom_nckh")
    thanh_vien = relationship("SinhVien", secondary=thanhvien_nhomNCKH_table, back_populates="nhom_nckh")

# MODEL ĐỀ TÀI NCKH GIẢNG VIÊN
class DeTaiNCKHGV(Base):
    __tablename__ = "DeTaiNCKHGV"
    # done
    ma_de_tai = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String, nullable=False)
    thoi_gian_bat_dau = Column(Date, nullable=False)
    thoi_han_nghiem_thu = Column(Date, nullable=False)
    thoi_gian_thuc_nghiem = Column(Date, nullable=True)
    trang_thai = Column(Integer, nullable=False)

    tai_lieu_gv = relationship("TaiLieuNCKHGV", back_populates="de_tai_gv", cascade="all, delete-orphan")
    thanh_vien = relationship("ThanhVienDeTaiNCKHGV", back_populates="de_tai_gv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaigv_table, back_populates="de_tai_gv")

class TaiLieuNCKHGV(Base):
    __tablename__ = "TaiLieuNCKHGV"
    # done
    ma_tai_lieu = Column(Integer, primary_key=True, autoincrement=True)
    loai_tai_lieu = Column(Integer, nullable=False)
    tep_tai_lieu = Column(String, nullable=False)
    thoi_gian_nop = Column(DateTime, nullable=False)
    trang_thai = Column(Integer, nullable=False)
    phan_hoi = Column(String, nullable=True)
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), nullable=False)    

    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="tai_lieu_gv")

# MODEL THÔNG TIN SƠ YẾU LÝ LỊCH KHOA HỌC
class HocVi(Base):
    __tablename__ = "HocVi"
    # done
    ma_hoc_vi = Column(Integer, primary_key=True, autoincrement=True)
    hoc_vi = Column(Integer, nullable=False)
    nam_dat = Column(Integer, nullable=False)
    nganh = Column(String(255), nullable=False)
    chuyen_nganh = Column(String(255), nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoc_vi")

class ChucDanhKhoaHoc(Base):
    __tablename__ = "ChucDanhKhoaHoc"
    # done
    ma_cdkh = Column(Integer, primary_key=True, autoincrement=True)
    chuc_danh = Column(String(255), nullable=False)
    chuc_vu = Column(String(255), nullable=True)
    nam_pgs = Column(Integer, nullable=True)
    nam_gs = Column(Integer, nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="chuc_danh_kh")

class TrinhDoHocVan(Base):
    __tablename__ = "TrinhDoHocVan"
    # done
    ma_tdhv = Column(Integer, primary_key=True, autoincrement=True)
    bac_dao_tao = Column(Integer, nullable=False)
    chuyen_nganh = Column(String(255), nullable=False)
    noi_dao_tao = Column(String(255), nullable=False)
    nam_tot_nghiep = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="trinh_do_hv")

class KhoaDaoTao(Base):
    __tablename__ = "KhoaDaoTao"
    # done
    ma_khoa_dao_tao = Column(Integer, primary_key=True, autoincrement=True)
    ten_khoa = Column(String(100), nullable=False)
    noi_dao_tao = Column(String(255), nullable=False)
    thoi_gian_dao_tao = Column(String(255), nullable=False)
    chung_chi = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="khoa_dao_tao")

class TrinhDoNgoaiNgu(Base):
    __tablename__ = "TrinhDoNgoaiNgu"
    # done
    ma_nn = Column(Integer, primary_key=True, autoincrement=True)
    ngoai_ngu = Column(String(100), nullable=False)
    nghe = Column(Integer, nullable=False)
    noi = Column(Integer, nullable=False)
    doc = Column(Integer, nullable=False)
    viet = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="trinh_do_nn")

class QuaTrinhCongTac(Base):
    __tablename__ = "QuaTrinhCongTac"
    # done
    ma_qtct = Column(Integer, primary_key=True, autoincrement=True)
    thoi_gian = Column(String(255), nullable=False)
    vi_tri_cong_tac = Column(String(255), nullable=False)
    linh_vuc_chuyen_mon = Column(String(255), nullable=False)
    co_quan_cong_tac = Column(String(255), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="qua_trinh_ct")

class SachBaoCongNghe(Base):
    __tablename__ = "SachBaoCongNghe"
    # done
    ma_sach = Column(Integer, primary_key=True, autoincrement=True)
    ten_sach = Column(String(100), nullable=False)
    vi_tri = Column(Boolean, nullable=False)
    noi_xuat_ban = Column(String(255), nullable=False)
    nam_xuat_ban = Column(Integer, nullable=False)
    loai_sach = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="sach_bao_cn")

class PhatMinhSangChe(Base):
    __tablename__ = "PhatMinhSangChe"
    # done
    ma_pmsc = Column(Integer, primary_key=True, autoincrement=True)
    ten_pmsc = Column(String(100), nullable=False)
    loai_phat_minh = Column(String(10), nullable=False)
    thong_tin = Column(String(255), nullable=False)
    thoi_gian = Column(Date, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="phat_minh_sc")

class DeTaiKHCN(Base):
    __tablename__ = "DeTaiKHCN"
    # done
    ma_sp = Column(Integer, primary_key=True, autoincrement=True)
    ten_sp = Column(String(255), nullable=False)
    cap_co_quan_ql = Column(String(255), nullable=True)
    thoi_gian_thuc_hien = Column(String(255), nullable=True)
    trang_thai = Column(Integer, nullable=True)
    ket_qua = Column(Integer, nullable=True)
    loai_de_tai = Column(Integer, nullable=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="de_tai_khcn")

class GiaiThuongKHCN(Base):
    __tablename__ = "GiaiThuongKHCN"
    # done
    ma_giai_thuong = Column(Integer, primary_key=True, autoincrement=True)
    noi_dung = Column(String(255), nullable=False)
    nam_tang_thuong = Column(Integer, nullable=True)
    loai_giai_thuong = Column(Boolean, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="giai_thuong_khcn")

class HoatDongCaoHoc(Base):
    __tablename__ = "HoatDongCaoHoc"
    # done
    ma_hdch = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(100), nullable=False)
    vai_tro_huong_dan = Column(Integer, nullable=False)
    ten_nguoi_hoc = Column(String(100), nullable=False)
    co_so_dao_tao = Column(String(255), nullable=False)
    hoc_vi = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoat_dong_ch")

class HoatDongGiangDay(Base):
    __tablename__ = "HoatDongGiangDay"
    # done
    ma_hoat_dong = Column(Integer, primary_key=True, autoincrement=True)
    ten_hoc_phan = Column(String(100), nullable=False)
    chuyen_nganh = Column(String(255), nullable=False)
    trinh_do = Column(Integer, nullable=False)
    so_nam = Column(Integer, nullable=False)
    noi_day = Column(String, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="hoat_dong_gd")

# BẢNG TRUNG GIAN
class ThanhVienDeTaiNCKHGV(Base):
    __tablename__ = "ThanhVienDeTaiNCKHGV"
    #done
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    vi_tri_tham_du = Column(Boolean, nullable=False)

    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="thanh_vien")
    giang_vien = relationship("GiangVien", back_populates="de_tai_gv_thanh_vien")

class NguyenVongDangKyNCKH(Base):
    __tablename__ = "NguyenVongDangKyNCKH"
    #done
    ma_dk = Column(Integer, ForeignKey("DangKyNCKH.ma_dk"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    muc_uu_tien = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False)

    dang_ky_nckh = relationship("DangKyNCKH", back_populates="nguyen_vong")
    giang_vien = relationship("GiangVien", back_populates="nguyen_vong_dk")