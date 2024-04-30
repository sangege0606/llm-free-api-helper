#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea
@time: 2024/4/29 15:08
"""
import enum


class LLMType(enum.Enum):
    GLM = "ChatGLM4", ""
    QWEN = "通义千问", ""

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
