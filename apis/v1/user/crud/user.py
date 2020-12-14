from sqlalchemy.orm import Session
from models.user import UserInfo


class UserCrud:
    @staticmethod
    def create(db: Session, obj_in) -> UserInfo:
        pass

    """
    根据user_id获取user_info
    """
    @staticmethod
    def get_user_info(db: Session, user_id:int ) -> UserInfo:
        # scalar 和first one 类似，当出现多种情况会报错，first是默认取第一条  one是必需查到一个结果
        # print(db.query(UserInfo).filter(UserInfo.id == user_id).scalar())
        return db.query(UserInfo).filter(UserInfo.id == user_id).scalar()




user_crud = UserCrud()
