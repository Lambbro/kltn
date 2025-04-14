from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.base_schemas import (
    NguyenVongDKResponse,
    NhomNCKHBase, HuongNghienCuuResponse, TaiLieuNCKHSVResponse
)

#Chức năng đăng ký
class DangKyNCKHSVResponse(BaseModel):
    ma_dk: int = Field(..., description="Mã đăng ký")
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=255, description="Tên sinh viên")
    trang_thai: int = Field(1, description="Trạng thái đăng ký")
    list_nguyen_vong: List[NguyenVongDKResponse] = Field(..., description="Danh sách nguyện vọng")
    list_hnc: List[HuongNghienCuuResponse] = Field(..., description="Danh sách hướng nghiên cứu")

    class Config:
        from_attributes = True
#Chức năng nhóm nckh sv
class ThanhVienNhomResponse(BaseModel):
    ma_sv: str = Field(..., max_length=20, description="Mã sinh viên")
    ten_sv: str = Field(..., max_length=255, description="Tên sinh viên")

    class Config:
        from_attributes = True

class NhomNCKHSVResponse(NhomNCKHBase):
    ma_nhom: int
    ma_de_tai: Optional[int]
    ten_de_tai: Optional[str]
    thanh_vien: List[ThanhVienNhomResponse]

    class Config:
        from_attributes = True

# ĐỀ TÀI NCKH SINH VIÊN
class DeTaiNCKHSinhVienResponse(BaseModel):
    ma_de_tai: int = Field(..., description="Mã đề tài nghiên cứu khoa học sinh viên")
    ten_de_tai: str = Field(..., max_length=255, description="Tên đề tài")
    dot_thuc_hien: int = Field(..., description="Đợt thực hiện")
    trang_thai: int = Field(1, description="Trạng thái đề tài")
    tien_do: int = Field(1, description="Tiến độ thực hiện")
    diem_so: Optional[int] = Field(None, description="Điểm số của đề tài") 

    nhom: NhomNCKHSVResponse
    tai_lieu: Optional[List[TaiLieuNCKHSVResponse]]

    class Config:
        from_attributes = True