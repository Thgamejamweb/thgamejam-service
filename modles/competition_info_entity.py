from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class CompetitionInfoEntity(BaseModel, base):
    __tablename__ = 'competition_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    competition_id = Column(BigInteger, nullable=False, comment='比赛id')
    content = Column(Text, nullable=False, comment='介绍页面富文本')
