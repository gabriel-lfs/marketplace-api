import asyncio

from pydantic import parse_raw_as
from starlette import status

from products.models import Product, ProductLoad
from providers.cache import CacheContext
from providers.exc import APIError
from providers.storage import StorageProvider


class CacheStoredProductsUseCase:
    def __init__(
            self, body: ProductLoad, storage_provider: StorageProvider, cache_context: CacheContext
    ):
        self._bucket_key = body.bucket_key
        self._storage_provider = storage_provider
        self._cache_context = cache_context

    async def execute(self):
        body = self._storage_provider.get_file(self._bucket_key)
        products = parse_raw_as(list[Product], body.read())

        async with self._cache_context.acquire() as client:
            await asyncio.gather(
                *[
                    client.hset(f'product', product.sku, product.json()) for product in products
                ]
            )


class ListAllProductsUseCase:
    def __init__(self, cache_context: CacheContext):
        self._cache_context = cache_context

    async def execute(self):
        async with self._cache_context.acquire() as client:
            return [Product.parse_raw(product) for product in await client.hvals('product')]


class RetrieveProductUseCase:
    def __init__(self, product_sku: str, cache_context: CacheContext):
        self._cache_context = cache_context
        self._product_sku = product_sku

    async def execute(self):
        async with self._cache_context.acquire() as client:
            result = await client.hget('product', self._product_sku)
            if not result:
                raise APIError(status.HTTP_404_NOT_FOUND, 'Produto não encontrado')

            return Product.parse_raw(result)
