#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
from enum import Enum
from dataclasses import dataclass

class Env(str, Enum):
    TEST = "test"
    PROD = "prod"

@dataclass
class Config:
    base_url: str
    corp_id: str
    contact_secret: str

TEST_CONFIG = Config(
    base_url="https://qyapi.weixin.qq.com",
    corp_id="test_corpid",
    contact_secret="test_secret"
)

PROD_CONFIG = Config(
    base_url="https://qyapi.weixin.qq.com",
    corp_id="prod_corpid",
    contact_secret="prod_secret"
)

ENV_MAP = {
    Env.TEST: TEST_CONFIG,
    Env.PROD: PROD_CONFIG
}