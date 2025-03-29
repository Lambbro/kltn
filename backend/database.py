from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY =  os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if not DATABASE_URL:
    raise ValueError("Lỗi: Không tìm thấy biến môi trường DATABASE_URL ở .env")

# Đảm bảo DATABASE_URL dùng driver async
if not DATABASE_URL.startswith("mysql+aiomysql://"):
    raise ValueError("Lỗi: DATABASE_URL phải sử dụng 'mysql+aiomysql://' thay vì 'mysqlconnector'")

# Tạo engine async
engine = create_async_engine(DATABASE_URL, echo=True)

# Tạo session async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model để kế thừa
Base = declarative_base()

# Dependency cho FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # Không cần `close()`, `async with` tự xử lý
