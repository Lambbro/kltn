import repositories.nckh_repository as repository
import schemas.nckh_schemas as schemas
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class DangKyNCKHService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.DangKyNCKHRepository(db)

    async def get_all(self) -> List[schemas.DangKyNCKH]:
        return await self.repo.get_all()
    
    async def get(self, ma_dang_ky: int) -> schemas.DangKyNCKH:
        dang_ky = await self.repo.get(ma_dang_ky)
        if not dang_ky:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy đăng ký nckh với mã {ma_dang_ky}")
        return dang_ky
    
    async def create(self, dang_ky_data: schemas.DangKyNCKHCreate) -> schemas.DangKyNCKH:
        return await self.repo.create(dang_ky_data)
    
    async def update(self, ma_dang_ky: int, dang_ky_data: schemas.DangKyNCKHUpdate) -> schemas.DangKyNCKH:
        dang_ky = await self.repo.update(ma_dang_ky, dang_ky_data)
        if not dang_ky:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật đăng ký mã {ma_dang_ky}")
        return dang_ky
    
    async def delete(self, ma_dang_ky: int) -> dict:
        success = await self.repo.delete(ma_dang_ky)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa đăng ký với mã {ma_dang_ky}")
        return {"success": True, "message": "Xóa đăng ký NCKH thành công."}
    
class NguyenVongService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.NguyenVongDangKyNCKHRepository(db)

    async def get_all(self) -> List[schemas.NguyenVongDangKyNCKH]:
        return await self.repo.get_all()
    
    async def get(self, ma_dk: int, ma_gv: str) -> schemas.NguyenVongDangKyNCKH:
        nguyen_vong = await self.repo.get(ma_dk, ma_gv)
        if not nguyen_vong:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy nguyện vọng với mã đăng ký {ma_dk} và mã giảng viên {ma_gv}")
        return nguyen_vong
    
    async def create(self, nguyen_vong_data: schemas.NguyenVongDangKyNCKHCreate, ma_dk: int) -> schemas.NguyenVongDangKyNCKH:
        return await self.repo.create(nguyen_vong_data, ma_dk)
    
    async def update(self, ma_dk: int, ma_gv: int, nguyen_vong_data: schemas.NguyenVongDangKyNCKHUpdate) -> schemas.NguyenVongDangKyNCKH:
        nguyen_vong = await self.repo.update(ma_dk, ma_gv, nguyen_vong_data)
        if not nguyen_vong:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật nguyện vọng của đăng ký mã {ma_dk} với mã giảng viên {ma_gv}")
        return nguyen_vong
    
    async def delete(self, ma_dk: int, ma_gv: int) -> dict:
        success = await self.repo.delete(ma_dk, ma_gv)
        if not success: 
            raise HTTPException(status_code=404, detail=f"Không thể xóa nguyện vọng với mã đăng ký {ma_dk} và mã giảng viên {ma_gv}")
        return {"success": True, "message": "Xóa thành công nguyện vọng."}
    
class NhomNCKHService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.NhomNCKHRepository(db)
    
    async def get_all(self) -> List[schemas.NhomNCKH]:
        return await self.repo.get_all()
    
    async def get(self, ma_nhom: int) -> schemas.NhomNCKH:
        nhom_nckh = await self.repo.get(ma_nhom)
        if not nhom_nckh:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy nhóm mã {ma_nhom}")
        return nhom_nckh
    
    async def create(self, nhom_data: schemas.NhomNCKHCreate) -> schemas.NhomNCKH:
        return await self.repo.create(nhom_data)

    async def update(self, ma_nhom: int, nhom_data: schemas.NhomNCKHUpdate) -> schemas.NhomNCKH:
        nhom_nckh = await self.repo.update(ma_nhom, nhom_data)
        if not nhom_nckh:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật nhóm nghiên cứu khoa học với mã {ma_nhom}")
        return nhom_nckh
    
    async def delete(self, ma_nhom: int) -> dict:
        success = await self.repo.delete(ma_nhom)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa nhóm mã {ma_nhom}")
        return {"success": True, "message": "Xóa thành công nhóm nghiên cứu khoa học."}

class DeTaiNCKHSVService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.DeTaiNCKHSVRepository(db)

    async def get_all(self) -> List[schemas.DeTaiNCKHSV]:
        return await self.repo.get_all()
    
    async def get(self, ma_de_tai: int) -> schemas.DeTaiNCKHSV:
        de_tai = await self.repo.get(ma_de_tai)
        if not de_tai:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy đề tài mã {ma_de_tai}")
        return de_tai
    
    async def create(self, de_tai_data: schemas.DeTaiNCKHSVCreate) -> schemas.DeTaiNCKHSV:
        return await self.repo.create(de_tai_data)
    
    async def update(self, ma_de_tai: int, de_tai_data: schemas.DeTaiNCKHSVUpdate) -> schemas.DeTaiNCKHSV:
        de_tai = await self.repo.update(ma_de_tai, de_tai_data)
        if not de_tai:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật đề tài NCKH sinh viên với mã {ma_de_tai}")
        return de_tai
    
    async def delete(self, ma_de_tai: int) -> dict:
        success = await self.repo.delete(ma_de_tai)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa đề tài NCKH sinh viên mã {ma_de_tai}")
        return {"success": True, "message": "Xóa thành công đề tài nghiên cứu khoa học sinh viên"}

class TaiLieuNCKHSVService:
    def __init__(self, db: AsyncSession):
        self.repo = repository.TaiLieuNCKHSVRepository(db)

    async def get_all(self) -> List[schemas.TaiLieuNCKHSV]:
        return await self.repo.get_all()
    
    async def get(self, ma_tai_lieu:int ) -> schemas.TaiLieuNCKHSV:
        tai_lieu = await self.repo.get(ma_tai_lieu)
        if not tai_lieu:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy tài liệu mã {ma_tai_lieu}")
        return tai_lieu
    
    async def create(self, de_tai_data: schemas.TaiLieuNCKHSVCreate) -> schemas.TaiLieuNCKHSV:
        return await self.repo.create(de_tai_data)
    
    async def update(self, ma_tai_lieu: int, tai_lieu_data: schemas.TaiLieuNCKHSVUpdate) -> schemas.TaiLieuNCKHSV:
        tai_lieu = await self.repo.update(ma_tai_lieu, tai_lieu_data)
        if not tai_lieu:
            raise HTTPException(status_code=404, detail=f"Không thể cập nhật tài liệu mã {ma_tai_lieu}")
        return tai_lieu
    
    async def delete(self, ma_tai_lieu: int) -> dict:
        success = await self.repo.delete(ma_tai_lieu)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không thể xóa tài liệu {ma_tai_lieu}")
        return {"success": True, "message": "Xóa thành công tài liệu"}