from typing import List
from pydantic import BaseModel, Field
from schemas.base_schemas import (
    NguyenVongDKResponse, DangKyNCKHResponse,
    NhomNCKHBase
)

#Chức năng đăng ký
class DangKyNguyenVongResponse(DangKyNCKHResponse):
    list_nguyen_vong: List[NguyenVongDKResponse] = Field(..., description="Danh sách nguyện vọng")

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
    thanh_vien: List[ThanhVienNhomResponse]

    class Config:
        orm_mode = True