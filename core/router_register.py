import json
from contextvars import ContextVar
from datetime import datetime

from fastapi import Request
from fastapi.routing import APIRoute
from typing import Callable as _Callable, Any as _Any, Dict as _Dict

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message
from starlette.responses import JSONResponse

from config import settings
from core.app import app
from modules.JWTUtil import generateToken

token_provide_router = ["/web/v1/user/login"]


class UserContext:
    def __init__(self, userid: int):
        self.userid = userid

    def __dict__(self):
        return {
            'userid': self.userid
        }


request_context: ContextVar[UserContext] = ContextVar("request_context")


# 注册函数中间件
def register_fastapi_route(methods: str, url: str, handler: _Callable[[_Dict[str, _Any], bytes], _Any]):
    custom_route = APIRoute(url, endpoint=register(handler), methods=[methods])
    app.routes.append(custom_route)


# 拦截器
def register(handler: _Callable[[_Dict[str, _Any], bytes], _Any]) -> _Callable[[Request], _Any]:
    async def endpoint(request: Request) -> _Any:
        # TODO token获取

        body = await request.body()
        result = handler(request.path_params, body)
        response = JSONResponse(result)

        return TokenProvideInterceptor(request, response)

    return endpoint


# token注入
def TokenProvideInterceptor(request: Request, response: JSONResponse) -> JSONResponse:
    if request.url.path in token_provide_router:
        try:
            jwt = generateToken(settings.JWT_SECRET_KEY, request_context.get(), datetime.now(),
                                int(settings.JWT_EXPIRATION_TIME))
            response.set_cookie("token", jwt)
        except LookupError:
            pass

    return response


def parse_reply(reply: Message) -> bytes:
    json_str = MessageToJson(reply)
    try:
        json_obj = json.loads(json_str)
        return json_obj
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}


def parse_request(request_proto: Message, request_bytes: bytes) -> Message:
    return Parse(request_bytes, request_proto)
