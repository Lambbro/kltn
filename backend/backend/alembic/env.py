import os
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Cấu hình Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import models để lấy metadata
from database import Base
from models import base_models

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Chạy migration ở chế độ offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Chạy migration ở chế độ online với AsyncEngine."""
    connectable = create_async_engine(DATABASE_URL, poolclass=None)

    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    """Hàm chạy migration trong transaction."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
