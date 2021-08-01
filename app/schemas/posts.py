import pydantic
from datetime import datetime


class PostBase(pydantic.BaseModel):
    title: str
    content: str


class PostDetailsBase(PostBase):
    id: int
    creation_time: datetime
    nickname: str
