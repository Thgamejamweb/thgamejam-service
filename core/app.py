from typing import Callable

from fastapi import FastAPI

from database.minio_client import minio_client
from database.mysql import database

app = FastAPI()


def startup(app: FastAPI) -> Callable:
    async def app_startup() -> None:
        print("启动")
        database.get_db_connection()
        minio_client.get_minio_connection()
        pass

    return app_startup


def stopping(app: FastAPI) -> Callable:
    async def app_stopping() -> None:
        print("停止")
        pass

    return app_stopping


app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", stopping(app))
