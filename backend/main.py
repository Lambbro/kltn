from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    dang_nhap_router, phong_router, to_router, sinhvien_router, giangvien_router,
    get_data_router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL của frontend Vue.js
    allow_credentials=False,  # Quan trọng để gửi cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(phong_router.ql_router)
app.include_router(dang_nhap_router.dn_router)
app.include_router(sinhvien_router.sv_router)
app.include_router(to_router.qlk_router)
app.include_router(giangvien_router.gv_router)
app.include_router(get_data_router.get_data_router)

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
