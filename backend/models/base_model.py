from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Table, Text
from sqlalchemy.orm import relationship
from database import Base
# MODEL CỦA BẢNG QUAN HỆ
# Bảng Thành viên nhóm sv: Sinh Viên - Nhóm NCKH
thanhvien_nhomSV_table = Table(
    "ThanhVienNhomSV", Base.metadata,
    Column("ma_nhom", Integer, ForeignKey("NhomNCKH.ma_nhom"), primary_key=True),
    Column("ma_sv", String(20), ForeignKey("SinhVien.ma_sv"), primary_key=True)
)
# Bảng Khen thưởng đề tài: Đề tài NCKH Sinh Viên - Khen Thưởng
khenthuong_detaiNCKHSV_table = Table(
    "KhenThuongDeTai", Base.metadata,
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"), primary_key=True),
    Column("ma_khen_thuong", Integer, ForeignKey("KhenThuong.ma_khen_thuong"), primary_key=True)
)
# Bảng Người nhận thông báo: Thông báo - tài khoản
taikhoan_thongbao_table = Table(
    "NguoiNhanTB", Base.metadata,
    Column("email", ForeignKey("TaiKhoan.email"), primary_key=True),
    Column("ma_tb", ForeignKey("ThongBao.ma_tb"), primary_key=True)
)
#Bảng Hướng Nghiên Cứu của giảng viên: Giảng Viên - Hướng Nghiên Cứu
giangvien_hnc_table = Table (
    "GVHNC", Base.metadata,
    Column("ma_gv", String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True),
    Column("ma_hnc", Integer, ForeignKey("HuongNghienCuu.ma_hnc"), primary_key=True)
)
#Bảng HNC đăng ký nckh: Hướng Nghiên Cứu - Đăng Ký NCKH
hnc_dknckh_table = Table(
    "HNCDangKyNCKH", Base.metadata,
    Column("ma_hnc", Integer, ForeignKey("HuongNghienCuu.ma_hnc"), primary_key=True),
    Column("ma_dk", Integer, ForeignKey("DangKyNCKH.ma_dk"), primary_key=True)
)
#Bảng HNC Đề tài SV: Hướng Nghiên Cứu - Đề tài NCKH SV
hnc_detaiNCKHSV_table = Table(
    "HNCDeTaiSV", Base.metadata,
    Column("ma_hnc", Integer, ForeignKey("HuongNghienCuu.ma_hnc"), primary_key=True),
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"), primary_key=True)
)
#Bảng HNC Đề tài GV: Hướng Nghiên Cứu - Đề tài NCKH GV
hnc_detaiNCKHGV_table = Table(
    "HNCDeTaiGV", Base.metadata,
    Column("ma_hnc", Integer, ForeignKey("HuongNghienCuu.ma_hnc"), primary_key=True),
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
)
# MODEL CHÍNH
#model khoa
class Khoa(Base):
    __tablename__ = "Khoa"

    #thuoc tinh
    ma_khoa = Column(String(20), primary_key=True)
    ten_khoa = Column(String(255), nullable=False)
    dia_chi = Column(Text)
    #relationship
    sinh_vien = relationship("SinhVien", back_populates="khoa")
    giang_vien = relationship("GiangVien", back_populates="khoa")
    hd_khoa = relationship("HoiDongKhoa", back_populates="khoa")

#model hướng nghiên cứu
class HuongNghienCuu(Base):
    __tablename__ = "HuongNghienCuu"

    #thuoc tinh
    ma_hnc = Column(Integer, primary_key=True, autoincrement=True)
    ten_hnc = Column(String(255), nullable=False)
    #relationship
    dk_nckh = relationship("DangKyNCKH", secondary=hnc_dknckh_table, back_populates="huong_nghien_cuu")
    giang_vien = relationship("GiangVien", secondary=giangvien_hnc_table, back_populates="huong_nghien_cuu")
    de_tai_sv = relationship("DeTaiNCKHSV", secondary=hnc_detaiNCKHSV_table, back_populates="huong_nghien_cuu")
    de_tai_gv = relationship("DeTaiNCKHGV", secondary=hnc_detaiNCKHGV_table, back_populates="huong_nghien_cuu")

