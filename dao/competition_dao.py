from datetime import datetime, date

from sqlalchemy import and_
from sqlalchemy.orm import Session

from modles.competition_entity import CompetitionEntity
from modles.competition_info_entity import CompetitionInfoEntity
from modles.team_competition_entity import TeamCompetitionEntity
from modles.team_user_entity import TeamUserEntity


def get_competition_list_by_userid(user_id: int, session: Session) -> list[CompetitionEntity]:
    team_list = session.query(TeamUserEntity).filter(TeamUserEntity.user_id == user_id, TeamUserEntity.is_join == True,
                                                     TeamUserEntity.deleted == False).all()

    join_competition_list = []
    for team in team_list:
        info_list = session.query(TeamCompetitionEntity).filter(TeamCompetitionEntity.team_id == team.team_id).all()
        for info in info_list:
            join_competition_list.append(
                session.query(CompetitionEntity).filter(CompetitionEntity.id == info.competition_id).first())

    return join_competition_list


def get_competition_info_by_team_id(team_id: int, session: Session) -> list[CompetitionEntity]:
    join_competitions = session.query(TeamCompetitionEntity).filter(TeamCompetitionEntity.team_id == team_id).all()

    competitions = []
    for competition in join_competitions:
        competitions.append(
            session.query(CompetitionEntity).filter(CompetitionEntity.id == competition.competition_id).first())

    return competitions


def create_competition(competition: CompetitionEntity, session: Session) -> CompetitionEntity:
    session.add(competition)
    session.commit()
    return competition


def create_competition_info(competition_id: int, content: str, session: Session):
    session.add(CompetitionInfoEntity(competition_id=competition_id, content=content))
    session.commit()


def team_join_competition(team_id: int, competition_id: int, session: Session) -> bool:
    join_info = session.query(TeamCompetitionEntity).filter(TeamCompetitionEntity.team_id == team_id,
                                                            TeamCompetitionEntity.competition_id == competition_id).first()
    if join_info is not None:
        return False

    session.add(TeamCompetitionEntity(team_id=team_id, competition_id=competition_id))
    session.commit()

    return True


def add_team_works_to_competition(competition_id: int, team_id: int, works_id: int, session: Session) -> bool:
    is_join_competition = session.query(TeamCompetitionEntity).filter(TeamCompetitionEntity.team_id == team_id,
                                                                      TeamCompetitionEntity.competition_id == competition_id).first()
    if is_join_competition is None:
        return False

    is_join_competition.works_id = works_id
    session.merge(is_join_competition)
    session.commit()
    return True


def get_signup_competition_list(session: Session) -> list[CompetitionEntity]:
    current_time = datetime.now()
    competition_list = session.query(CompetitionEntity).filter(and_(CompetitionEntity.signup_start_date <= current_time,
                                                                    CompetitionEntity.signup_end_date >= current_time)).all()
    return competition_list


def get_start_competition_list(session: Session) -> list[CompetitionEntity]:
    current_time = datetime.now()
    competition_list = session.query(CompetitionEntity).filter(and_(CompetitionEntity.start_date <= current_time,
                                                                    CompetitionEntity.end_date >= current_time)).all()
    return competition_list


def get_score_competition_list(session: Session) -> list[CompetitionEntity]:
    current_time = datetime.now()
    competition_list = session.query(CompetitionEntity).filter(and_(CompetitionEntity.score_start_date <= current_time,
                                                                    CompetitionEntity.score_end_date >= current_time)).all()
    return competition_list


def get_all_upload_works_by_competitionId(competition_id: int, session: Session) -> list[TeamCompetitionEntity]:
    works_ids = session.query(TeamCompetitionEntity).filter(TeamCompetitionEntity.competition_id == competition_id,
                                                            TeamCompetitionEntity.works_id.isnot(None)).all()
    return works_ids


def get_competition_detail_info_byid(competition_id: int, session: Session) -> CompetitionEntity:
    return session.query(CompetitionEntity).filter(CompetitionEntity.id == competition_id).one()


def get_detail_competition_info_byid(competition_id: int, session: Session) -> CompetitionInfoEntity:
    return session.query(CompetitionInfoEntity).filter(CompetitionInfoEntity.competition_id == competition_id).one()

