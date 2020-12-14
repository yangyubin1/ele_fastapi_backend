# api接口
import datetime

from fastapi import APIRouter, Request, Depends, Cookie
from tools.myTools import resp_200_fail, resp_200, encrypt_password
from apis.v1.user2.crud import user_crud
from schemes.userSchema import UserLoginSchema, UserCreateSchema
from sqlalchemy.orm import Session
from apis.deps import get_db
from typing import Dict
from consts import CustomErr, ERROR_CODE

router = APIRouter()


@router.post('/', tags=['user'])
def user_login(login_info: UserLoginSchema, cap: str = Cookie(None), db: Session = Depends(get_db)) -> Dict:
    """
    根据user_id获取用户信息
    """
    # print(
    #     f"打印请求的参数，user_name: {login_info.username}, password:{login_info.password}, "
    #     f"captcha_code:{login_info.captcha_code},cookie中的cap:{cap}")

    username = login_info.username
    password = login_info.password
    captcha_code = login_info.captcha_code

    if not cap:
        return resp_200_fail(resp_type='USER_LOGIN', message='验证码已过期')
    if not username:
        return resp_200_fail(resp_type='USER_LOGIN', message='用户名未填写')
    if not password:
        return resp_200_fail(resp_type='USER_LOGIN', message='密码未填写')
    if not captcha_code:
        return resp_200_fail(resp_type='USER_LOGIN', message='验证码未填写')
    if int(cap) != int(captcha_code):
        return resp_200_fail(resp_type='USER_LOGIN', message='验证码不正确')
    user_info = user_crud.get_user_info_by_name(db=db, user_name=username)
    # 密码加密
    hash_password = encrypt_password(password)
    if not user_info:
        # 新增用户环节
        obj_in = UserCreateSchema(username=username, registe_time=datetime.datetime.now(), password=hash_password)
        user_crud.user_create(db=db, obj_in=obj_in)
        new_user_info = user_crud.get_user_info_by_name(db=db, user_name=username)
        return new_user_info
    # 如果信息存在 则判断密码是否一致
    elif user_info.password != hash_password:
        return resp_200_fail(resp_type='USER_LOGIN', message='密码错误，请重新输入')
    else:
        return user_info

    #raise CustomErr(ERROR_CODE,msg_dict={"REASON":"用户信息不存在"})
