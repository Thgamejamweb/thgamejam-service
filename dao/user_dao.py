from typing import Any

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from core.Helper import encrypt_data, decrypt_data
from modles.user_entity import UserEntity


def get_userinfo_by_username(username: str, session: Session) -> UserEntity | None:
    try:
        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()
        return user
    except NoResultFound:
        return None


def get_userinfo_by_id(userid: int, session: Session) -> UserEntity | None:
    return session.query(UserEntity).get(userid)


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
        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()

        psw = decrypt_data(password, user.private_key)
        if psw == user.password:
            return user
        else:
            raise HTTPException(status_code=403, detail="Password error")

    except NoResultFound:
        raise HTTPException(status_code=404, detail="UserInfo can not found or password is incorrect")
