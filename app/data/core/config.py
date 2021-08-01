from starlette.config import Config

config = Config(".env")
DATABASE_URL = config("CNC_DATABASE_URL", cast=str, default="db/news.sqlite")
