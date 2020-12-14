# api接口

from fastapi import APIRouter, Request, Depends
from tools.myTools import get_city_info_by_name, get_city_info_by_id, search_place, resp_200_fail
# from sqlalchemy.orm import Session
# from apis.deps import get_db
from typing import Dict
from data import cities
from consts import CustomErr, ERROR_CODE
from fishbase.fish_logger import logger

router = APIRouter()


@router.get('/', tags=['pois'])
def search_user_place(type: str = 'search', city_id: int = 1, keyword: str = None) -> Dict:
    """
    根据type,city_id和keyword查询最近的地点
     [{"name":"普天科创产业园","address":"上海市徐汇区宜山路700号","latitude":31.176567,"longitude":121.417537,"geohash":"31.176567,121.417537"},{"name":"上海普天工业园A区","address":"上海市奉贤区南桥环城北路999号","latitude":30.955165,"longitude":121.442938,"geohash":"30.955165,121.442938"},{"name":"上海普天科技产业基地三期","address":"上海市徐汇区 ","latitude":31.177047,"longitude":121.418087,"geohash":"31.177047,121.418087"},{"name":"上海普天工业园B区","address":"上海市奉贤区南桥环城北路1099号","latitude":30.953371,"longitude":121.440985,"geohash":"30.953371,121.440985"},{"name":"上海普天工业园","address":"上海市奉贤区沪杭公路1377号内部西南方向80米","latitude":30.953068,"longitude":121.444041,"geohash":"30.953068,121.444041"},{"name":"上海普天信息产业园B2楼","address":"上海市徐汇区田林街道宜山路700号普天信息产业园b2座","latitude":31.175891,"longitude":121.41769,"geohash":"31.175891,121.41769"},{"name":"中国普天","address":"上海市嘉定区墨玉南路888号上海国际汽车城大厦6层","latitude":31.281632,"longitude":121.165238,"geohash":"31.281632,121.165238"},{"name":"上海普天物流有限公司(浏翔公路)","address":"上海市嘉定区浏翔公路2377号","latitude":31.356752,"longitude":121.309631,"geohash":"31.356752,121.309631"},{"name":"普天信息产业园C1楼","address":"上海市徐汇区 ","latitude":31.175351,"longitude":121.418253,"geohash":"31.175351,121.418253"},{"name":"中国普天上海信息工业园区","address":"上海市奉贤区南桥环城北路168号","latitude":30.95887,"longitude":121.45285,"geohash":"30.95887,121.45285"}]
    """

    city_info = get_city_info_by_id(city_id, cities.city_info)
    # 搜索地址
    place_info = search_place(keyword=keyword, city_name=city_info['name'], type=type)
    logger.info(f"查询的位置信息为:{place_info}")
    # name: item.title,
    # address: item.address,
    # latitude: item.location.lat,
    # longitude: item.location.lng,
    # geohash: item.location.lat + ',' + item.location.lng
    if place_info.get('status') == 0:
        city_list = []
        for place in place_info['data']:
            data = {'name': place.get('title'), 'address': place.get('address'),
                    'latitude': place.get('location').get('lat'), 'longitude': place.get('location').get('lng'),
                    'geohash': ','.join([str(place.get('location').get('lat')), str(place.get('location').get('lng'))])}
            city_list.append(data)
        return city_list
    else:
        logger.error('调用腾讯API地图查询接口查询失败，请稍后再试')
        return resp_200_fail(resp_type='posi_search', message='调用腾讯API地图查询接口查询失败，请稍后再试')
