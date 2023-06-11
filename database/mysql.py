from sqlalchemy import create_engine

from config import settings

engine = create_engine(settings.DATA_BASE_URL, echo=True)

