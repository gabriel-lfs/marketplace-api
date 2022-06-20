from random import randrange, random

from faker import Faker
from faker_vehicle import VehicleProvider
from orjson import orjson

fake = Faker()
fake.add_provider(VehicleProvider)

with open('products.json', 'w') as f:
    products = [
        {
            "sku": fake.bothify('###?###?#').upper(),
            "description": fake.vehicle_year_make_model_cat(),
            "full_price": fake.random_int(min=100_000, max=1_000_000) + round(random(), 2)
        } for _ in range(randrange(start=4000))
    ]

    f.write(orjson.dumps(products).decode())
