import os

import pytest_asyncio

from noname.db import Database


CREATE_DB_QUERY = '''
BEGIN;

CREATE TABLE link (
    id BIGSERIAL NOT NULL, 
    url VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TABLE tag (
    name VARCHAR, 
    UNIQUE (name)
);

CREATE TABLE link_tag (
    link_id BIGINT, 
    tag_name VARCHAR, 
    FOREIGN KEY(link_id) REFERENCES link (id), 
    FOREIGN KEY(tag_name) REFERENCES tag (name)
);

COMMIT;
'''


DELETE_DB_QUERY = '''
BEGIN;

DROP TABLE link_tag;

DROP TABLE tag;

DROP TABLE link;

COMMIT;
'''


async def create_database(db):
    async with db.pool.acquire() as connection:
        await connection.execute(CREATE_DB_QUERY)


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
