from fastapi import APIRouter, Depends
from starlette import status

from deals.models import CompleteDeal, Deal
from deals.use_cases import GenerateDealUseCase
from providers.cache import CacheContext, get_cache_context

router = APIRouter()


@router.post(
    '/{product_sku}',
    status_code=status.HTTP_201_CREATED,
    response_model=CompleteDeal
)
async def generate_deal(
        product_sku: str,
        deal: Deal,
        cache_context: CacheContext = Depends(get_cache_context()),
):
    return await GenerateDealUseCase(product_sku, deal, cache_context).execute()