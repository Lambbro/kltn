from repositories.repository import SinhVienRepository
from sqlalchemy.orm import Session
from schemas.schemas import SinhVien, SinhVienCreate, SinhVienUpdate
from typing import List, Optional

class SinhVienService:
    def __init__(self, db: Session):
        self.repo = SinhVienRepository(db)

    def get_all_sinh_vien(self) -> List[SinhVien]:
        return self.repo.get_all()

    def get_sinh_vien(self, ma_sv: str) -> Optional[SinhVien]:
        sinh_vien = self.repo.get(ma_sv)
        if not sinh_vien:
            raise ValueError(f"Sinh viên với mã '{ma_sv}' không tồn tại.")
        return sinh_vien

    def create_sinh_vien(self, sinh_vien_data: SinhVienCreate) -> SinhVien:
        return self.repo.create(sinh_vien_data)

    def update_sinh_vien(self, ma_sv: str, sinh_vien_data: SinhVienUpdate) -> Optional[SinhVien]:
        sinh_vien = self.repo.update(ma_sv, sinh_vien_data)
        if not sinh_vien:
            raise ValueError(f"Không thể cập nhật sinh viên với mã '{ma_sv}', có thể mã này không tồn tại.")
        return sinh_vien

    def delete_sinh_vien(self, ma_sv: str) -> bool:
        success = self.repo.delete(ma_sv)
        if not success:
            raise ValueError(f"Không thể xóa sinh viên với mã '{ma_sv}', có thể mã này không tồn tại.")
        return success