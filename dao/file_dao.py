from sqlalchemy.orm import Session

from modles.file_entity import FileEntity


def verify_file_eTag(eTag: str, session: Session) -> FileEntity | None:
    return session.query(FileEntity).filter(FileEntity.e_tag == eTag, FileEntity.deleted == False).first()


def create_fileinfo(file: FileEntity, session: Session):
    session.add(file)
    session.commit()
