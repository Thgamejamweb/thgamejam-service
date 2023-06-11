from sqlalchemy import Column, BigInteger, String, event, Boolean
from sqlalchemy.orm import declarative_base, Session

from modles.base_model import BaseModel

base = declarative_base()


class User(BaseModel, base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=True, comment='用户名')
    email = Column(String(50), nullable=True, comment='邮箱')
    password = Column(String(50), nullable=False, comment='密码')



