from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.conf_pb2 import Bootstrap
from modles.base_model import CustomSession


class Database:
    conf: Bootstrap

    def __init__(self, conf: Bootstrap) -> None:
        self.connection_is_active = False
        self.engine = None
        self.conf = conf

    def get_db_connection(self):
        if not self.connection_is_active:
            connect_args = {"connect_timeout": self.conf.database.connect_timeout}
            try:
                self.engine = create_engine(self.conf.database.source,
                                            pool_size=self.conf.database.pool_size,
                                            pool_recycle=self.conf.database.pool_recycle,
                                            pool_timeout=self.conf.database.pool_timeout,
                                            connect_args=connect_args)
                print("数据库连接成功")
                self.connection_is_active = True
            except Exception as e:
                print("Error connecting to MySQL DB:", e)
        return self.engine

    def get_db_session(self):
        if self.connection_is_active is False:
            self.get_db_connection()  # 确保数据库引擎已经被创建和配置
        try:
            session = sessionmaker(bind=self.engine, class_=CustomSession)
            return session()
        except Exception as e:
            print("Error getting DB session:", e)
            return None