#model tài khoản
class TaiKhoan(Base):
    __tablename__ = "TaiKhoan"

    #thuoc tinh
    email = Column(String(50), primary_key=True)
    mat_khau = Column(String(255), nullable=False) #hash
    quyen_han = Column(Integer, nullable=False, default=3)
    #relationship
    sinh_vien = relationship("SinhVien", back_populates="tai_khoan")
    giang_vien = relationship("GiangVien", back_populates="tai_khoan")
    thong_bao = relationship("ThongBao", back_populates="tai_khoan")
    nguoi_nhan_tb = relationship("ThongBao", secondary=taikhoan_thongbao_table, back_populates="tai_khoan_nguoi_nhan")

#model khen thưởng
class KhenThuong(Base):
    __tablename__ = "KhenThuong"

    #thuoc tinh
    ma_khen_thuong = Column(Integer, primary_key=True, autoincrement=True)
    cap_do = Column(Integer, nullable=False)
    muc_do = Column(Integer, nullable=False)
    #relationship
    de_tai_sv = relationship("DeTaiNCKHSV", secondary=khenthuong_detaiNCKHSV_table, back_populates="khen_thuong")

#model sinh viên
class SinhVien(Base):
    __tablename__ = "SinhVien"

    #thuoc tinh
    ma_sv = Column(String(20), primary_key=True)
    ten_sv = Column(String(255), nullable=False)
    anh_dai_dien = Column(Text)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String(255))
    sdt = Column(String(10), unique=True, nullable=True)
    lop_hc = Column(String(15), nullable=False)
    khoa_hoc = Column(Integer, nullable=False)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)
    #relationship
    tai_khoan = relationship("TaiKhoan", back_populates="sinh_vien")    
    khoa = relationship("Khoa", back_populates="sinh_vien")
    dk_nckh = relationship("DangKyNCKH", back_populates="sinh_vien")
    nhom_nckh = relationship("NhomNCKH", secondary=thanhvien_nhomSV_table, back_populates="sinh_vien")
