from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import declarative_base

from modles.base_model import BaseModel

base = declarative_base()


class FileEntity(BaseModel, base):
    __tablename__ = 'file'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(64), nullable=False, comment='文件名')
    e_tag = Column(String(50), nullable=False, comment='文件哈希')
    is_Upload = Column(Boolean, default=False, nullable=False, comment='是否上传成功')
