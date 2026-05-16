#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import time
import requests

# 企业微信配置
corpid =  "wwea6e80ed8c327bf0"
corpsecret = "Yfw8DMFyAs9Re964-PfloE81tWhQDdEOW73ObXJq-lk"

# 全局缓存：保存token和过期时间
cache = {
    "access_token": None,
    "expires_time": 0     # 过期时间
}

def get_token():
    """自动缓存token，2小时获取一次"""
    global cache

    # 当前时间
    now = time.time()

    # 1.如果缓存里有token，且没过期 ➡️ 直接返回
    if cache["access_token"] and now < cache["expires_time"]:
        return cache["access_token"]

    # 2.没有token或已过期 ➡️ 重新获取
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        "corpid": corpid,
        "corpsecret": corpsecret,
    }
    response = requests.get(url, params=params).json()
    access_token = response["access_token"]
    expires_in = response["expires_in"]      # 企业微信固定2小时 = 7200秒

    # 3.存入缓存，并设置过期时间（提前60秒过期，更安全）
    cache["access_token"] = access_token
    cache["expires_time"] = now + expires_in - 60

    return access_token



import requests
from config.settings import CONFIG
from base.logger import get_logger

logger = get_logger()

class WeComTokenManager:
    _token = None

    @classmethod
    def get_token(cls):
        if cls._token:
            return cls._token

        url = f"{CONFIG.base_url}/cgi-bin/gettoken"
        params = {
            "corpid": CONFIG.corp_id,
            "corpsecret": CONFIG.contact_secret
        }

        resp = requests.get(url, params=params).json()
        if resp["errcode"] != 0:
            raise RuntimeError("获取 token 失败")

        cls._token = resp["access_token"]
        return cls._token