#Model giảng viên
class GiangVien(Base):
    __tablename__ = "GiangVien"

    #thuoc tinh
    ma_gv = Column(String(20), primary_key=True)
    ten_gv = Column(String(255), nullable=False)
    anh_dai_dien = Column(Text)
    cccd = Column(String(12), unique=True, nullable=False)
    gioi_tinh = Column(Boolean, nullable=False)
    ngay_sinh = Column(Date, nullable=False)
    que_quan = Column(String(255))
    sdt = Column(String(10), unique=True, nullable=True)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)
    #relationship
    tai_khoan = relationship("TaiKhoan", back_populates="giang_vien")
    khoa = relationship("Khoa", back_populates="giang_vien")
    nguyen_vong = relationship("NguyenVongDK", back_populates="giang_vien")
    nhom_nckh = relationship("NhomNCKH", back_populates="giang_vien")
    tvhd_khoa = relationship("TVHDKhoa", back_populates="giang_vien")
    
    tv_de_tai_gv = relationship("ThanhVienNCKHGV", back_populates="de_tai_gv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=giangvien_hnc_table, back_populates="giang_vien")
    
    hoc_vi = relationship("HocVi", back_populates="giang_vien", cascade="all, delete-orphan")
    trinh_do_hoc_van = relationship("TrinhDoHocVan", back_populates="giang_vien", cascade="all, delete-orphan")
    chuc_danh_khoa_hoc = relationship("ChucDanhKhoaHoc", back_populates="giang_vien", cascade="all, delete-orphan")
    khoa_dao_tao = relationship("KhoaDaoTao", back_populates="giang_vien", cascade="all, delete-orphan")
    trinh_do_ngoai_ngu = relationship("TrinhDoNgoaiNgu", back_populates="giang_vien", cascade="all, delete-orphan")
    qua_trinh_cong_tac = relationship("QuaTrinhCongTac", back_populates="giang_vien", cascade="all, delete-orphan")
    sach_bao_cong_bo = relationship("SachBaoCongBo", back_populates="giang_vien", cascade="all, delete-orphan")
    phat_minh_sang_che = relationship("PhatMinhSangChe", back_populates="giang_vien", cascade="all, delete-orphan")
    de_tai_khcn = relationship("DeTaiKHCN", back_populates="giang_vien", cascade="all, delete-orphan")
    giai_thuong_khcn = relationship("GiaiThuongKHCN", back_populates="giang_vien", cascade="all, delete-orphan")
    hoat_dong_cao_hoc = relationship("HoatDongCaoHoc", back_populates="giang_vien", cascade="all, delete-orphan")
    hoat_dong_giang_day = relationship("HoatDongGiangDay", back_populates="giang_vien", cascade="all, delete-orphan")

# MODEL THÔNG BÁO
#model thông báo 
class ThongBao(Base):
    __tablename__ = "ThongBao"

    ma_tb = Column(Integer, primary_key=True, autoincrement=True)
    tieu_de = Column(String(255), nullable=False)
    noi_dung = Column(Text, nullable=False)
    link_tep = Column(Text)
    anh_dinh_kem = Column(Text)
    thoi_gian_gui = Column(DateTime, nullable=False)
    email = Column(String(50), ForeignKey("TaiKhoan.email"), nullable=False)

    #relationship
    tai_khoan = relationship("TaiKhoan", back_populates="thong_bao")
    tai_khoan_nguoi_nhan = relationship("TaiKhoan", secondary=taikhoan_thongbao_table, back_populates="nguoi_nhan_tb")


# MODEL HỘI ĐỒNG
#model hội đồng khoa
class HoiDongKhoa(Base):
    __tablename__ = "HoiDongKhoa"

    #thuoc tinh
    ma_hd = Column(Integer, primary_key=True, autoincrement=True)
    so_hd = Column(Integer)
    loai_hd = Column(Integer, nullable=False)
    ngay_bao_cao = Column(Date)
    dia_diem = Column(Text)
    trang_thai = Column(Integer)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"), nullable=False)
    #relationship
    khoa = relationship("Khoa", back_populates="hd_khoa")
    tai_lieu_sv = relationship("TaiLieuNCKHSV", back_populates="hd_khoa")
    tvhd_khoa = relationship("TVHDKhoa", back_populates="hd_khoa")

#model thành viên hội đồng khoa
class TVHDKhoa(Base):
    __tablename__ = "TVHDKhoa"

    #thuoc tinh
    ma_hd = Column(Integer, ForeignKey("HoiDongKhoa.ma_hd"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    tu_cach = Column(Integer, nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="tvhd_khoa")
    hd_khoa = relationship("HoiDongKhoa", back_populates="tvhd_khoa")

#model hội đồng trường
class HoiDongTruong(Base):
    __tablename__ = "HoiDongTruong"

    #thuoc tinh
    ma_hd = Column(Integer, primary_key=True, autoincrement=True)
    so_hd = Column(Integer)
    loai_hd = Column(Integer, nullable=False)
    ngay_bao_cao = Column(Date)
    dia_diem = Column(Text)
    trang_thai = Column(Integer)
    #relationship
    tai_lieu_gv = relationship("TaiLieuNCKHGV", back_populates="hd_truong")
    tai_lieu_sv = relationship("TaiLieuNCKHSV", back_populates="hd_truong")
    tvhd_truong = relationship("TVHDTruong", back_populates="hd_truong")

#model thành viên hội đồng trường
class TVHDTruong(Base):
    ma_tv = Column(Integer, primary_key=True, autoincrement=True)

    #thuoc tinh
    gmail = Column(String(50))
    ten_tv = Column(String(255), nullable=False)
    noi_cong_tac = Column(Text, nullable=False)
    tu_cach = Column(Integer, nullable=False)
    ma_hd = Column(Integer, ForeignKey("HoiDongTruong.ma_hd"), nullable=False)
    #relationship
    hd_truong = relationship("HoiDongTruong", back_populates="tvhd_truong")

# MODEL ĐỀ TÀI NCKH SINH VIÊN
#model đăng ký nckh
class DangKyNCKH(Base):
    __tablename__ = "DangKyNCKH"

    #thuoc tinh
    ma_dk = Column(Integer, primary_key=True, autoincrement=True)
    ma_sv = Column(String(20), ForeignKey("SinhVien.ma_sv"), nullable=False)
    #relationship
    sinh_vien = relationship("SinhVien", back_populates="dk_nckh")
    nguyen_vong = relationship("NguyenVongDK", back_populates="dk_nckh")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_dknckh_table, back_populates="dk_nckh")

#model nguyện vọng đăng ký
class NguyenVongDK(Base):
    __tablename__ = "NguyenVongDK"

    #thuoc tinh
    ma_dk = Column(Integer, ForeignKey("DangKyNCKH.ma_dk"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_dk"), primary_key=True)
    muc_uu_tien = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False, default=1)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="nguyen_vong")
    dk_nckh = relationship("DangKyNCKH", back_populates="nguyen_vong")

#model đề tài nckh sinh viên
class DeTaiNCKHSV(Base):
    __tablename__ = "DeTaiNCKHSV"

    #thuoc tinh
    ma_de_tai = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(255), nullable=False)
    dot_thuc_hien = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False)
    tien_do = Column(Integer, nullable=False)
    ma_khoa = Column(String(20), ForeignKey("Khoa.ma_khoa"))
    #relationship
    nhom_nckh = relationship("NhomNCKH", back_populates="de_tai_sv")
    tai_lieu_sv = relationship("TaiLieuNCKHSV", back_populates="de_tai_sv")
    khen_thuong = relationship("KhenThuong", secondary=khenthuong_detaiNCKHSV_table, back_populates="de_tai_sv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaiNCKHSV_table, back_populates="de_tai_sv")

#model tài liệu nckh sinh viên
class TaiLieuNCKHSV(Base):
    __tablename__ = "TaiLieuNCKHSV"

    #thuoc tinh
    ma_tai_lieu = Column(Integer, primary_key=True, autoincrement=True)
    loai_tai_lieu = Column(Integer, nullable=False)
    link_tep = Column(Text)
    thoi_gian_nop = Column(DateTime)
    trang_thai = Column(Integer, nullable=False, default=0)
    phan_hoi = Column(Text)
    ma_hd_khoa = Column(Integer, ForeignKey("HoiDongKhoa.ma_hd"))
    ma_hd_truong = Column(Integer, ForeignKey("HoiDongTruong.ma_hd"))
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"))
    #relationship
    de_tai_sv = relationship("DeTaiNCKHSV", back_populates="tai_lieu_sv")
    hd_khoa = relationship("HoiDongKhoa", back_populates="tai_lieu_sv")
    hd_truong = relationship("HoiDongTruong", back_populates="tai_lieu_sv")

#model nhóm nckh
class NhomNCKH(Base):
    __tablename__ = "NhomNCKH"

    #thuoc tinh
    ma_nhom = Column(Integer, primary_key=True, autoincrement=True)
    trang_thai = Column(Integer, nullable=False, default=1)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHSV.ma_de_tai"))
    #relationship
    de_tai_sv = relationship("DeTaiNCKHSV", back_populates="nhom_nckh")
    giang_vien = relationship("GiangVien", back_populates="nhom_nckh")
    sinh_vien = relationship("SinhVien", secondary=thanhvien_nhomSV_table, back_populates="nhom_nckh")
# MODEL ĐỀ TÀI NCKH GIẢNG VIÊN
#model đề tài nckh giảng viên
class DeTaiNCKHGV(Base):
    __tablename__ = "DeTaiNCKHGV"

    #thuoc tinh
    ma_de_tai = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(255), nullable=False)
    tg_bat_dau = Column(DateTime, nullable=False)
    tg_nghiem_thu = Column(DateTime, nullable=False)
    tg_thuc_nghiem = Column(DateTime, nullable=False)
    trang_thai = Column(Integer, nullable=False, default=2)
    tien_do = Column(Integer, nullable=False, default=1)
    #relationship
    tai_lieu_gv = relationship("TaiLieuNCKHGV", back_populates="de_tai_gv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaiNCKHGV_table, back_populates="de_tai_gv")
    tv_de_tai_gv = relationship("ThanhVienNCKHGV", back_populates="de_tai_gv")

#model thành viên nckh giảng viên
class ThanhVienNCKHGV(Base):
    __tablename__ = "ThanhVienNCKHGV"

    #thuoc phim
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_dk"), primary_key=True)
    vi_tri_tham_gia = Column(Integer, nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="tv_de_tai_gv")
    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="tv_de_tai_gv")

