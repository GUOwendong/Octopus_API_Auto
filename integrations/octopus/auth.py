#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证层 (Auth Layer)
====================
职责：通过账号密码调用 /login 接口获取 JWT Token。
token 缓存起来，过期自动重新登录。

使用方式：
    auth = OctopusAuth()        # 自动从 .env 读用户名密码
    token = auth.get_token()    # 返回 token（首次调用自动登录）
"""

import os

import requests

from common.log_utils import log
from integrations.auth_provider import AuthProvider


class OctopusAuth(AuthProvider):
    """
    八爪鱼系统认证类
    ----------------
    认证方式：账号密码 → POST /login → 返回 JWT Token
    继承 AuthProvider，必须实现 get_token() 方法
    """

    def __init__(self):
        """从 .env 读取用户名和密码"""
        self._token = ""
        self._base_url = os.getenv("OCTOPUS_BASE_URL", "http://api.wxorder.taover.com")
        self._username = os.getenv("OCTOPUS_USERNAME", "")
        self._password = os.getenv("OCTOPUS_PASSWORD", "")

    def login(self):
        """调 /login 接口，用账号密码获取 token"""
        log.info("🔐 开始登录获取 token...")
        resp = requests.post(
            url=f"{self._base_url}/login",
            json={"username": self._username, "password": self._password},
        )
        if resp.status_code != 200:
            raise RuntimeError(f"登录失败, HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        if data.get("code") != "ok":
            raise RuntimeError(f"登录失败: {data.get('error', data)}")

        self._token = (data.get("data") or {}).get("token", "")
        if not self._token:
            raise RuntimeError(f"登录响应缺少 token: {data}")
        log.info(f"✅ 登录成功, token前20字符: {self._token[:20]}...")

    def get_token(self, force_refresh=False):
        """
        获取认证 token
        - 首次调用 / token 为空 → 自动登录
        - force_refresh=True → 强制重新登录
        """
        if force_refresh or not self._token:
            self.login()
        return self._token

    def is_valid(self):
        """判断当前 token 是否有效"""
        return bool(self._token)
