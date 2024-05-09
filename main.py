import json
import logging
import os
import time

import requests
import schedule

from enum_schedule_type import ScheduleType
from enum_llm_type import LLMType
from util import my_email_util, llm_free_api_util

logger = logging.getLogger(__name__)


def check_tokens():
    """
    检测各个 token 是否存活
    :return:
    """
    email_host = os.getenv("EMAIL_HOST", "")
    email_pass = os.getenv("EMAIL_PASS", "")
    # 发送邮箱
    email_sender = os.getenv("EMAIL_SENDER", "")
    email_sender_name = os.getenv("EMAIL_SENDER_NAME", "")
    # 接收邮箱，多个用英文逗号分隔
    email_receivers = os.getenv("EMAIL_RECEIVERS", "")

    # 检测结果字典
    check_res_dict = {}

    # 获取环境变量中的`ONE_API_BASE_URL`
    one_api_base_url = os.getenv("ONE_API_BASE_URL", "")
    # 如果`ONE_API_BASE_URL`不为空，则调用`one_api`服务的`/api/channel/{channel_id}`接口获取各个`free-api`服务的`baseUrl`、`token`，并检测`token`是否存活
    if one_api_base_url:
        logger.info(f'one_api_base_url = {one_api_base_url}')
        # 获取环境变量中的`ONE_API_TOKEN`
        one_api_token = os.getenv("ONE_API_TOKEN", "")
        if not one_api_token:
            logger.error('`ONE_API_BASE_URL`不为空时，`ONE_API_TOKEN`不能为空！')
            return

        # 遍历LLM类型
        for llm_type in LLMType:
            logger.info(f'llm_type = {llm_type.name}')
            # 获取当前llm_type的`channel_id`
            channel_id = os.getenv(llm_type.env_name_one_api_channel_id, '')
            if not channel_id:
                logger.error(f'未配置`{llm_type.env_name_one_api_channel_id}`，跳过检测')
                continue

            # 调用`one_api`服务的`/api/channel/{channel_id}`接口获取`baseUrl`、`token`
            headers = {
                'Authorization': f'Bearer {one_api_token}'
            }
            response = requests.get(f'{one_api_base_url}/api/channel/{channel_id}', headers=headers)
            resp = response.json()
            logger.info(f'call API [{one_api_base_url}/api/channel/{channel_id}], resp = {resp}')
            resp_data = resp.get('data', {})
            base_url = resp_data.get('base_url', '')
            origin_token_list = resp_data.get('key', '').split(',')
            check_one_llm_type_tokens(llm_type, base_url, origin_token_list, check_res_dict)
    else:
        # 遍历LLM类型
        for llm_type in LLMType:
            # 读取配置的 base_url、token
            base_url = os.getenv(f"{llm_type.env_name_base_url}", "")
            origin_token_list = os.getenv(f"{llm_type.env_name_token}", "").split(',')
            check_one_llm_type_tokens(llm_type, base_url, origin_token_list, check_res_dict)

    # 发送邮件
    mail = my_email_util.Mail(email_host, email_pass, email_sender, email_sender_name)
    # 使用json.dumps()格式化输出
    check_res_str = json.dumps(check_res_dict, indent=4)
    mail.send(email_receivers.split(','), f'【llm-free-api-helper】token_check_res', check_res_str)


def check_one_llm_type_tokens(llm_type: LLMType, base_url: str, origin_token_list: list[str], check_res_dict: dict):
    # 如果`base_url`为空，则跳过检测
    if not base_url:
        logger.info('`base_url`为空，跳过检测')
        return

    # 全部元素去除前后空格，再去除空的元素
    token_list = [origin_token.strip() for origin_token in origin_token_list if origin_token and origin_token.strip()]
    # 遍历 token
    for token in token_list:
        logger.info(f'llm_type = {llm_type.name}, base_url = {base_url}, token = {token}')
        # 如果`token`为空，则跳过检测
        if not token:
            logger.info('`token`为空，跳过检测')
            continue

        # 检测 token 是否存活
        live = llm_free_api_util.token_check(base_url, token)
        logger.info(f'live = {live}')
        # 记录检测结果
        check_res_dict[f'[{llm_type.name}]{token}'] = live


if __name__ == '__main__':
    # 日志系统基本配置
    logging.basicConfig(filename="logs/main.log", filemode="a", format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG, encoding="utf-8")

    # 获取环境变量`SCHEDULE_TYPE`
    schedule_type = os.getenv('SCHEDULE_TYPE')
    # 如果没有配置环境变量`SCHEDULE_TYPE`，则只执行一次
    if not schedule_type:
        logger.info("没有配置环境变量`SCHEDULE_TYPE`，只执行一次")
        check_tokens()
        # 如果这里写`exit(0)`，且`docker-compose.yml`中`restart`的值为`always`，就会一直重启容器，导致重复执行main.py
        time.sleep(3600 * 24 * 365)

    # 根据环境变量配置定时任务
    logger.info(f"配置的定时任务类型为:{schedule_type}")
    schedule_type_enum = ScheduleType.match_name(schedule_type)
    if schedule_type_enum == ScheduleType.INTERVAL:
        # 按时间间隔执行
        interval = int(os.getenv(schedule_type_enum.env_name_of_value, 3600))  # 获取环境变量，默认间隔为3600秒
        schedule.every(interval).seconds.do(check_tokens)
    elif schedule_type_enum == ScheduleType.SPECIFIC_TIME:
        # 在指定时间执行
        specific_time = os.getenv(schedule_type_enum.env_name_of_value, '08:00')  # 获取环境变量，默认时间为"08:00"
        schedule.every().day.at(specific_time).do(check_tokens)
        # 下次执行时间
        # next_run = schedule.next_run()
        # 距离下次执行还有多少秒
        # idle_seconds = schedule.idle_seconds()
        # logger.info(f"距离下次执行[{next_run.strftime('%Y-%m-%d %H:%M:%S')}]还有:{idle_seconds}秒")
    else:
        logger.info("不支持的定时任务类型，退出！")
        # 如果这里写`exit(1)`，且`docker-compose.yml`中`restart`的值为`always/on-failure`，就会一直重启容器，导致重复执行main.py
        time.sleep(3600 * 24 * 365)

    # 主循环，不断检查任务是否需要执行
    while True:
        schedule.run_pending()
        time.sleep(1)
