import json
import uuid
import requests
from typing import Optional
import hashlib
from urllib import parse
from consts import *
from fastapi import status
from fastapi.responses import JSONResponse
from fishbase.fish_logger import logger


def gen_uuid() -> str:
    # 生成uuid
    # https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy?rq=1
    return uuid.uuid4().hex


def encrypt_password(password: str) -> str:
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    #  按照node版本这么加密，大概是为了防止暴力解密太容易
    new_password = m.hexdigest()[2:7] + m.hexdigest()
    return new_password


def resp_200(resp_type: Optional[str] = None, message: str = "Success"):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 1,
            'type': resp_type,
            'message': message,
        }
    )


def resp_200_fail(resp_type: Optional[str] = None, message: str = "Success"):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 0,
            'type': resp_type,
            'message': message,
        }
    )


# 根据city_name 获取city信息
def get_city_info_by_name(city_name, city_dict):
    city_info = {}
    for k, v in city_dict.items():
        for content in v:
            if content.get('name') == city_name:
                city_info.update(content)
    return city_info


# 根据city_name 获取city信息
def get_city_info_by_id(city_id, city_dict):
    city_info = {}
    for k, v in city_dict.items():
        for content in v:
            if content.get('id') == city_id:
                city_info.update(content)
    return city_info


# 调用腾讯地图接口获取
def search_place(keyword, city_name, type='search'):
    params = {"key": TECENT_KEY,
              "keyword": parse.quote(keyword),
              "boundary": 'region(' + parse.quote(city_name) + ',0)',
              "page_size": 10}
    result = requests.get(PLACE_URL, params=params)
    return json.loads(result.text)


# 通过geohash 经纬度获取精确位置
def get_acct_place(lat, lng):
    # 根据node版本来，此接口失败可能性较高，得多请求几次
    params = {"key": TECENT_KEY, "location": lat + ',' + lng}
    result = requests.get(GET_ACCT_PLACE_URL, params=params)

    if json.loads(result.text).get('status') != 0:
        params['key'] = TECENT_KEY2
        result = requests.get(GET_ACCT_PLACE_URL, params=params)
        if json.loads(result.text).get('status') != 0:
            params['key'] = TECENT_KEY3
            result = requests.get(GET_ACCT_PLACE_URL, params=params)
            if json.loads(result.text).get('status') != 0:
                params['key'] = TECENT_KEY4
                result = requests.get(GET_ACCT_PLACE_URL, params=params)
                if json.loads(result.text).get('status') != 0:
                    logger.error('获取位置信息异常')
                    return resp_200_fail(resp_type='GET_ACCT_PLACE', message='获取位置信息异常')
                else:
                    return json.loads(result.text)
            else:
                return json.loads(result.text)
        else:
            return json.loads(result.text)
    else:
        return json.loads(result.text)



