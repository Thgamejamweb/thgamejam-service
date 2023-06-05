import glob
import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from typing import Callable as _Callable, Any as _Any, Dict as _Dict

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

from app.services.user import UserServiceImpl
from thgamejam.api.user.user_pb2_http import register_user_http_server

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
    return MessageToJson(reply)


def parse_request(request_proto: Message, request_bytes: bytes) -> Message:
    return Parse(request_bytes, request_proto)


# service_file = glob.glob("services/*.py")

if __name__ == '__main__':
    # for file_path in service_file:
    #     module_name = file_path.replace(".py", "").replace("\\", ".")
    #     print(module_name)
    #     module = importlib.import_module(module_name)
    register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
    uvicorn.run(app)
