#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea0606
@time: 2024/5/6 3:00
"""
class Opt:
    def __init__(self, value):
        self.value = value

    def map(self, func):
        if self.value is None:
            return self
        self.value = func(self.value)
        return self

    def get(self):
        return self.value