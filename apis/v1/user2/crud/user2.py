from sqlalchemy.orm import Session
from models.user import UserInfo
from schemes.userSchema import UserCreateSchema


class UserCrud:
    """

    """

    @staticmethod
    def user_create(db: Session, obj_in: UserCreateSchema) -> UserInfo:
        print(f'ojb_in:{obj_in}')
        db_obj = UserInfo(username=obj_in.username, user_id=obj_in.user_id, city=obj_in.city,
                          registe_time=obj_in.registe_time, password=obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    """
    根据user_name获取user_info
    """

    @staticmethod
    def get_user_info_by_name(db: Session, user_name: str) -> UserInfo:
        # scalar 和first one 类似，当出现多种情况会报错，first是默认取第一条  one是必需查到一个结果
        # print(db.query(UserInfo).filter(UserInfo.id == user_id).scalar())
        return db.query(UserInfo).filter(UserInfo.username == user_name).first()


user_crud = UserCrud()
