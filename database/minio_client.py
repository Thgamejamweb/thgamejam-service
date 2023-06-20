from minio import Minio

from config import settings
from database.mysql import database
from modles.file_entity import FileEntity


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

    def get_minio_client(self) -> Minio:
        return self.client


minio_client = MinioClient()


def listen_minio_events():
    with minio_client.client.listen_bucket_notification('web', '') as events:
        for event in events:
            event_dict = event['Records'][0]
            event_name = event_dict['eventName']
            file_name = event_dict['s3']['object']['key']

            if event_name == 's3:ObjectCreated:Put':
                e_tag = event_dict['s3']['object']['eTag']
                session = database.get_db_session()
                file = session.query(FileEntity).filter(FileEntity.deleted == False, FileEntity.e_tag == e_tag).first()
                if file is None:
                    file = FileEntity()
                    file.file_name = file_name
                    file.e_tag = e_tag

                    session.add(file)
                    session.commit()
                    session.close()
