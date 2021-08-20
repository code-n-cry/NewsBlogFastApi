from sqlalchemy.sql import expression
from sqlalchemy.sql.schema import MetaData, Table
import sqlalchemy as sql
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
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
    sql.Column("is_active", sql.Boolean, server_default=expression.true(), nullable=False),
    sql.Column("is_superuser", sql.Boolean, default=False, nullable=False)
)
metadata.create_all(engine)