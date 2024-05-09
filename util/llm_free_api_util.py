#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea0606
@time: 2024/5/9 22:29
"""
import logging
import requests

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
    # 返回'live'字段的值，如果不存在，则返回'message'字段的值
    return resp.get('live', resp.get('message'))
