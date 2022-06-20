from decimal import Decimal

from datetime import datetime

from core.model import Model
from products.models import Product


class Deal(Model):
    discount_percentage: Decimal
    expires: datetime


class CompleteDeal(Deal):
    product: Product
    discounted_value: Decimal
    actual_value: Decimal
