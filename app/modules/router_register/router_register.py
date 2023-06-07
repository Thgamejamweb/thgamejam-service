import json

from fastapi import Request, FastAPI
from fastapi.routing import APIRoute
from typing import Callable as _Callable, Any as _Any, Dict as _Dict

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

app = FastAPI()


def register_fastapi_route(methods: str, url: str, handler: _Callable[[_Dict[str, _Any], bytes], _Any]):
    custom_route = APIRoute(url, endpoint=register(handler), methods=[methods])
    app.routes.append(custom_route)


def register(handler: _Callable[[_Dict[str, _Any], bytes], _Any]) -> _Callable[[Request], _Any]:
    async def endpoint(request: Request) -> _Any:
        body = await request.body()
        return handler(request.path_params, body)

    return endpoint


def parse_reply(reply: Message) -> bytes:
    json_str = MessageToJson(reply)
    try:
        json_obj = json.loads(json_str)
        return json_obj
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}


def parse_request(request_proto: Message, request_bytes: bytes) -> Message:
    return Parse(request_bytes, request_proto)
