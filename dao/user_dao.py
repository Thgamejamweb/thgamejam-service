
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from core.Helper import decrypt_data
from modles.user_entity import UserEntity


def get_userinfo_by_username(username: str, session: Session) -> UserEntity | None:
    try:
        user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()
        return user
    except NoResultFound:
        return None


def get_userinfo_by_id(userid: int, session: Session) -> UserEntity | None:
    return session.query(UserEntity).get(userid)


def update_userinfo(user: UserEntity, session: Session):
    session.merge(user)
    session.commit()


def create_userinfo(user: UserEntity, session: Session) -> UserEntity:
    session.add(user)
    session.commit()
    return user


def verify_user_password(username: str, password: str, session: Session) -> UserEntity:
    user = session.query(UserEntity).filter(UserEntity.name == username, UserEntity.deleted == False).one()

    psw = decrypt_data(password, user.private_key)
    if psw == user.password:
        return user
