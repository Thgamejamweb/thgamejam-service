from sqlalchemy import create_engine

from app.config import DATA_BASE_URL

engine = create_engine(DATA_BASE_URL, echo=True)

