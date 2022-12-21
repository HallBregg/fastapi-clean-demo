import pytest_asyncio

from noname.db import Database


CREATE_DB_QUERY = '''
        BEGIN;
        
        CREATE TABLE alembic_version (
            version_num VARCHAR(32) NOT NULL, 
            CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
        );
        
        -- Running upgrade  -> c6ec6d05af2d
        
        CREATE TABLE book (
            id SERIAL NOT NULL, 
            title VARCHAR, 
            primary_author VARCHAR, 
            PRIMARY KEY (id)
        );
        
        INSERT INTO alembic_version (version_num) VALUES ('c6ec6d05af2d') RETURNING alembic_version.version_num;
        
        COMMIT;
        '''
DELETE_DB_QUERY = '''
        BEGIN;
        
        -- Running downgrade c6ec6d05af2d -> 
        
        DROP TABLE book;
        
        DELETE FROM alembic_version WHERE alembic_version.version_num = 'c6ec6d05af2d';
        
        DROP TABLE alembic_version;
        
        COMMIT;
    '''


async def create_database(db):
    async with db.pool.acquire() as connection:
        await connection.execute(CREATE_DB_QUERY)
        await connection.execute('''INSERT INTO book (title, primary_author) VALUES ('My title', 'Some Author')''')


async def drop_database(db):
    async with db.pool.acquire() as connection:
        await connection.execute(DELETE_DB_QUERY)


@pytest_asyncio.fixture(autouse=False, scope='function')
async def db_fixture():
    db = Database(
        name='example',
        host='localhost',
        port=5433,
        username='example',
        password='example',
    )
    await db.connect()
    await create_database(db)
    yield db
    await drop_database(db)
    await db.disconnect()
