import json
from contextvars import ContextVar

from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from typing import Callable as _Callable, Any as _Any, Dict as _Dict

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message
from jwt import InvalidSignatureError, ExpiredSignatureError
from starlette.responses import JSONResponse

from config import settings
from core.app import app
from modules.JWTUtil import generateToken, parserToken


class UserContext:
    def __init__(self, userid: int):
        self.userid = userid

    def __dict__(self):
        return {
            'userid': self.userid
        }


request_context: ContextVar[UserContext] = ContextVar("request_context")
token_provide_router = ["/web/v1/user/login",
                        "/web/v1/user/register"]
token_check_router = ["/web/v1/user/change/password",
                      "/web/v1/user/id"]


# 注册函数中间件
def register_fastapi_route(methods: str, url: str, handler: _Callable[[_Dict[str, _Any], bytes], _Any]):
    custom_route = APIRoute(url, endpoint=register(handler), methods=[methods])
    app.routes.append(custom_route)


# 拦截器
def register(handler: _Callable[[_Dict[str, _Any], bytes], _Any]) -> _Callable[[Request], _Any]:
    async def endpoint(request: Request) -> _Any:
        token_check_interceptor(request)

        body = await request.body()
        result = handler(request.path_params, body)
        response = JSONResponse(result)

        return token_provide_interceptor(request, response)

    return endpoint


def token_check_interceptor(request: Request):
    request_context.set(UserContext(userid=0))

    if any(request.url.path.startswith(router) for router in token_check_router):
        token = request.cookies.get("token")

        if token is None:
            raise HTTPException(status_code=401, detail="Unauthorized Token")
        else:
            try:
                user_ctx = parserToken(settings.JWT_SECRET_KEY, token, UserContext)
                request_context.set(user_ctx)

            except InvalidSignatureError:
                raise HTTPException(status_code=401, detail="Signature verification failed")

            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Signature has expired")


# token注入
def token_provide_interceptor(request: Request, response: JSONResponse) -> JSONResponse:
    if any(request.url.path.startswith(router) for router in token_provide_router):
        try:
            jwt = generateToken(settings.JWT_SECRET_KEY, request_context.get(), int(settings.JWT_EXPIRATION_TIME))
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
