#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea0606
@time: 2024/5/11 22:04
"""
import json
import logging
import sys

import requests

# 日志记录器
logger = logging.getLogger(__name__)


def get_all_channel_date(one_api_base_url: str, one_api_token: str, file_name: str) -> list:
    # 所有渠道数据列表
    all_channel_data_list = []
    # 调用`one_api`服务的`/api/channel`接口分页获取各个渠道的数据
    headers = {
        'Authorization': f'Bearer {one_api_token}'
    }
    # 每一页只能取一定个数的渠道数据，所以需要循环取（p从0开始，不断自增）
    for p in range(0, 100):
        logger.info(f'p = {p}')
        response = requests.get(f'{one_api_base_url}/api/channel?p={p}', headers=headers)
        channel_list_resp = response.json()
        logger.info(f'call API [{one_api_base_url}/api/channel?p={p}], resp = {channel_list_resp}')
        channel_list_resp_data = channel_list_resp.get('data', [])
        # 如果获取的数据为空，跳出循环
        if not channel_list_resp_data:
            logger.info(f'channel_list_resp_data = {channel_list_resp_data}, break')
            break

        # 将获取的数据添加到`all_channel_data_list`中
        all_channel_data_list += channel_list_resp_data

    # 写入文件
    logger.info(f'all_channel_data_list = {all_channel_data_list}, file_name = {file_name}')
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(all_channel_data_list, ensure_ascii=False, indent=4))


def migrate_all_channel_data_to_martialbe(martialbe_one_api_base_url: str, martialbe_one_api_token: str, file_name: str) -> list:
    headers = {
        'Authorization': f'Bearer {martialbe_one_api_token}'
    }
    # 读取文件
    with open(file_name, 'r', encoding='utf-8') as f:
        all_channel_data_list = json.loads(f.read())
        logger.info(f'all_channel_data_list = {all_channel_data_list}')

        # 将`all_channel_data_list`倒序
        reversed_list = all_channel_data_list[::-1]
        # 遍历`reversed_list`
        for channel_data in reversed_list:
            models = channel_data.get('models', '').split(',')
            # 每个元素去除前后空格，再去除空的元素
            models = [model.strip() for model in models if model and model.strip()]
            # 设置测试模型。如果渠道的`models`字段包含`gpt-3.5-turbo`，则将测试模型设置为`gpt-3.5-turbo`，否则将测试模型设置为第一个模型
            test_model = 'gpt-3.5-turbo'
            if test_model not in models:
                test_model = models[0]
            channel_data['test_model'] = test_model
            # 调用`martialbe_one_api`服务的`/api/channel`接口添加渠道
            requests.post(f'{martialbe_one_api_base_url}/api/channel', headers=headers, json=channel_data)


if __name__ == '__main__':
    # 日志系统基本配置
    logging.basicConfig(filename="logs/one_api_migrator.log", filemode="a", format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG,
                        encoding="utf-8")

    # 从命令行获取`one_api_base_url`、`one_api_token`、`martialbe_one_api_base_url`、`martialbe_one_api_token`
    args = sys.argv[1:]
    one_api_base_url = args[0]
    one_api_token = args[1]
    martialbe_one_api_base_url = args[2]
    martialbe_one_api_token = args[3]
    all_channel_data_list_file_name = 'data/all_channel_data_list.json'
    logger.info(
        f'one_api_base_url = {one_api_base_url}, one_api_token = {one_api_token}, martialbe_one_api_base_url = {martialbe_one_api_base_url}, martialbe_one_api_token = {martialbe_one_api_token}')

    # 调用`one_api`服务的`/api/channel`接口，获取各个渠道的数据
    get_all_channel_date(one_api_base_url, one_api_token, all_channel_data_list_file_name)
    # 迁移渠道数据到`martialbe/one-api`
    migrate_all_channel_data_to_martialbe(martialbe_one_api_base_url, martialbe_one_api_token, all_channel_data_list_file_name)
