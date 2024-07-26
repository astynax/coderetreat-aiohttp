import inspect
from dataclasses import dataclass
from typing import (
    Awaitable, Callable, Concatenate, Any, Annotated, LiteralString
)

import aiohttp
from aiohttp import web, typedefs
from aiohttp.abc import AbstractView

DEPS_KEY = web.AppKey("dependencies", dict[str, Any])


@dataclass
class Injectable:
    from_key: LiteralString | None = None


app = aiohttp.web.Application()


HandlerType = type[AbstractView] | typedefs.Handler

REQUEST_ATTRS = {
    "headers": dict[str, str],
    "cookies": dict[str, str],
}


def inject[**P](inner: Callable[Concatenate[web.Request, P], Awaitable[web.Response]]) -> HandlerType:
    request_attrs = []
    app_keys: list[(str, str)] = []
    for param in inspect.signature(inner).parameters.values():
        match param:
            case inspect.Parameter(name="request"):
                pass
            case inspect.Parameter(annotation=ann, name=name) if name in REQUEST_ATTRS:
                if ann == inspect.Parameter.empty or ann == REQUEST_ATTRS[name]:
                    request_attrs.append(name)
                else:
                    raise TypeError(f"Type of parameter '{name}' does not match "
                                    f"request attribute type {REQUEST_ATTRS[name]}")
            case inspect.Parameter(
                annotation=object(__metadata__=(Injectable(k),)),
                name=name
            ):
                if k is None:
                    app_keys.append((name, name))
                else:
                    app_keys.append((name, k))
            case _:
                raise ValueError(f"Unknown request attribute: {param.name}")

    async def wrapper(request: web.Request) -> web.Response:
        kwargs = {p: getattr(request, p) for p in request_attrs}
        kwargs.update({n: request.app[DEPS_KEY][k] for n, k in app_keys})
        return await inner(request, **kwargs)

    return wrapper


@inject
async def handler(
        request: web.Request,
        headers: dict[str, str],
        port: Annotated[int, Injectable()],
        p: Annotated[int, Injectable(from_key="port")],
) -> web.Response:
    return web.Response(text=f"{p}, {port}, {headers}")


if __name__ == '__main__':
    app.add_routes([web.get('/', handler)])
    app[DEPS_KEY] = {
        "port": 8080,
        # "conn": Fabric(lambda app: ...)
    }
    web.run_app(app)
