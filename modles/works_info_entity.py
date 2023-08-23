import string

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class WorksInfoEntity(BaseModel, base):
    __tablename__ = 'works_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, nullable=False, comment='团队id')
    works_id = Column(BigInteger, nullable=False, comment="对应的work id")
    image_url_list = Column(Text, nullable=False, comment='轮播图urlList')
    content = Column(Text, nullable=False, comment='作品介绍富文本')
    file_id = Column(BigInteger, nullable=True, comment='作品id')

    def __init__(self, team_id: int, image_url_list: str, content: string, file_id: int, works_id: int):
        self.team_id = team_id
        self.file_id = file_id
        self.image_url_list = image_url_list
        self.content = content
        self.works_id = works_id