#model tài liệu nckh giảng viên
class TaiLieuNCKHGV(Base):
    __tablename__ = "TaiLieuNCKHGV"

    #thuoc tinh
    ma_tai_lieu = Column(Integer, primary_key=True, autoincrement=True)
    loai_tai_lieu = Column(Integer, nullable=False)
    link_tep = Column(Text, nullable=False)
    thoi_gian_nop = Column(DateTime, nullable=False)
    trang_thai = Column(Integer, nullable=False, default=1)
    phan_hoi = Column(Text)
    ma_de_tai = Column(Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), nullable=False)
    ma_hd = Column(Integer, ForeignKey("HoiDongTruong.ma_hd"))
    #relationship
    de_tai_gv = relationship("DeTaiNCKHGV", back_populates="tai_lieu_gv")
    hd_truong = relationship("HoiDongTruong", back_populates="tai_lieu_gv")

# MODEL SƠ YẾU LÝ LỊCH KHOA HỌC GIẢNG VIÊN
#model học vị
class HocVi(Base):
    __tablename__ = "HocVi"
    #thuoc tinh
    ma_hv = Column(Integer, primary_key=True, autoincrement=True)
    hoc_vi = Column(Integer, nullable=False)
    nam_dat = Column(Integer, nullable=False)
    nganh = Column(String(255), nullable=False)
    chuyen_nganh = Column(Text, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="hoc_vi", ondelete="CASCADE")

