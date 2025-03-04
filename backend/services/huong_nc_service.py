from repositories.repository import HuongNghienCuuRepository
from sqlalchemy.orm import Session
from schemas.schemas import HuongNghienCuu, HuongNghienCuuCreate, HuongNghienCuuUpdate
from typing import List, Optional

class HuongNghienCuuService:
    def __init__ (self, db: Session):
        self.repo = HuongNghienCuuRepository(db)

    def get_all_hnc(self) -> List[HuongNghienCuu]:
        return self.repo.get_all()
    
    def get_hnc(self, ma_hnc: int) -> Optional[HuongNghienCuu]:
        huong_nghien_cuu = self.repo.get(ma_hnc)
        if not huong_nghien_cuu:
            raise ValueError(f"Hướng Nghiên Cứu này không tồn tại.")
        return huong_nghien_cuu
    
    def create_hnc(self, hnc_data: HuongNghienCuuCreate) -> HuongNghienCuu:
        return self.repo.create(hnc_data)
    
    def update_hnc(self, ma_hnc: int, hnc_data: HuongNghienCuuUpdate) -> HuongNghienCuu:
        huong_nghien_cuu = self.repo.update(ma_hnc, hnc_data)
        if not huong_nghien_cuu:
            raise ValueError(f"Không thể cập nhật Hướng Nghiên Cứu với mã '{ma_hnc}', có thể mã này không tồn tại.")
        return huong_nghien_cuu
    
    def delete_hnc(self, ma_hnc: int) -> bool:
        success = self.repo.delete(ma_hnc)
        if not success:
            raise ValueError(f"Không thể xóa Hướng Nghiên Cứu với mã '{ma_hnc}', có thể mã này không tồn tại.")
        return success
    