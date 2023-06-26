from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class WorksEntity(BaseModel, base):
    __tablename__ = 'works'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, comment='作品名')
    team_id = Column(BigInteger, nullable=False, comment='团队id')
    header_imageURL = Column(String, nullable=False, comment='头图url')

    def __init__(self, team_id: int, header_imageURl: str = None, name: str = None, ):
        self.name = name
        self.team_id = team_id
        self.header_imageURL = header_imageURl
