from sqlalchemy.orm import Session

from dao.user_dao import get_userinfo_by_id
from modles.team_entity import TeamEntity
from modles.team_user_entity import TeamUserEntity
from modles.user_entity import UserEntity


def get_team_member_by_team_id(team_id: int, session: Session) -> list[UserEntity]:
    session.query(TeamEntity).filter(TeamEntity.id == team_id, TeamEntity.deleted == False).one()

    users = session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id, TeamUserEntity.is_join == True,
                                                 TeamUserEntity.deleted == False).all()

    user_entities = []
    for user in users:
        user_entity = session.query(UserEntity).get(user.user_id)
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


def change_team_name(team_id: int, team_name: str, session: Session):
    team = session.query(TeamEntity).get(team_id)
    team.name = team_name

    session.merge(team)
    session.commit()


def verify_user_id_team_admin(user_id: int, team_id: int, session: Session) -> bool:
    team_info = session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id,
                                                     TeamUserEntity.user_id == user_id,
                                                     TeamUserEntity.is_admin == True,
                                                     TeamUserEntity.deleted == False).first()
    if team_info is None:
        return False
    return True


def add_user_into_team(user_id: int, team_id: int, session: Session):
    user = session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id, TeamUserEntity.user_id == user_id,
                                                TeamUserEntity.deleted == False).first()

    if user is None:
        session.add(TeamUserEntity(team_id=team_id, user_id=user_id, is_join=False, is_admin=False))
        session.commit()


def get_user_add_team_info(user_id: int, team_id: int, session: Session) -> TeamUserEntity | None:
    return session.query(TeamUserEntity).filter(TeamUserEntity.user_id == user_id,
                                                TeamUserEntity.team_id == team_id,
                                                TeamUserEntity.is_join == False,
                                                TeamUserEntity.deleted == False).first()


def user_join_team(user_info: TeamUserEntity, session: Session):
    user_info.is_join = True
    session.merge(user_info)
    session.commit()


def delete_user_in_team_info(user_id: int, team_id: int, session: Session):
    user_info = session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id,
                                                     TeamUserEntity.user_id == user_id,
                                                     TeamUserEntity.is_admin == False,
                                                     TeamUserEntity.deleted == False).one()
    session.delete(user_info)
    session.commit()


def delete_team(team_id: int, session: Session):
    session.query(TeamEntity).filter(TeamEntity.id == team_id).delete()
    session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id).delete()
    session.commit()


def delete_team_info(team_id: int, user_id: int, session: Session):
    session.query(TeamUserEntity).filter(TeamUserEntity.team_id == team_id,
                                         TeamUserEntity.user_id == user_id,
                                         TeamUserEntity.is_admin == False,
                                         TeamUserEntity.is_join == False,
                                         TeamUserEntity.deleted == False).delete()
    session.commit()


def get_join_team_list_by_userid(user_id: int, session: Session) -> list[TeamEntity]:
    team_into_list = session.query(TeamUserEntity).filter(TeamUserEntity.user_id == user_id,
                                                          TeamUserEntity.is_join == True,
                                                          TeamUserEntity.deleted == False).all()
    team_list = []
    for team in team_into_list:
        team_list.append(session.query(TeamEntity).filter(TeamEntity.id == team.team_id).one())

    return team_list


def get_all_not_join_team_list_by_userid(user_id: int, session: Session) -> list[TeamEntity]:
    team_into_list = session.query(TeamUserEntity).filter(TeamUserEntity.user_id == user_id,
                                                          TeamUserEntity.is_join == False,
                                                          TeamUserEntity.deleted == False).all()
    team_list = []
    for team in team_into_list:
        team_list.append(session.query(TeamEntity).filter(TeamEntity.id == team.team_id).one())
    return team_list
