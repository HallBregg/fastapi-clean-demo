import asyncio
import json
import logging
from typing import Optional

import asyncpg


class Database:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        name: str,
        min_connections: int = 5,
        max_connections: int = 10,
    ):
        self.__logger = logging.getLogger(f'main.{__name__}')
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._name = name
        self._min_connections = min_connections
        self._max_connections = max_connections

        self._pool: Optional[asyncpg.Pool] = None
        self._connection = None

        self.__logger.debug('Database fully initialized.')

        self._connection_lock = asyncio.Lock()
        self._connection_counter = 0

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    @property
    def _pool_connection_kwargs(self):
        return dict(
            user=self._username,
            password=self._password,
            host=self._host,
            port=self._port,
            database=self._name,
            min_size=self._min_connections,
            max_size=self._max_connections,
        )

    @property
    def _connection_kwargs(self):
        return dict(
            user=self._username,
            password=self._password,
            host=self._host,
            port=self._port,
            database=self._name,
        )

    @property
    def is_connected(self):
        return any([self._pool, self._connection])

    @property
    def pool(self):
        return self._pool

    async def _connect(self):
        connection = await asyncpg.connect(**self._connection_kwargs)
        await connection.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        return connection

    async def _create_pool(self):
        return await asyncpg.create_pool(**self._pool_connection_kwargs)

    async def connect(self):
        assert not self.is_connected, 'Database is already running'
        self._pool = await self._create_pool()
        self.__logger.info('Database connected.')

    async def disconnect(self):
        assert self.is_connected, 'Database is not running.'
        await self._pool.close()
        self.__logger.info('Database disconnected.')
