# api接口

from fastapi import APIRouter, Request, Depends, Path
from tools.myTools import get_city_info_by_name, get_city_info_by_id, search_place
# from sqlalchemy.orm import Session
# from apis.deps import get_db
from typing import Dict
from data import cities
from consts import CustomErr, ERROR_CODE
from fishbase.fish_logger import logger

router = APIRouter()


@router.get('/', tags=['cities'])
def get_cities(type: str) -> Dict:
    """
    根据type返回城市信息，直接返回的是一个json
    {"pinyin":"shanghai","is_map":true,"longitude":121.473701,"latitude":31.23037,"sort":1,"area_code":"021","abbr":"SH","name":"上海","id":1}
    """
    # 先猜测用户是哪个区域的

    if type == 'guess':
        # 此处为了方便，就不调用第三方接口了，直接返回上海
        city_name = '上海'
        # 根据城市名字从city_info中获取城市信息
        # city_info = {}
        # for k, v in cities.city_info.items():
        #     for content in v:
        #         if content.get('name') == city_name:
        #             city_info.update(content)
        city_info = get_city_info_by_name(city_name, cities.city_info)
        if not city_info:
            raise CustomErr(ERROR_CODE, msg_dict={"REASON": "根据定位信息无法查询到城市信息"})
        logger.info('guess获取的城市信息:{}'.format(city_info))
        return city_info

    if type == 'hot':
        # 此处为了方便，就不调用第三方接口了，直接返回上海
        # 根据城市名字从city_info中获取城市信息
        return cities.city_info['hotCities']

    if type == 'group':
        # 此处为了方便，就不调用第三方接口了，直接返回上海
        city_name = '上海'
        # 根据城市名字从city_info中获取城市信息
        return cities.city_info


@router.get('/{id}', tags=['cities'])
def get_cities(id: int = Path(...)) -> Dict:
    city_info = get_city_info_by_id(id,cities.city_info)
    return city_info
