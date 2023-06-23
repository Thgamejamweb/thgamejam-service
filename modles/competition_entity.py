from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class CompetitionEntity(BaseModel, base):
    __tablename__ = 'competition'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment='比赛名称')
    staff_id = Column(BigInteger, nullable=False, comment='主办方id')
    description = Column(String(100), comment='比赛简介描述')
    header_imageURL = Column(String(255), comment='头图')
    signup_start_date = Column(DateTime, comment='报名开始日期')
    signup_end_date = Column(DateTime, comment='报名结束日期')
    start_date = Column(DateTime, comment='比赛开始日期')
    end_date = Column(DateTime, comment='比赛结束日期')
    score_start_date = Column(DateTime, comment='投票开始日期')
    score_end_date = Column(DateTime, comment='投票结束日期')
