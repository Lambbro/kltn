from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base

from routers import (
    # sinh_vien_router, tai_khoan_router, khoa_router, 
    # huong_nc_router, giang_vien_router,
    # syll_router
    dang_nhap_router, quan_ly_router, detai_sv_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo database khi ứng dụng chạy
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="API Quản Lý NCKH",
    description="API Quản Lý NCKH của Trường Đại học Mở Hà Nội",
    version="1.0.0",
    lifespan=lifespan  # Truyền lifespan vào app
)

# Đăng ký các router
# app.include_router(khoa_router.router)
# app.include_router(huong_nc_router.router)
# app.include_router(tai_khoan_router.router)
# app.include_router(sinh_vien_router.router)
# app.include_router(giang_vien_router.router)
# app.include_router(syll_router.hoc_vi_router)

app.include_router(quan_ly_router.router)
app.include_router(dang_nhap_router.router)
app.include_router(detai_sv_router.router)

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
