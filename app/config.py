from databases import Database
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///app/db/news.sqlite"
engine = create_engine(DATABASE_URL, echo=False)
database = Database(DATABASE_URL)