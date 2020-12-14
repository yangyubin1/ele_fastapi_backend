from typing import Dict
from fishbase.fish_logger import logger as log

SUCCESS_CODE = '20000'
ERROR_CODE = '20001'
PLACE_URL = 'http://apis.map.qq.com/ws/place/v1/search'
GET_ACCT_PLACE_URL = 'http://apis.map.qq.com/ws/geocoder/v1/'
TECENT_KEY = 'RLHBZ-WMPRP-Q3JDS-V2IQA-JNRFH-EJBHL'
TECENT_KEY2 = 'RRXBZ-WC6KF-ZQSJT-N2QU7-T5QIT-6KF5X'
TECENT_KEY3 = 'OHTBZ-7IFRG-JG2QF-IHFUK-XTTK6-VXFBN'
TECENT_KEY4 = 'Z2BBZ-QBSKJ-DFUFG-FDGT3-4JRYV-JKF5O'
ERROR_MSG_MAP = {
    SUCCESS_CODE: 'success成功',
    ERROR_CODE: 'error,失败原因:{REASON}'
}


class CustomErr(Exception):
    """
    处理各类错误情况
    默认的返回码
    定义 return_code，作为更细颗粒度的错误代码
    定义 msg_dict, 作为显示具体元素的 dict
    """
    status_code = 400

    def __init__(self, return_code: str = None, status_code: int = status_code, msg_dict: Dict = None,
                 payload: Dict = None) -> None:
        self.return_code = return_code
        if status_code is not None:
            self.status_code = status_code
        if msg_dict is not None:
            self.msg_dict = msg_dict
        else:
            self.msg_dict = None
        self.payload = payload

    def to_dict(self) -> Dict:
        """
        构造要返回的错误代码和错误信息的 dict
        """
        rv = dict(self.payload or ())
        rv['resp_code'] = self.return_code  # 增加 dict key: return code
        if self.msg_dict is not None:  # 增加 dict key: message, 具体内容由常量定义文件中通过 return_code 转化而来
            s = ERROR_MSG_MAP[self.return_code].format(**self.msg_dict)
        else:
            s = ERROR_MSG_MAP[self.return_code]
        rv['data'] = s
        rv['message'] = '系统异常'
        log.warning(s)  # 日志打印
        return rv
