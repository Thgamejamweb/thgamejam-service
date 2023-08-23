from sqlalchemy.orm import Session

from modles.file_entity import FileEntity


def verify_file_eTag(eTag: str, session: Session) -> FileEntity | None:
    return session.query(FileEntity).filter(FileEntity.e_tag == eTag, FileEntity.deleted == False).first()


def create_fileinfo(file: FileEntity, session: Session):
    session.add(file)
    session.commit()


def update_file_info(file: FileEntity, session: Session):
    session.merge(file)
    session.commit()


def get_file_info_by_id(file_id: int, session: Session) -> FileEntity | None:
    return session.query(FileEntity).filter(FileEntity.id == file_id, FileEntity.deleted == False).first()


def get_file_info_by_name(file_name: str, session: Session) -> FileEntity | None:
    return session.query(FileEntity).filter(FileEntity.file_name == file_name, FileEntity.deleted == False).first()


def get_file_info_by_tag(file_tag: str, session: Session) -> FileEntity | None:
    return session.query(FileEntity).filter(FileEntity.e_tag == file_tag, FileEntity.deleted == False).first()
