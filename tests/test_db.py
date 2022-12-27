import pytest


@pytest.mark.integration
@pytest.mark.db
class TestDb:

    @pytest.mark.asyncio
    async def test_database(self, db_fixture):
        async with db_fixture.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 as result;')
            assert row['result'] == 1
