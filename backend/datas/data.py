import random
import datas.default_data as default_data

from datetime import datetime, timedelta

#Create Khoa
def get_list_khoa():
    return default_data.khoa_dict

#Create Hướng Nghiên Cứu
def get_list_hnc():
    return default_data.huong_nghien_cuu_list

#Create Sinh Viên
#tên sv
def random_ten():
    return f"{random.choice(default_data.ho_list)} {random.choice(default_data.ten_dem_list)} {random.choice(default_data.ten_list)}"

# Hàm random ngày sinh
def random_ngay_sinh_sv(tuoi: int):
    nam_sinh = (datetime.today() - timedelta(days=tuoi*365)).year  # Xác định năm sinh cố định
    random_date = datetime(nam_sinh, random.randint(1, 12), random.randint(1, 28))  # Random tháng và ngày
    return random_date.date()

#quê quán
def random_quequan():
    tinh, basodau_cccd = random.choice(list(default_data.cccd_3sodau.items()))
    return tinh, basodau_cccd
#sđt
def random_sdt():
    so_dien_thoai = f"0{random.randint(100000000, 999999999)}"
    return so_dien_thoai
#lớp
def random_lophc(nam_sinh: int):
    ma_nhap_hoc = nam_sinh%2000+18 if nam_sinh > 1999 else 18 + nam_sinh - 2000
    lop_hc = f"{ma_nhap_hoc}10A0{random.randint(1,5)}"
    khoa_hoc = ma_nhap_hoc+2000
    return khoa_hoc, lop_hc
#cccd
def random_cccd(basodau:str, nam_sinh, gioi_tinh):
    so_thu_tu = gioi_tinh if nam_sinh < 2000 else gioi_tinh + 1
    so_ngau_nhien = f"{random.randint(0, 999999):06d}"
    return f"{basodau}{so_thu_tu}{str(nam_sinh)[2:]}{so_ngau_nhien}"

#tạo mã sinh viên
def random_masv(khoa_hoc, stt, ma_khoa):
    ma = khoa_hoc%2000
    return f"{ma}A10{ma_khoa[-2:]}0{stt:04d}"

# Hàm random mã khoa
def random_ma_khoa():
    return random.choice([khoa["ma_khoa"] for khoa in get_list_khoa()])

#insert 1 sv
def create_sv(stt, tuoi):
    ten = random_ten()
    gioi_tinh = random.randint(0,1)
    ngay_sinh = random_ngay_sinh_sv(tuoi)
    que_quan, cccd_baso = random_quequan()
    sdt = random_sdt()
    khoa_hoc, lop_hc = random_lophc(ngay_sinh.year)
    cccd = random_cccd(cccd_baso, ngay_sinh.year, gioi_tinh)
    ma_khoa = random_ma_khoa()
    ma_sv = random_masv(khoa_hoc, stt, ma_khoa)
    email = f"{ma_sv}@students.hou.edu.vn"
    
    return {
        "ma_sv": ma_sv,
        "ten_sv": ten,
        "cccd": cccd,
        "gioi_tinh": gioi_tinh,
        "ngay_sinh": ngay_sinh,
        "que_quan": que_quan,
        "sdt": sdt,
        "lop_hc": lop_hc,
        "khoa_hoc": khoa_hoc,
        "email": email,
        "ma_khoa": ma_khoa
    }

# Create gv
def random_ngay_sinh_gv():
    start_date = datetime.today() - timedelta(days=80*365)  # Giới hạn tuổi tối đa là 25
    end_date = datetime.today() - timedelta(days=25*365)   # Giới hạn tuổi tối thiểu là 18
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.date()

def create_gv():
    ten_gv = random_ten()
    gioi_tinh = random.randint(0,1)
    ngay_sinh = random_ngay_sinh_gv()
    que_quan, cccd_baso = random_quequan()
    sdt = random_sdt()
    cccd = random_cccd(cccd_baso, ngay_sinh.year, gioi_tinh)
    ma_khoa = random_ma_khoa()
    ma_gv = f"GV{ngay_sinh.day:02d}{ngay_sinh.month:02d}{ngay_sinh.year:04d}{ma_khoa}{cccd[-6:]}"
    email = f"{ma_gv}@hou.edu.vn"

    return {
        "ma_gv": ma_gv,
        "ten_gv": ten_gv,
        "cccd": cccd,
        "gioi_tinh": gioi_tinh,
        "ngay_sinh": ngay_sinh,
        "que_quan": que_quan,
        "sdt": sdt,
        "don_vi_cong_tac": "Trường Đại học Mở Hà Nội",
        "dia_chi_cong_tac": "Hà Nội",
        "email": email,
        "ma_khoa": ma_khoa
    }

#Test Data