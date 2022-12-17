import logging
import random

from fastapi import FastAPI, Depends
from sqlalchemy import MetaData, Column, Table, String, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from noname.services.hostname import HostnameService
from noname.utils import TimedRoute
from noname.conf import initialize_logging

from fastapi.routing import APIRouter


initialize_logging()


view_logger = logging.getLogger('main.view')
router = APIRouter(route_class=TimedRoute)
app = FastAPI()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://example:example@localhost/example"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)


metadata = MetaData()
books = Table(
    'book', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('primary_author', String),
)


def async_session_generator():
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession
    )


async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def create_current_database():
    from sqlalchemy import create_engine

    local_engine = create_engine("postgresql://example:example@localhost/example", connect_args={"check_same_thread": False},)
    metadata.create_all(local_engine)


@router.get('/')
async def home():
    view_logger.info('Called home view.')
    if random.choice([True, False]):
        try:
            raise Exception('Test exception')
        except Exception as e:
            view_logger.exception(e)
            return {'error': str(e)}
    return {'host': await HostnameService().get_hostname()}


@router.get('/test')
async def test(db: Session = Depends(get_session)):
    cursor = await db.execute('SELECT 1 as result, pg_sleep(5) as sleep;')
    result, _ = cursor.fetchone()
    view_logger.debug('Hello World', extra={'hello': 'extra'})
    return {'hello': result}


app.include_router(router)
