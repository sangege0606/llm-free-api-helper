#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea0606
@time: 2024/4/29 15:08
"""
import enum


class LLMType(enum.Enum):
    GLM = "智谱清言", ""
    QWEN = "通义千问", ""
    KIMI = "Moonshot AI", ""
    SPARK = "讯飞星火", ""
    METASO = "秘塔AI", ""

    def __init__(self, desc, placeholder):
        self._desc = desc
        self._placeholder = placeholder

    @property
    def desc(self):
        return self._desc

    @property
    def env_name_base_url(self):
        return f"{self.name}_FREE_API_BASE_URL"

    @property
    def env_name_token(self):
        return f"{self.name}_FREE_API_TOKEN"

    @property
    def env_name_one_api_channel_id(self):
        return f"ONE_API_{self.name}_FREE_API_CHANNEL_ID"
