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

router = APIRouter()


# ?latitude=31.143234&longitude=121.423575&offset=0&limit=20
# &extras[]=activities&keyword=
# &restaurant_category_id=
# &restaurant_category_ids[]=
# &order_by=
# &delivery_mode[]=
@router.get('/restaurants', tags=['restaurants'])
def shopping_restaurants(latitude: float = Query(None),
                         longitude: float = Query(None),
                         offset: int = 0,
                         limt: int = 20,
                         extras: str = Query(None),
                         keyword: str = Query(None),
                         restaurant_category_ids: str = Query(None),
                         order_by: str = Query(None),
                         delivery_mode: str = Query(None)) -> List:
    mongo_client = MongoClient(collection='shops')
    result = list(mongo_client.db.find())
    mongo_client.close()
    # 一定要处理objectid，默认json无法序列化的
    json_response = json.loads(json_util.dumps(result))
    return json_response


@router.get('/restaurant/{id}', tags=['restaurants'])
def get_restaurant_by_id(id: int = Query(...)) -> Dict:
    mongo_client = MongoClient(collection='shops')
    result = mongo_client.db.find_one({'id': id})
    mongo_client.close()
    json_response = json.loads(json_util.dumps(result))
    return json_response


@router.get('/v2/menu', tags=['restaurants'])
def get_menu_by_id(restaurant_id: int = Query(...)) -> Dict:
    mongo_client = MongoClient(collection='menus')
    result = list(mongo_client.db.find({'restaurant_id': restaurant_id}))
    print(result)
    mongo_client.close()
    json_response = json.loads(json_util.dumps(result))
    return json_response
