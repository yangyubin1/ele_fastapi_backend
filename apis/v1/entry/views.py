# api接口
import json

from bson import json_util
from fastapi import APIRouter, Request, Depends
from tools.myTools import get_city_info_by_name, get_city_info_by_id, search_place, resp_200_fail
# from sqlalchemy.orm import Session
# from apis.deps import get_db
from typing import List
from data import entry
from consts import CustomErr, ERROR_CODE
from fishbase.fish_logger import logger
from middlewares import MongoClient

router = APIRouter()


@router.get('/', tags=['entry'])
def index_entry() -> List:
    """

    :param type:
    :param city_id:
    :param keyword:
    :return:
    """
    # 根据id排序后返回
    # entry.entry_info.sort(key=lambda k: k.get('id'))
    # return entry.entry_info
    mongo_client = MongoClient(collection='entries')
    result = list(mongo_client.db.find())
    mongo_client.close()
    # 一定要处理objectid，默认json无法序列化的
    json_response = json.loads(json_util.dumps(result))
    return json_response
