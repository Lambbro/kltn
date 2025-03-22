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
# Bảng Thành viên đề tài giảng viên: Giảng viên - đề tài NCKH GV
giangvien_detainckhgv_table = Table (
    "ThanhVienDeTaiGV", Base.metadata,
    Column("ma_gv", String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True),
    Column("ma_de_tai", Integer, ForeignKey("DeTaiNCKHGV.ma_de_tai"), primary_key=True)
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

class KhenThuong(Base):
    __tablename__ = "KhenThuong"

    #thuoc tinh
    ma_khen_thuong = Column(Integer, primary_key=True, autoincrement=True)
    cap_do = Column(Integer, nullable=False)
    muc_do = Column(Integer, nullable=False)
    #relationship
    de_tai_sv = relationship("DeTaiNCKHSV", secondary=khenthuong_detaiNCKHSV_table, back_populates="khen_thuong")

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
    de_tai_gv = relationship("DeTaiNCKHGV", secondary=giangvien_detainckhgv_table, back_populates="giang_vien")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=giangvien_hnc_table, back_populates="giang_vien")

# MODEL THÔNG BÁO 
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

class TVHDKhoa(Base):
    __tablename__ = "TVHDKhoa"

    #thuoc tinh
    ma_hd = Column(Integer, ForeignKey("HoiDongKhoa.ma_hd"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_gv"), primary_key=True)
    tu_cach = Column(Integer, nullable=False)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="tvhd_khoa")
    hd_khoa = relationship("HoiDongKhoa", back_populates="tvhd_khoa")

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
class DangKyNCKH(Base):
    __tablename__ = "DangKyNCKH"

    #thuoc tinh
    ma_dk = Column(Integer, primary_key=True, autoincrement=True)
    ma_sv = Column(String(20), ForeignKey("SinhVien.ma_sv"), nullable=False)
    #relationship
    sinh_vien = relationship("SinhVien", back_populates="dk_nckh")
    nguyen_vong = relationship("NguyenVongDK", back_populates="dk_nckh")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_dknckh_table, back_populates="dk_nckh")

class NguyenVongDK(Base):
    __tablename__ = "NguyenVongDK"

    #thuoc tinh
    ma_dk = Column(Integer, ForeignKey("DangKyNCKH.ma_dk"), primary_key=True)
    ma_gv = Column(String(20), ForeignKey("GiangVien.ma_dk"))
    muc_uu_tien = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False, default=1)
    #relationship
    giang_vien = relationship("GiangVien", back_populates="nguyen_vong")
    dk_nckh = relationship("DangKyNCKH", back_populates="nguyen_vong")

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
class DeTaiNCKHGV(Base):
    __tablename__ = "DeTaiNCKHGV"

    #thuoc tinh
    ma_de_tai = Column(Integer, primary_key=True, autoincrement=True)
    ten_de_tai = Column(String(255), nullable=False)
    tg_bat_dau = Column(DateTime, nullable=False)
    tg_nghiem_thu = Column(DateTime, nullable=False)
    tg_thuc_nghiem = Column(DateTime, nullable=False)
    vi_tri_tham_gia = Column(Integer, nullable=False)
    trang_thai = Column(Integer, nullable=False, default=2)
    tien_do = Column(Integer, nullable=False, default=1)
    #relationship
    tai_lieu_gv = relationship("TaiLieuNCKHGV", back_populates="de_tai_gv")
    giang_vien = relationship("GiangVien", secondary=giangvien_detainckhgv_table, back_populates="de_tai_gv")
    huong_nghien_cuu = relationship("HuongNghienCuu", secondary=hnc_detaiNCKHGV_table, back_populates="de_tai_gv")

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
