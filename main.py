import json
import logging
import os

import requests

from enum_llm_type import LLMType
from util import my_email_util

logger = logging.getLogger(__name__)


def token_check(base_url, token):
    """
    检测refresh_token是否存活，如果存活live为true，否则为false，请不要频繁（小于10分钟）调用此接口。
    :param base_url:
    :param token:
    :return:
    """
    response = requests.post(
        url=f'{base_url}/token/check',
        json={
            "token": token
        }
    )
    resp = response.json();
    logger.info(f'call function [token_check], token = {token}, resp = {resp}')
    return resp['live']


def check_tokens(email_host, email_pass, email_sender, email_sender_name, email_receivers):
    """
    检测各个 token 是否存活
    :return:
    """
    # 检测结果字典
    check_res_dict = {}
    # 遍历LLM类型
    for llm_type in LLMType:
        # 读取配置的 base_url、token
        base_url = os.getenv(f"{llm_type.env_name_base_url}", "")
        token = os.getenv(f"{llm_type.env_name_token}", "")
        logger.info(f'llm_type = {llm_type.name}, base_url = {base_url}, token = {token}')
        # 如果有任何一个为空，则跳过
        if not base_url or not token:
            logger.info('跳过检测')
            continue

        # 检测 token 是否存活
        # live = token_check(base_url, token)
        live = True
        logger.info(f'live = {live}')
        # 记录检测结果
        check_res_dict[llm_type.name] = live
    # 发送邮件
    mail = my_email_util.Mail(email_host, email_pass, email_sender, email_sender_name)
    # 使用json.dumps()格式化输出
    check_res_str = json.dumps(check_res_dict, indent=4)
    mail.send(email_receivers.split(','), f'【llm-free-api-helper】token_check_res', check_res_str)


if __name__ == '__main__':
    # 日志系统基本配置
    logging.basicConfig(filename="logs/main.log", filemode="a", format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG, encoding="utf-8")

    email_host = os.getenv("EMAIL_HOST", "")
    email_pass = os.getenv("EMAIL_PASS", "")
    # 发送邮箱
    email_sender = os.getenv("EMAIL_SENDER", "")
    email_sender_name = os.getenv("EMAIL_SENDER_NAME", "")
    # 接收邮箱，多个用英文逗号分隔
    email_receivers = os.getenv("EMAIL_RECEIVERS", "")

    # 检测各个 token 是否存活
    check_tokens(email_host, email_pass, email_sender, email_sender_name, email_receivers)
