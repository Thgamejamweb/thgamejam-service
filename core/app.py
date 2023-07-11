import threading
from typing import Callable
from fastapi import FastAPI

from config.conf_pb2 import Bootstrap
from core.Helper import register_openai
from database.minio_client import MinioClient, listen_minio_events
from database.mysql import Database


class App(object):
    http: FastAPI
    database: Database
    minio_client: MinioClient

    def __init__(self, conf: Bootstrap):
        register_openai(conf)
        self.database = Database(conf)
        self.minio_client = MinioClient(conf)
        self.database.get_db_connection()
        self.minio_client.get_minio_connection()
        self.http = FastAPI()
        self.http.add_event_handler("startup", startup(self.http))
        self.http.add_event_handler("shutdown", stopping(self.http))


def startup(http_app: FastAPI) -> Callable:
    async def app_startup() -> None:
        print("启动")

        thread = threading.Thread(target=listen_minio_events(instance.minio_client, instance.database))
        thread.start()
        pass

    return app_startup


def stopping(http_app: FastAPI) -> Callable:
    async def app_stopping() -> None:
        print("停止")
        pass

    return app_stopping


instance: App
