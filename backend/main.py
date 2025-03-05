from routers import sinh_vien_router, tai_khoan_router, khoa_router, huong_nc_router
from fastapi import FastAPI
from database import engine, Base
import asyncio

app = FastAPI(
    title="API Quản Lý NCKH",
    description="API Quản Lý NCKH của Trường Đại học Mở Hà Nội",
    version="1.0.0"
)

# Chạy tạo bảng bất đồng bộ
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Chạy init_db() khi khởi động ứng dụng
@app.on_event("startup")
async def on_startup():
    await init_db()

# Đăng ký các router
app.include_router(khoa_router.router)
app.include_router(huong_nc_router.router)
app.include_router(tai_khoan_router.router)
app.include_router(sinh_vien_router.router)

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
