from contextvars import ContextVar

from fastapi import Depends, Request

from starlette.middleware.base import BaseHTTPMiddleware

from core.app import app


class UserContext:
    def __init__(self, userid: int):
        self.userid = userid


request_context: ContextVar[UserContext] = ContextVar("request_context")


class TokenProvideInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 在请求之前设置上下文数据
        response = await call_next(request)

        mctx = request_context
        print(mctx)

        return response


app.add_middleware(TokenProvideInterceptor)
