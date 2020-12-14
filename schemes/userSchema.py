from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel
from tools import gen_uuid


class UserLoginSchema(BaseModel):
    username: str
    password: str
    captcha_code: str


class UserCreateSchema(BaseModel):
    username: str
    password: str
    user_id: str = gen_uuid()
    city: str = "上海"
    registe_time: datetime
