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
                    file = session.query(FileEntity).filter(FileEntity.deleted == False,
                                                            FileEntity.e_tag == file_name).first()

                    if file is None:
                        file_info = FileEntity()
                        file_info.file_name = file_name
                        file_info.e_tag = e_tag
                        file_info.is_Upload = True

                        session.add(file_info)
                        session.commit()
                    else:
                        file.is_Upload = True
                        session.merge(file)
                        session.commit()

    return minio_event
