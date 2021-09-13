import pydantic
from datetime import datetime
from typing import Optional, Union

class PostBase(pydantic.BaseModel):
    title: str
    content: str
    image: Optional[Union[list, str]] = None


class PostDetailsBase(PostBase):
    id: int
    creation_date: datetime
    nickname: str
    user_id: int
