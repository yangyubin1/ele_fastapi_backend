# api接口

from fastapi import APIRouter, Request, Depends, Path
from tools.myTools import get_city_info_by_name, get_city_info_by_id, search_place, resp_200_fail, get_acct_place
# from sqlalchemy.orm import Session
# from apis.deps import get_db
from typing import Dict
from data import cities
from consts import CustomErr, ERROR_CODE
from fishbase.fish_logger import logger

router = APIRouter()


@router.get('/{geohash}', tags=['pois'])
def search_user_place_v2(geohash: str = Path(...)) -> Dict:
    position_list = geohash.split(',')
    lat_1, lng_1 = position_list[0], position_list[1]
    # 通过geohash获取精确位置
    res = get_acct_place(lat_1, lng_1)
    # const address = {
    #               address: result.result.address,
    #               city: result.result.address_component.province,
    #               geohash,
    #           latitude: poisArr[0],
    #                     longitude: poisArr[1],
    # name: result.result.formatted_addresses.recommend,
    address = {"address": res['result']['address'], "city": res['result']['address_component']['province'],
               "geohash": geohash, "latitude": lat_1, "longitude": lng_1,
               "name": res['result']['formatted_addresses']['recommend']}

    return address