# for test
if __name__ == '__main__':
    data = [{'_id': ('5fb33753cb75e17964807bd3'), 'name': '小彬彬炸鸡店', 'address': '上海市静安区荣和苑万荣路970弄19号', 'id': 1, 'latitude': 31.288026, 'longitude': 121.440478, 'location': [121.440478, 31.288026], 'phone': '13214234522', 'category': '快餐便当/简餐', 'supports': [{'description': '已加入“外卖保”计划，食品安全有保障', 'icon_color': '999999', 'icon_name': '保', 'id': 7, 'name': '外卖保', '_id': ObjectId('5fb33753cb75e17964807bd6')}, {'description': '准时必达，超时秒赔', 'icon_color': '57A9FF', 'icon_name': '准', 'id': 9, 'name': '准时达', '_id': ObjectId('5fb33753cb75e17964807bd5')}, {'description': '该商家支持开发票，请在下单时填写好发票抬头', 'icon_color': '999999', 'icon_name': '票', 'id': 4, 'name': '开发票', '_id': ObjectId('5fb33753cb75e17964807bd4')}], 'status': 0, 'recent_order_num': 605, 'rating_count': 325, 'rating': 4.8, 'promotion_info': '3元鸡翅，6元吃鸡腿，15元吃整鸡', 'piecewise_agent_fee': {'tips': '配送费约¥5'}, 'opening_hours': ['09:00/21:45'], 'license': {'catering_service_license_image': '', 'business_license_image': ''}, 'is_new': True, 'is_premium': True, 'image_path': '175d40ee1bb1.jpg', 'identification': {'registered_number': '', 'registered_address': '', 'operation_period': '', 'licenses_scope': '', 'licenses_number': '', 'licenses_date': '', 'legal_person': '', 'identificate_date': None, 'identificate_agency': '', 'company_name': ''}, 'float_minimum_order_amount': 20, 'float_delivery_fee': 5, 'distance': '', 'order_lead_time': '', 'description': '便宜吃鸡', 'delivery_mode': {'color': '57A9FF', 'id': 1, 'is_solid': True, 'text': '蜂鸟专送'}, 'activities': [{'icon_name': '新', 'name': '新用户立减', 'description': '新用户首单免费', 'icon_color': '70bc46', 'id': 1, '_id': ObjectId('5fb33753cb75e17964807bd8')}, {'icon_name': '减', 'name': '满减优惠', 'description': '满20减16，满48减40，满100减80', 'icon_color': 'f07373', 'id': 2, '_id': ObjectId('5fb33753cb75e17964807bd7')}], '__v': 0}, {'_id': ObjectId('5fd1bb35ad41899dd87652fe'), 'name': '小俊俊生煎店', 'address': '上海市徐汇区宜山路700号', 'id': 2, 'latitude': 31.176567, 'longitude': 121.417537, 'location': [121.417537, 31.176567], 'phone': '60006000', 'category': '快餐便当/生煎锅贴', 'supports': [{'description': '已加入“外卖保”计划，食品安全有保障', 'icon_color': '999999', 'icon_name': '保', 'id': 7, 'name': '外卖保', '_id': ObjectId('5fd1bb35ad41899dd8765301')}, {'description': '准时必达，超时秒赔', 'icon_color': '57A9FF', 'icon_name': '准', 'id': 9, 'name': '准时达', '_id': ObjectId('5fd1bb35ad41899dd8765300')}, {'description': '该商家支持开发票，请在下单时填写好发票抬头', 'icon_color': '999999', 'icon_name': '票', 'id': 4, 'name': '开发票', '_id': ObjectId('5fd1bb35ad41899dd87652ff')}], 'status': 0, 'recent_order_num': 465, 'rating_count': 847, 'rating': 4.8, 'promotion_info': '小俊俊卖生煎，特别香', 'piecewise_agent_fee': {'tips': '配送费约¥5'}, 'opening_hours': ['06:15/23:15'], 'license': {'catering_service_license_image': '', 'business_license_image': '1764b4331735.png'}, 'is_new': True, 'is_premium': True, 'image_path': '1764b42f3ea4.jpg', 'identification': {'registered_number': '', 'registered_address': '', 'operation_period': '', 'licenses_scope': '', 'licenses_number': '', 'licenses_date': '', 'legal_person': '', 'identificate_date': None, 'identificate_agency': '', 'company_name': ''}, 'float_minimum_order_amount': 20, 'float_delivery_fee': 5, 'distance': '', 'order_lead_time': '', 'description': '可能是上海最好吃的生煎店', 'delivery_mode': {'color': '57A9FF', 'id': 1, 'is_solid': True, 'text': '蜂鸟专送'}, 'activities': [{'icon_name': '减', 'name': '满减优惠', 'description': '满30减5，满60减8', 'icon_color': 'f07373', 'id': 1, '_id': ObjectId('5fd1bb35ad41899dd8765302')}], '__v': 0}]

    print(get_acct_place('31.143234', '121.423575'))