#model chức danh khoa học
class ChucDanhKhoaHoc(Base):
    __tablename__ = "ChucDanhKhoaHoc"
    #thuoc tinh
    ma_cd = Column(Integer, primary_key=True, autoincrement=True)
    chuc_danh = Column(String(255))
    chuc_vu = Column(String(255))
    nam_dat_pgs = Column(Integer)
    nam_dat_gs = Column(Integer)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="chuc_danh_khoa_hoc", ondelete="CASCADE")

#model trình độ học vấn
class TrinhDoHocVan(Base):
    __tablename__ = "TrinhDoHocVan"
    #thuoc tinh
    ma_tdhv = Column(Integer, primary_key=True, autoincrement=True)
    bac_dao_tao = Column(Integer, nullable=False)
    chuyen_nganh = Column(String(255), nullable=False)
    noi_dao_tao = Column(Text, nullable=False)
    nam_tot_nghiep = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="trinh_do_hoc_van", ondelete="CASCADE")

#model khóa đào tạo bồi dưỡng khác
class KhoaDaoTao(Base):
    __tablename__ = "KhoaDaoTao"
    #thuoc tinh 
    ma_kdt = Column(Integer, primary_key=True, autoincrement=True)
    ten_kdt = Column(String(255), nullable=False)
    noi_dao_tao = Column(Text, nullable=False)
    tg_bat_dau = Column(Date, nullable=False)
    tg_ket_thuc = Column(Date, nullable=False)
    van_bang_chung_chi = Column(String(50), nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="khoa_dao_tao", ondelete="CASCADE")

#model trình độ ngoại ngữ
class TrinhDoNgoaiNgu(Base):
    __tablename__ = "TrinhDoNgoaiNgu"
    #thuoc tinh
    ma_nn = Column(Integer, primary_key=True, autoincrement=True)
    ngoai_ngu = Column(String(50), nullable=False)
    nghe = Column(Integer)
    noi = Column(Integer)
    doc = Column(Integer)
    viet = Column(Integer)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="trinh_do_ngoai_ngu", ondelete="CASCADE")

