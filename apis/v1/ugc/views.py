# api接口

from fastapi import APIRouter, Request, Depends, Query
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


# ?latitude=31.143234&longitude=121.423575&offset=0&limit=20
# &extras[]=activities&keyword=
# &restaurant_category_id=
# &restaurant_category_ids[]=
# &order_by=
# &delivery_mode[]=
@router.get('/restaurants/{restaurant_id}/ratings', tags=['restaurants'])
def get_rating_info(restaurant_id: int = Query(...)) -> List:
    mongo_client = MongoClient(collection='ratings')
    result = list(mongo_client.db.find({'restaurant_id': restaurant_id}).sort('_id', pymongo.DESCENDING))
    detail = [i['ratings'] for i in result]
    mongo_client.close()
    # 一定要处理objectid，默认json无法序列化的
    json_response = json.loads(json_util.dumps(detail))
    return json_response

"""
商铺评论详情
"""


@router.get('/restaurants/{restaurant_id}/ratings/scores', tags=['restaurants'])
def get_rating_scores_info(restaurant_id: int = Query(...)) -> List:
    mongo_client = MongoClient(collection='ratings')
    result = list(mongo_client.db.find({'restaurant_id': restaurant_id}).sort('_id', pymongo.DESCENDING))
    detail = [i['scores'] for i in result]
    mongo_client.close()
    # 一定要处理objectid，默认json无法序列化的
    json_response = json.loads(json_util.dumps(detail))
    return json_response


"""
商户评论tag
"""


@router.get('/restaurants/{restaurant_id}/ratings/tags', tags=['restaurants'])
def get_rating_tags_info(restaurant_id: int = Query(...)) -> List:
    mongo_client = MongoClient(collection='ratings')
    result = list(mongo_client.db.find({'restaurant_id': restaurant_id}).sort('_id', pymongo.DESCENDING))
    detail = [i['tags'] for i in result]
    mongo_client.close()
    # 一定要处理objectid，默认json无法序列化的
    json_response = json.loads(json_util.dumps(detail))
    return json_response
