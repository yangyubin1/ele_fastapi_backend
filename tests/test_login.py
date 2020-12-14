from common import Database, SendMsg, socket_send, handle_string
from config import *
from logs import logger
import os
import datetime
import sys
from generic_tools import MysqlDataBase

sys.path.append("/app/yunwei/send_omcc")  # 导入上送方法的路径
from api import SendtoApi  # 导入模块中的方法

# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2019/6/6 14:22'

"""
逾期1分钟，检索前3分钟-前1分钟的交易情况 每隔2分钟
SELECT   a.gate_id,a.bank_no,a.trd_status,count(*)   FROM bipusr.outcome_bank_record t,bipusr.outcome_record a WHERE
a.recv_date='20190702'
and t.outcome_record_id=a.id
and t.bank_rtn_code like 'A_'
group by a.gate_id,a.bank_no,a.trd_status

网关

"""
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

now = datetime.datetime.now()
# 3分钟前
start_time = (now - datetime.timedelta(minutes=3)).strftime('%H%M%S')
start_time_show = (now - datetime.timedelta(minutes=3)).strftime('%H:%M:%S')
# 1分钟前
end_time = (now - datetime.timedelta(minutes=1)).strftime('%H%M%S')
end_time_show = (now - datetime.timedelta(minutes=1)).strftime('%H:%M:%S')

# socket_send(IP_PORT, handle_string(message, CODE_DICT.get(i).get('code_1'), CODE_DICT.get(i).get('code_2'),
#                                    CODE_DICT.get(i).get('code_3')))

if __name__ == '__main__':
    status_yyb = 'N'
    start_time_yyb = datetime.datetime.now()
    try:
        conn = MysqlDataBase(host=host, user=username, password=passwd, port=3306, db=db)
        logger.info("数据库连接成功")
        # 查询总数
        rule_result_all = conn.pd_read_sql(sql=sql_0, params={'start_time': start_time, 'end_time': end_time})
        # 查询同一个bank_name是否10分钟大于等于2条
        rule_result_1 = conn.pd_read_sql(sql=sql_1, params={'start_time': start_time, 'end_time': end_time})
        # 查询同一个gateid ------
        rule_result_2 = conn.pd_read_sql(sql=sql_2, params={'start_time': start_time, 'end_time': end_time})
        conn.close_db()
        logger.info(rule_result_all)
        if rule_result_all[0]['sl'] >= 2:
            logger.info('存在异常')
            content = ''
            content_bank = ''
            content_gate_id = ''
            for n in range(0, len(rule_result_1)):
                content_bank += '从{0}到{1}，{2}出现{3}笔A系列返回码的情况\n'.format(start_time_show, end_time_show,
                                                                       rule_result_1[n]['bank_name'],
                                                                       rule_result_1[n]['sl'])
            for n in range(0, len(rule_result_2)):
                content_gate_id += '其中，{2}出现{3}笔\n'.format(rule_result_2[n]['gate_id'], rule_result_2[n]['sl'])
            content = content_bank + content_gate_id
            logger.info("播报内容:{}".format(content))
            # SendMsg(title1, content).send()
            socket_send(IP_PORT, handle_string(content, CODE_DICT.get('code_1'), CODE_DICT.get('code_2'),
                                               CODE_DICT.get('code_3')))
        else:
            logger.info('无异常信息')
    except Exception as e:  # 如果异常，测试日志输出异常，状态改成C
        print('竟然有异常,异常原因:', e)
        logger.error(e)
        status_yyb = 'C'
    end_time_yyb = datetime.datetime.now()  # 获取结束时间
    interval_time_yyb = (end_time_yyb - start_time_yyb).seconds  # 获取间隔时间
    content_yyb = {'data_source_test': 'orcl_228', 'data_source_prod': 'orcl_189',
                   'chargeman': 'yubin.yang', 'status': status_yyb, 'business_type': 'jc',
                   'lens_code': '43;YWJK;CODEA1', 'email_address': '', 'dingding_token': '',
                   'monitor_name': 'outcome_a_yyb', 'route': os.path.abspath(__file__),
                   'config_route': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.py'),
                   'interval_time': interval_time_yyb,
                   'auditor': 'yubin.yang'}
    logger.info('开始上送配置')
    SendtoApi(**content_yyb).send_api()  # 根据content字典内容上送给api结果
    logger.info('结束上送')
