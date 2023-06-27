from sqlalchemy import Column, BigInteger, String, event, Boolean
from sqlalchemy.orm import declarative_base, Session

from modles.base_model import BaseModel

base = declarative_base()


class UserEntity(BaseModel, base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=True, comment='用户名')
    email = Column(String(50), nullable=True, comment='邮箱')
    password = Column(String(50), nullable=False, comment='密码')
    description = Column(String(100), nullable=True, comment='用户描述')
    avatar_image = Column(String(500), nullable=True, comment='用户头像url')
    is_staff = Column(Boolean, default=False, nullable=False, comment='是否是主办方')
    public_key = Column(String(4096))
    private_key = Column(String(4096))

    def __repr__(self):
        return f"UserEntity(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}', " \
               f"description='{self.description}', is_staff='{self.is_staff}')"
