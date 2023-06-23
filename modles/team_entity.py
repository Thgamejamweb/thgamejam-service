from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class TeamEntity(BaseModel, base):
    __tablename__ = 'team'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, comment='团队名')
