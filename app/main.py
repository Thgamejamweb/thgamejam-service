import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_url = os.getenv('DATA_BASE_URL')

engine = create_engine(db_url, echo=True)
connection = engine.connect()

result = connection.execute(text('SELECT * FROM user'))
for row in result:
    print(row)

connection.close()
