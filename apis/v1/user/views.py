# api接口

from fastapi import APIRouter, Request, Depends
from tools.myTools import resp_200, resp_200_fail
from apis.v1.user.crud import user_crud
from sqlalchemy.orm import Session
from apis.deps import get_db
from typing import Dict
from consts import CustomErr, ERROR_CODE

router = APIRouter()


@router.get('/', tags=['user'])
def get_user_info(user_id: str, db: Session = Depends(get_db)) -> Dict:
    """
    根据user_id获取用户信息， 用户信息返回内容中 应该用response_model过滤password，但方便期间先不做了
    """
    # print(f"请求的session: {request.session}")
    if user_id != 'null':
        user_info = user_crud.get_user_info(db=db, user_id=user_id)
        return resp_200(resp_type='GET_USER_INFO', message='获取用户信息成功')
    else:
        # 根据生产demo拷贝的返回
        return resp_200_fail(resp_type='GET_USER_INFO', message='无用户信息')
    # raise CustomErr(ERROR_CODE,msg_dict={"REASON":"用户信息不存在"})