#model quá trình công tác
class QuaTrinhCongTac(Base):
    __tablename__ = "QuaTrinhCongTac"
    #thuoc tinh
    ma_ct = Column(Integer, primary_key=True, autoincrement=True)
    nam_bat_dau = Column(Integer, nullable=False)
    nam_ket_thuc = Column(Integer, nullable=False)
    vi_tri = Column(String(255), nullable=False)
    linh_vuc = Column(String(255), nullable=False)
    co_quan = Column(Text, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="qua_trinh_cong_tac", ondelete="CASCADE")

#model hoạt động khoa học công nghệ và đào tạo
class SachBaoCongBo(Base):
    __tablename__ = "SachBaoCongBo"
    #thuoc tinh
    ma_sach = Column(Integer, primary_key=True, autoincrement=True)
    ten_sach = Column(String(255), nullable=False)
    vi_tri = Column(Boolean, nullable=False) #1: TG, 2: ĐTG
    noi_xb = Column(Text, nullable=False)
    nam_xb = Column(Integer, nullable=False)
    loai_sach = Column(Integer, nullable=False) # map_sach_bao
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="sach_bao_cong_bo", ondelete="CASCADE")

#model phát minh sáng chế
class PhatMinhSangChe(Base):
    __tablename__ = "PhatMinhSangChe"
    #thuoc tinh
    ma_pmsc = Column(Integer, primary_key=True, autoincrement=True)
    ten_pmsc = Column(String(255), nullable=False)
    loai_pmsc = Column(String(255), nullable=False)
    thong_tin = Column(Text, nullable=False)
    tg_cap_bang = Column(Integer, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="phat_minh_sang_che", ondelete="CASCADE")

#model đề tài khcn
class DeTaiKHCN(Base):
    __tablename__ = "DeTaiKHCN"
    #thuoc tinh
    ma_dt_khcn = Column(Integer, primary_key=True, autoincrement=True)
    ten_dt = Column(String(255), nullable=False)
    cap_quan_ly = Column(String(255), nullable=False)
    tg_thuc_hien = Column(Integer, nullable=False)
    trang_thai = Column(Boolean, nullable=False, default=True) #true: đã nghiệm thu, false: chưa nghiệm thu
    ket_qua = Column(String(20))
    loai_de_tai = Column(Integer, nullable=False)#map_loai_de_tai_khcn
    tu_cach = Column(Boolean, nullable=True)#true = chủ trì, false: thành viên
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="de_tai_khcn", ondelete="CASCADE")

#model giải thưởng khcn
class GiaiThuongKHCN(Base):
    __tablename__ = "GiaiThuongKHCN"
    #thuoc tinh
    ma_gt_khcn = Column(Integer, primary_key=True, autoincrement=True)
    noi_dung = Column(Text, nullable=False)
    nam_tang_thuong = Column(Integer, nullable=False)
    loai_giai_thuong = Column(Boolean, nullable=False) #true: giải thưởng, false: hoạt động
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="giai_thuong_khcn", ondelete="CASCADE")

#model hoạt động giảng dạy sau đại học
class HoatDongCaoHoc(Base):
    __tablename__ = "HoatDongCaoHoc"
    #thuoc tinh
    ma_hdch = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(255), nullable=False)
    vai_tro_hd = Column(Integer, nullable=False)#map_vai_tro_hd_cao_hoc
    ten_nguoi_hoc = Column(String(255), nullable=False)
    co_so_dao_tao = Column(Text, nullable=False)
    hoc_vi_dao_tao = Column(Integer, nullable=False)#MAP_HOC_VI_DAO_TAO
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="hoat_dong_cao_hoc", ondelete="CASCADE")

#model hoạt động giảng dạy
class HoatDongGiangDay(Base):
    __tablename__ = "HoatDongGiangDay"
    #thuoc tinh
    ma_hdgd = Column(Integer, primary_key=True, autoincrement=True)
    ten_hoc_phan = Column(String(255), nullable=False)
    chuyen_nganh = Column(String(255), nullable=False)
    trinh_do = Column(Integer, nullable=False) #MAP_CAP_DO_GIANG_DAY
    so_nam = Column(Integer, nullable=False)
    noi_giang_day = Column(Text, nullable=False)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="hoat_dong_giang_day", ondelete="CASCADE")
