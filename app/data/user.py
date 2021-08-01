from sqlalchemy.sql import expression
from sqlalchemy.sql.schema import MetaData, Table
import sqlalchemy as sql
from uuid import uuid4
from sqlalchemy.sql.sqltypes import Integer
from app.config import engine

metadata = MetaData()

table_of_users = Table(
    "users",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("nickname", sql.String),
    sql.Column("email", sql.String, unique=True, nullable=False, index=True),
    sql.Column("hashed_password", sql.String),
    sql.Column("is_active", sql.Boolean, default=expression.true(), nullable=False),
    sql.Column("is_superuser", sql.Boolean, default=False, nullable=True)
)
table_of_tokens = Table(
    "tokens",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("token", sql.String, nullable=False, unique=True, index=True, default=str(uuid4())),
    sql.Column("expires", sql.DateTime),
    sql.Column("user_id", sql.ForeignKey("users.id"))
)
metadata.create_all(engine)