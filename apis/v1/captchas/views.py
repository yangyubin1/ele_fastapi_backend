# api接口

from fastapi import APIRouter, Response
from typing import Dict
from fishbase.fish_logger import logger
from consts import CustomErr, ERROR_CODE
import base64
import random
import os
from captcha.image import ImageCaptcha

router = APIRouter()


@router.post('/', tags=['captchas'])
def get_captchas(response: Response) -> Dict:
    """
    获取验证码信息
    {status: 1, code:'图片url'}

    """
    code = str(int(random.random() * 9000 + 1000))
    logger.info(f'验证码为:{str(code)}')
    image = ImageCaptcha().generate_image(code)
    image.save('./%s.jpg' % code)
    file_path = os.path.join(os.getcwd(), f'{code}.jpg')
    try:
        with open(file_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            url = 'data:image/jpeg;base64,%s' % s
            response.set_cookie(key='cap', value=code, max_age=3600)
            return {'status': 1, 'code': url}
    except Exception as e:
        raise CustomErr(ERROR_CODE, msg_dict={"REASON": "获取验证码信息失败:{}".format(e)})
    finally:
        os.remove(file_path)
