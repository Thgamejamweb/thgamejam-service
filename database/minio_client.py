from minio import Minio

from config.conf_pb2 import Bootstrap
from database.mysql import Database
from modles.file_entity import FileEntity


class MinioClient:
    conf: Bootstrap

    def __init__(self, conf: Bootstrap) -> None:
        self.connection_is_active = False
        self.client = None
        self.conf = conf

    def get_minio_connection(self):
        if not self.connection_is_active:
            self.client = Minio(
                endpoint=self.conf.oss.endpoint,
                access_key=self.conf.oss.access_key,
                secret_key=self.conf.oss.secret_key,
                secure=False
            )
        print("对象存储连接成功")
        self.connection_is_active = True
        return self.client

    def get_minio_client(self) -> Minio:
        return self.client


def listen_minio_events(minio_client: MinioClient, database: Database):
    def minio_event():
        with minio_client.client.listen_bucket_notification('web', '') as events:
            for event in events:
                event_dict = event['Records'][0]
                event_name = event_dict['eventName']
                file_name = event_dict['s3']['object']['key']

                if event_name == 's3:ObjectCreated:Put':
                    e_tag = event_dict['s3']['object']['eTag']
                    session = database.get_db_session()
                    file = session.query(FileEntity).filter(FileEntity.deleted is False,
                                                            FileEntity.e_tag == e_tag).first()
                    if file is None:
                        file = FileEntity()
                        file.file_name = file_name
                        file.e_tag = e_tag

                        session.add(file)
                        session.commit()
                        session.close()

    return minio_event
