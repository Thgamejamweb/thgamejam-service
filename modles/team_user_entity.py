from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class TeamUserEntity(BaseModel, base):
    __tablename__ = 'team_user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, nullable=False, comment='团队id')
    user_id = Column(BigInteger, nullable=False, comment='用户id')
    is_admin = Column(Boolean, nullable=False, comment='是否为管理员')
    is_join = Column(Boolean, nullable=False, comment='是否加入')

    def __init__(self, team_id: int, user_id: int = None, is_admin: bool = None, is_join: bool = None):
        self.team_id = team_id
        self.user_id = user_id
        self.is_admin = is_admin
        self.is_join = is_join
