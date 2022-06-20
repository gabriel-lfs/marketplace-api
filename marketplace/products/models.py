from decimal import Decimal

from pydantic import Field

from core.model import Model


class Product(Model):
    sku: str = Field(..., min_length=1, max_length=10, regex=r'([A-Z]|[a-z]|\d)+')
    description: str = Field(..., min_length=3)
    full_price: Decimal = Field(..., gt=0, decimal_places=2)


class ProductLoad(Model):
    bucket_key: str
