from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import aioredis
from aioredis import Redis
from pydantic import RedisDsn
from starlette import status
from starlette.datastructures import State

from core.settings import settings
from providers.exc import APIError
from providers.helpers import get_context_from_provider


class CacheProvider:
    state_name = 'cache_provider'

    def __init__(self, config: Optional[RedisDsn] = None):
        self.config = config or settings.redis_path

    @property
    async def client(self):
        if not hasattr(self, '__async_client'):
            self.__async_client = await aioredis.from_url(str(self.config))
        return self.__async_client

    async def _ping(self) -> bool:
        async with self.context().acquire() as client:
            result = await client.ping()
        return result

    async def health_check(self):
        return await self._ping()

    def context(self):
        return CacheContext(self)


class CacheContext:
    def __init__(self, provider: CacheProvider):
        self._provider = provider
        self._waiters = []

    @property
    def client(self):
        if not hasattr(self, '__async_client') or self.__async_client is not None:
            self.__async_client = self._provider.client
        return self.__async_client

    @asynccontextmanager
    async def acquire(
            self
    ) -> AsyncGenerator[Redis, None]:
        async with self:
            yield await self.client

    async def start(self):
        if not self._waiters:
            await self.client
        self._waiters.append(object())

    def __await__(self):
        self.start().__await__()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        del exc_type, exc_val, exc_tb
        await self.finish()

    async def finish(self):
        self._waiters.pop()
        if not self._waiters:
            self.client.close()
            self.__async_client = None


def setup_cache(config: Optional[RedisDsn] = None):
    provider = CacheProvider(config)

    async def _setup_cache(state: State):
        setattr(state, CacheProvider.state_name, provider)

        if not await provider.health_check():
            raise APIError(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                'Cache not working',
            )
    return _setup_cache


def get_cache_context():
    return get_context_from_provider(CacheProvider)
