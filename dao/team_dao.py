from sqlalchemy.orm import Session

from dao.user_dao import get_userinfo_by_id
from modles.team_entity import TeamEntity
from modles.team_user_entity import TeamUserEntity
from modles.user_entity import UserEntity


def get_team_number_by_team_id(team_id: int, session: Session) -> list[UserEntity]:
    session.query(TeamEntity).filter(TeamEntity.id == team_id, TeamEntity.deleted == False).one()

    users = session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id, TeamUserEntity.is_join == True,
                                                 TeamUserEntity.deleted == False).all()

    user_entities = []
    for user in users:
        user_entity = session.query(UserEntity).get(user.id)
        user_entities.append(user_entity)
    return user_entities


def create_team(team_name: str, create_user_id: int, session: Session) -> TeamEntity | None:
    ex_team = session.query(TeamEntity).filter(TeamEntity.name == team_name, TeamEntity.deleted == False).first()
    if ex_team is not None:
        return None

    team = TeamEntity(name=team_name)
    session.add(team)
    session.commit()

    session.add(TeamUserEntity(team_id=team.id, user_id=create_user_id, is_admin=True, is_join=True))
    session.commit()

    return team
