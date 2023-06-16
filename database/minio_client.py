from minio import Minio

from config import settings


class MinioClient:

    def __init__(self) -> None:
        self.connection_is_active = False
        self.client = None

    def get_minio_connection(self):
        if not self.connection_is_active:
            self.client = Minio(
                endpoint=settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False
            )

        print("对象存储连接成功")
        self.connection_is_active = True
        return self.client

    def get_minio_client(self):
        return self.client


minio_client = MinioClient()
