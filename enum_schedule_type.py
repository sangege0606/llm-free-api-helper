#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: sangea0606
@time: 2024/4/29 15:08
"""
import enum
from dataclasses import dataclass, field
from typing import Optional

from util.Opt import Opt


# 使用dataclass装饰器定义一个数据类，用于混入到枚举类中。这个装饰器可以自动为类生成特殊方法，如__init__()和__repr__()等。
@dataclass
class ScheduleTypeDataMixin:
    # 描述
    desc: str
    # 调度类型值的环境变量名
    env_name_of_value: str
    # 占位符：默认为True，不在类的字符串表示中显示。field函数用于进一步配置数据类的字段，例如设置repr=False表示在类的字符串表示中不包含该字段。
    placeholder: bool = field(repr=False, default=True)


# 定义一个枚举类，继承自ScheduleTypeDataMixin和enum.Enum
class ScheduleType(ScheduleTypeDataMixin, enum.Enum):
    # 定义枚举成员INTERVAL，代表间隔调度类型
    INTERVAL = "间隔", "SCHEDULE_JOB_INTERVAL"
    # 定义枚举成员SPECIFIC_TIME，代表指定时间调度类型
    SPECIFIC_TIME = "指定时间", "SCHEDULE_JOB_SPECIFIC_TIME"

    @classmethod
    def match_name(cls, name_str) -> Optional['ScheduleType']:
        # 将输入字符串转换为大写
        name_str_upper = name_str.upper()
        # 遍历枚举类中的所有成员
        for member in cls:
            # 如果成员的name与输入字符串大写形式匹配
            if member.name == name_str_upper:
                # 返回匹配到的枚举成员
                return member
        # 如果没有找到匹配项，返回None
        return None

if __name__ == '__main__':
    print(ScheduleType.match_name('interval').env_name_of_value)
    print(Opt(ScheduleType.match_name('intervalll')).map(lambda x: x.env_name_of_value).get())
