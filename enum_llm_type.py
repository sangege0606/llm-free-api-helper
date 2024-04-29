#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea
@time: 2024/4/29 15:08
"""
import enum

class LLMType(enum.Enum):
    GLM = "ChatGLM4", "GLM_REFRESH_TOKEN"
    QWEN = " 通义千问", "LOGIN_TONGYI_TICKET"

    def __init__(self, desc, env_name_token):
        self._desc = desc
        self._env_name_token = env_name_token

    @property
    def desc(self):
        return self._desc

    @property
    def env_name_base_url(self):
        return f"{self.name}_FREE_API_BASE_URL"


    @property
    def env_name_token(self):
        return self._env_name_token