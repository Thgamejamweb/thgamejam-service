from typing import Callable

from fastapi import FastAPI

from core.app import app
from database.mysql import engine


def startup(app: FastAPI) -> Callable:
    async def app_startup() -> None:
        print("启动")
        pass

    return app_startup


def stopping(app: FastAPI) -> Callable:
    async def app_stopping() -> None:
        print("停止")
        pass

    return app_stopping


app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", stopping(app))
