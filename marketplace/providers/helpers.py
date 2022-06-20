import re
from asyncio import gather
from enum import Enum
from typing import Callable, Awaitable, Any

from fastapi import FastAPI
from starlette.datastructures import State
from starlette.requests import Request

_snake_case_regexp = re.compile(r'_([a-z])')


class EventTypes(str, Enum):
    STARTUP = 'startup'
    SHUTDOWN = 'shutdown'


def get_context_from_provider(provider_class):
    def _get_context_from_provider(request: Request):
        state_name = provider_class.state_name.lower().replace(
            'provider', 'context'
        )
        if context := getattr(request.state, provider_class.state_name, None):
            return context
        provider = getattr(request.app.state, provider_class.state_name)
        context = provider.context()
        setattr(request.state, state_name, context)
        return context
    return _get_context_from_provider


def on_event(
        app: FastAPI,
        event_type: EventTypes,
        *handler_funcs: Callable[[State], Awaitable[Any]]
):
    async def inner():
        await gather(*(handler(app.state) for handler in handler_funcs))

    app.add_event_handler(event_type.value, inner)


def to_camel(string: str):
    string = '_'.join(string.split())

    return re.sub(
        _snake_case_regexp,
        lambda match: match[1].upper(),
        string.removesuffix('_')
    )