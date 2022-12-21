import logging
import random

import asyncpg
from fastapi import FastAPI, Depends
from sqlalchemy import MetaData, Column, Table, String, Integer

from noname.db import Database
from noname.services.hostname import HostnameService
from noname.utils import TimedRoute
from noname.conf import initialize_logging

from fastapi.routing import APIRouter


initialize_logging()

# https://tapoueh.org/blog/2018/11/preventing-sql-injections/
# https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4


view_logger = logging.getLogger('main.view')
app_logger = logging.getLogger('main.app')
router = APIRouter(route_class=TimedRoute)
app = FastAPI()


metadata = MetaData()
books = Table(
    'book', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('primary_author', String),
)


DB_CONNECTION_STRING = "postgresql://example:example@localhost/example"
database = Database(name='example', host='localhost', port=5432, username='example', password='example')


async def get_db_connection():
    async with database.pool.acquire() as connection:
        yield connection


@app.on_event('startup')
async def startup_event_handler():
    app_logger.info('Handling startup event.')
    await database.connect()
    app_logger.info(f'Created database pool.'
                    f'Available connections: {database.pool.get_size()}.')


@app.on_event('shutdown')
async def shutdown_event_handler():
    app_logger.info('Handling shutdown event.')
    await database.disconnect()
    app_logger.info(f'Closed all database connections.'
                    f'Available connections: {database.pool.get_size()}.'
                    f'Database disconnected.')


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
async def test(db_connection: asyncpg.Connection = Depends(get_db_connection)):
    row = await db_connection.fetchrow('''SELECT 1 as result, pg_sleep(1) as sleep;''')
    result = row['result']
    view_logger.debug('Hello World', extra={'hello': 'extra'})
    return {'hello': result}


app.include_router(router)
