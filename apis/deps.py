"""
接口依赖，比如获取数据库连接、获取当前用户等等。
"""
from typing import Generator

from sqlalchemy.orm import Session

from middlewares import db_session


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库连接
    """
    db = None
    try:
        db = db_session()
        yield db
    finally:
        if db is not None:
            db.close()
