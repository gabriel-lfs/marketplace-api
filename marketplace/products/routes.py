from fastapi import APIRouter, Body, Depends
from starlette import status

from products.models import ProductLoad, Product
from products.use_cases import CacheStoredProductsUseCase, ListAllProductsUseCase, RetrieveProductUseCase
from providers.cache import CacheContext, get_cache_context
from providers.storage import StorageProvider, get_storage

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def update_products(
        body: ProductLoad,
        storage_provider: StorageProvider = Depends(get_storage),
        cache_context: CacheContext = Depends(get_cache_context()),
):
    await CacheStoredProductsUseCase(body, storage_provider, cache_context).execute()


@router.get('/', response_model=list[Product])
async def get_all(cache_context: CacheContext = Depends(get_cache_context())):
    return await ListAllProductsUseCase(cache_context).execute()


@router.get('/{product_sku}', response_model=Product)
async def get_one(product_sku: str, cache_context: CacheContext = Depends(get_cache_context())):
    return await RetrieveProductUseCase(product_sku, cache_context).execute()
