from datetime import datetime
from sqlalchemy.sql.schema import MetaData
from .user import table_of_users
import sqlalchemy as sql
from app.config import engine

metadata = MetaData()

table_of_posts = sql.Table(
    "posts",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("user_id", sql.ForeignKey(table_of_users.c.id)),
    sql.Column("creation_date", sql.DateTime, default=datetime.now()),
    sql.Column("title", sql.String),
    sql.Column("content", sql.Text),
    sql.Column("image", sql.String, default=None)
)
metadata.create_all(engine)
