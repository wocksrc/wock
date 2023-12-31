from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Union

from werkzeug.local import LocalProxy


if TYPE_CHECKING:
    from .app import Quart
    from .ctx import AppContext, RequestContext, WebsocketContext, _AppCtxGlobals
    from .sessions import SessionMixin
    from .wrappers import Request, Websocket

_no_app_msg = "Not within an app context"
_cv_app: ContextVar[AppContext] = ContextVar("quart.app_ctx")
app_ctx: _AppCtxGlobals = LocalProxy(_cv_app, unbound_message=_no_app_msg)  # type: ignore[assignment]
current_app: Quart = LocalProxy(_cv_app, "app", unbound_message=_no_app_msg)  # type: ignore[assignment]
g: _AppCtxGlobals = LocalProxy(_cv_app, "g", unbound_message=_no_app_msg)  # type: ignore[assignment]

_no_req_msg = "Not within a request context"
_cv_request: ContextVar[RequestContext] = ContextVar("quart.request_ctx")
request_ctx: RequestContext = LocalProxy(_cv_request, unbound_message=_no_req_msg)  # type: ignore[assignment]
request: Request = LocalProxy(_cv_request, "request", unbound_message=_no_req_msg)  # type: ignore[assignment]

_no_websocket_msg = "Not within a websocket context"
_cv_websocket: ContextVar[WebsocketContext] = ContextVar("quart.websocket_ctx")
websocket_ctx: WebsocketContext = LocalProxy(_cv_websocket, unbound_message=_no_websocket_msg)  # type: ignore[assignment]
websocket: Websocket = LocalProxy(_cv_websocket, "websocket", unbound_message=_no_websocket_msg)  # type: ignore[assignment]


def _session_lookup() -> Union[RequestContext, WebsocketContext]:
    try:
        return _cv_request.get()
    except LookupError:
        try:
            return _cv_websocket.get()
        except LookupError:
            raise RuntimeError("Not within a request nor websocket context")


session: SessionMixin = LocalProxy(_session_lookup, "session")  # type: ignore[assignment]
