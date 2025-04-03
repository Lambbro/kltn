from typing import List
from pydantic import BaseModel, Field
from schemas.base_schemas import NguyenVongDKResponse, DangKyNCKHResponse

class DangKyNguyenVongResponse(DangKyNCKHResponse):
    list_nguyen_vong: List[NguyenVongDKResponse] = Field(..., description="Danh sách nguyện vọng")

    class Config:
        from_attributes = True