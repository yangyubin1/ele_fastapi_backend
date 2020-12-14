# api接口

from fastapi import APIRouter, Request, Depends, Body
from tools.myTools import get_city_info_by_name, get_city_info_by_id, search_place, resp_200_fail
# from sqlalchemy.orm import Session
# from apis.deps import get_db
from typing import List, Dict
from data import entry
from consts import CustomErr, ERROR_CODE
from fishbase.fish_logger import logger
from middlewares import MongoClient
import json
from bson import json_util
import pymongo

router = APIRouter()


@router.post('/checkout', tags=['carts'])
def cart_checkout(come_from: str = Body(...),
                  entities: List = Body(...),
                  geohash: str = Body(...),
                  restaurant_id: int = Body(...)) -> Dict:
    """

    :param come_from:
    :param entities:
    :param geohash:
    :param restaurant_id:
    :return:
    """

    # todo 后续优化封装成一个专门的函数处理
    # 1 获取payments  有新任务断更了
    mongo_client = MongoClient(collection='payments')
    payment = list(mongo_client.db.find({}).sort('_id', pymongo.DESCENDING))
    payments = json.loads(json_util.dumps(payment))
    mongo_client.close()
    # 2、获取cart_id
    mongo_client2 = MongoClient(collection='ids')
    result_ids = mongo_client2.db.find_one()
    # 先获取cart_id
    cart_id = result_ids['cart_id'] + 1
    # 然后更新cart_id
    result_ids['cart_id'] = cart_id
    mongo_client2.db.update({}, result_ids)
    mongo_client2.close()
    # 2、获取cart_id

    return {'hello,world'}
