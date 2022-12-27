from fastapi.testclient import TestClient
from httpx import AsyncClient

from noname.db import Database
from noname.main import app, get_db_connection
import pytest


database = Database(
    name='example', host='localhost', port=5433, username='example', password='example'
)


async def get_test_db_connection():
    await database.connect()
    async with database.pool.acquire() as connection:
        yield connection


app.dependency_overrides[get_db_connection] = get_test_db_connection


@pytest.mark.asyncio
async def test_home():
    async with AsyncClient(app=app, base_url='http://localhost:1234') as ac:
        response = await ac.get('/')
    assert response.status_code == 200
    data = response.json()
    assert data['db'] == 1
    assert data['host']
