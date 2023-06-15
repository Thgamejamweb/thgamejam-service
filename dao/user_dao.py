from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from modles.user_entity import UserEntity


def get_userinfo_by_username(username: str, session: Session) -> UserEntity | None:
    try:
        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()
        return user
    except NoResultFound:
        return None


def update_userinfo(user: UserEntity, session: Session) -> bool:
    try:
        session.merge(user)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def create_userinfo(user: UserEntity, session: Session) -> UserEntity:
    try:
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(f"Error occurred while creating user: {e}")
        return None



def verify_user_password(username: str, password: str, session: Session) -> UserEntity:
    try:
        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.password == password,
                                                UserEntity.deleted == False).one()
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="UserInfo can not found or password is incorrect")
