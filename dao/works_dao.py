from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from modles.works_entity import WorksEntity
from modles.team_entity import TeamEntity
from modles.works_info_entity import WorksInfoEntity


def create_works(name: str, header_imageURL: str, team_id: int, session: Session):
    works = session.query(WorksEntity).filter(WorksEntity.name == name).first()
    if works is None:
        work = WorksEntity(team_id=team_id, header_imageURl=header_imageURL, name=name)
        session.add(work)
        session.commit()
        return work
    return None


def create_works_info(workInfoEntity: WorksInfoEntity, session: Session):
    work_info = WorksInfoEntity(team_id=workInfoEntity.team_id,
                                works_id=workInfoEntity.works_id,
                                image_url_list=workInfoEntity.image_url_list,
                                content=workInfoEntity.content,
                                file_id=workInfoEntity.file_id)
    session.add(work_info)
    session.commit()


def get_works_by_name(name: str, session: Session) -> WorksEntity | None:
    return session.query(WorksEntity).filter(WorksEntity.name == name).first()


def get_works_by_id(work_id: int, session: Session) -> WorksEntity | None:
    return session.query(WorksEntity).filter(WorksEntity.id == work_id).first()


def get_works_list_by_term_name(term_name: str, session: Session) -> list[WorksEntity] | None:
    team = session.query(TeamEntity).filter(TeamEntity.name == term_name).one()
    return session.query(WorksEntity).filter(WorksEntity.team_id == team.id).all()


def get_works_list_by_term_id(team_id: int, session: Session) -> list[WorksEntity] | None:
    return session.query(WorksEntity).filter(WorksEntity.team_id == team_id).all()


def get_works_info_by_id(works_id: int, session: Session) -> WorksInfoEntity | None:
    return session.query(WorksInfoEntity).filter(WorksInfoEntity.works_id == works_id).first()


def delete_works_by_id(work_id: int, session: Session):
    session.query(WorksEntity).filter(WorksEntity.id == work_id).one().delete()
    session.query(WorksInfoEntity).filter(WorksInfoEntity.works_id == work_id).delete()
    session.commit()


def update_work(work_entity: WorksEntity, session: Session):
    session.merge(work_entity)
    session.commit()


def update_work_info(work_Info_entity: WorksInfoEntity, session: Session):
    session.merge(work_Info_entity)
    session.commit()


def get_random_four_date(session: Session):
    return session.query(WorksEntity).order_by(func.random()).limit(4).all()


def get_reserve_eight_date(session: Session):
    return session.query(WorksEntity).order_by(getattr(WorksEntity, "id").desc()).limit(8).all()


def get_work_list_by_team_id_list(ids: list[int], session: Session) -> list[WorksEntity]:
    return session.query(WorksEntity).filter(WorksEntity.id.in_(ids)).all()
