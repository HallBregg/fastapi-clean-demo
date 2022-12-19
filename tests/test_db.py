import pytest


class TestDb:
    @pytest.mark.asyncio
    async def test_database(self, db_fixture):
        async with db_fixture.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * from book;')
            assert row['title'] == 'My title'
            assert row['primary_author'] == 'Some Author'
