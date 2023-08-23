from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class TeamCompetitionEntity(BaseModel, base):
    __tablename__ = 'team_competition'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, nullable=False, comment='团队id')
    competition_id = Column(BigInteger, nullable=False, comment='比赛id')
    works_id = Column(BigInteger, nullable=True, comment='作品id')

    def __init__(self, team_id, competition_id, works_id=None):
        self.team_id = team_id
        self.competition_id = competition_id
        self.works_id = works_id
