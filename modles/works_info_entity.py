from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class WorksEntity(BaseModel, base):
    __tablename__ = 'works_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, nullable=False, comment='团队id')
    image_url_list = Column(Text, nullable=False, comment='轮播图urlList')
    content = Column(Text, nullable=False, comment='作品介绍富文本')
    file_id = Column(BigInteger, nullable=True, comment='作品id')
