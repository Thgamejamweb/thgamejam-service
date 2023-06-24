from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, TypeDecorator, event
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import Session


class BaseModel:
    ctime = Column(DateTime, nullable=True, default=datetime.utcnow, comment='创建时间')
    mtime = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow, comment='修改时间')
    deleted = Column(Boolean, default=False, nullable=False, comment='是否删除')


class CustomSession(Session):
    def delete(self, model):
        if hasattr(model, 'deleted'):
            model.deleted = True
        self.merge(model)
