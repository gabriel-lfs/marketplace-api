from fastapi import APIRouter

# from deals.routes import router as deals_router
from products.routes import router as products_router

root_router = APIRouter()
v1_router = APIRouter()

v1_router.include_router(products_router, prefix='/products', tags=['Products'])
# v1_router.include_router(deals_router, prefix='/deals', tags=['Deals'])
root_router.include_router(v1_router, prefix='/v1')
