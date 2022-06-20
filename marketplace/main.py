from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from marketplace import __version__
from marketplace.core.settings import settings
from providers.cache import setup_cache
from providers.exc import setup_exception_handlers
from providers.helpers import on_event, EventTypes
from providers.storage import setup_storage
from routes import root_router

app = FastAPI(
    title='Marketplace API',
    version=__version__,
    description='A simple marketplace using redis',
    docs_url=f'{settings.base_path}/docs',
    redoc_url=f'{settings.base_path}/redoc',
    openapi_url=f'{settings.base_path}/openapi.json',
    debug=settings.debug,
    default_response_class=ORJSONResponse,
)

app.include_router(root_router, prefix=settings.base_path)
setup_exception_handlers(app)

on_event(
    app,
    EventTypes.STARTUP,
    setup_cache(),
    setup_storage(),
)
