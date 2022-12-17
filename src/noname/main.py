import logging
import random

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, MetaData, Column, Table, String, Integer
from sqlalchemy.orm import sessionmaker, Session

from noname.services.hostname import HostnameService
from noname.utils import TimedRoute
from noname.conf import initialize_logging

from fastapi.routing import APIRouter


initialize_logging()


view_logger = logging.getLogger('main.view')
router = APIRouter(route_class=TimedRoute)
app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


metadata = MetaData()
books = Table(
    'book', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('primary_author', String),
)


def create_current_database():
    metadata.create_all(engine)


def db_client():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
async def test(db: Session = Depends(db_client)):
    view_logger.debug('Hello World', extra={'hello': 'extra'})
    [result] = db.execute('SELECT 1;').first()
    return {'hello': result}


app.include_router(router)
