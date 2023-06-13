from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from modles.user_entity import UserEntity


def get_userinfo_by_username(username: str, session: Session) -> UserEntity:
    try:

        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="UserInfo can not found")


def update_userinfo(user: UserEntity, session: Session) -> bool:
    try:
        session.merge(user)
        session.commit()
        return True
    except:
        session.rollback()
        return False
