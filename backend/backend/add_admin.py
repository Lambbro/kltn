from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import base_models as models
from schemas.base_schemas import TaiKhoanCreate, GiangVienCreate
from services import ql_dang_ky_service
import asyncio
from database import get_db  # Đảm bảo bạn có get_db để lấy session
from datetime import date

async def create_admin_account(db: AsyncSession):
    admin_email = "admin2@example.com"
    admin_quyen_han = 1  

    result = await db.execute(select(models.TaiKhoan).filter(models.TaiKhoan.email == admin_email))
    admin_account = result.scalars().first()

    if not admin_account:
        try:
            print("🔍 Không tìm thấy tài khoản admin, đang tạo mới...")

            admin_data = GiangVienCreate(
                ma_gv="GV002",
                ten_gv="Admin User",
                anh_dai_dien=None,
                cccd="001234567891",
                gioi_tinh=True,
                ngay_sinh=date(1990, 1, 1),
                que_quan="Hà Nội",
                email=admin_email,
                quyen_han=admin_quyen_han
            )

            await ql_dang_ky_service.QLDangKyService(db).tao_giang_vien(admin_data)

            # ✅ THÊM COMMIT
            await db.commit()  
            print("✅ Tài khoản admin đã được tạo thành công!")

        except Exception as e:
            print(f"❌ Lỗi khi tạo tài khoản admin: {e}")
            import traceback
            print(traceback.format_exc())  # In stack trace chi tiết
            await db.rollback()
    else:
        print("⚠️ Tài khoản admin đã tồn tại.")

# Chạy script để tạo admin
async def main():
    async for db in get_db():  # Lấy database session
        await create_admin_account(db)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Nếu trong môi trường async, chạy main() theo kiểu task
        asyncio.create_task(main())
    else:
        # Nếu là môi trường bình thường, dùng asyncio.run()
        asyncio.run(main())