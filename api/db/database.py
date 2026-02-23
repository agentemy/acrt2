from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from config import load_config


config = load_config()
DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_pass}@{config.db.db_host}:{config.db.db_port}/{config.db.db_name}"
SYNC_URL = DATABASE_URL.replace("asyncpg", "psycopg2")
sync_engine = create_engine(SYNC_URL, echo=False)
Base = automap_base()
Base.prepare(sync_engine, reflect=True)

def init_models():
    try:
        Base.prepare(sync_engine, reflect=True)
        print("Модели отражены успешно. Доступные таблицы:", list(Base.classes.keys()))
    except Exception as e:
        print("Ошибка при отражении схемы:", e)
        raise
    finally:
        sync_engine.dispose()


async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)

async def get_async_session():
    async with async_session_maker() as session:
        yield session




