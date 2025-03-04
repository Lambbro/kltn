from repositories.repository import KhoaRepository
from sqlalchemy.orm import Session
from schemas.schemas import Khoa, KhoaCreate, KhoaUpdate
from typing import List, Optional

class KhoaService:
    def __init__(self, db: Session):
        self.repo = KhoaRepository(db)

    def get_all_khoa(self) -> List[Khoa]:
        return self.repo.get_all()
    
    def get_khoa(self, ma_khoa: str) -> Khoa:
        khoa = self.repo.get(ma_khoa)
        if not khoa:
            raise ValueError(f"Khoa với mã '{ma_khoa}' không tồn tại.")
        return khoa
    
    def create_khoa(self, khoa_data: KhoaCreate) -> Khoa:
        return self.repo.create(khoa_data)
    
    def update_khoa(self, ma_khoa: str, khoa_data: KhoaUpdate) -> Khoa:
        khoa = self.repo.update(ma_khoa, khoa_data)
        if not khoa:
            raise ValueError(f"Không thể cập nhật khoa với mã '{ma_khoa}', có thể mã này không tồn tại.")
        return khoa
    
    def delete_khoa(self, ma_khoa: str) -> bool:
        success = self.repo.delete(ma_khoa)
        if not success:
            raise ValueError(f"Không thể xóa khoa với mã '{ma_khoa}', có thể mã này không tồn tại.")
        return success