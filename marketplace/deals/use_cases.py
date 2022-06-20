from aioredis import Redis

from deals.models import Deal, CompleteDeal
from products.use_cases import RetrieveProductUseCase
from providers.cache import CacheContext


class GenerateDealUseCase:
    def __init__(
            self,
            product_sku: str,
            deal: Deal,
            cache_context: CacheContext
    ):
        self._product_sku = product_sku
        self._deal = deal
        self._cache_context = cache_context

    async def execute(self):
        product = await RetrieveProductUseCase(self._product_sku, self._cache_context).execute()
        discounted_value = product.full_price * (self._deal.discount_percentage / 100)

        complete_deal = CompleteDeal(
            discount_percentage=self._deal.discount_percentage,
            expires=self._deal.expires,
            discounted_value=discounted_value,
            actual_value=product.full_price - discounted_value,
            product=product
        )
        async with self._cache_context.acquire() as client:  # type: Redis
            key = f'deal-{product.sku}'
            data = complete_deal.json(exclude={'product'})
            await client.set(key, data)
            await client.expireat(key, self._deal.expires)
            await client.hset('deals', key, data)



