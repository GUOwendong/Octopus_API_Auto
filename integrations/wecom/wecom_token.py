#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信 AccessToken 管理器（单例，自动缓存，实现 AuthProvider）"""

import os
import time

import requests

from common.log_utils import log
from config.global_config import TIMEOUT
from integrations.auth_provider import AuthProvider
from integrations.wecom.wecom_error_code import extract_error_from_response, is_success


class WeComTokenManager(AuthProvider):
    """企业微信 AccessToken 管理器（单例），实现 AuthProvider 接口"""

    _instance = None
    _token: str = None
    _expires_at: float = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self, force_refresh: bool = False) -> str:
        now = time.time()
        if not force_refresh and self._token and now < self._expires_at:
            log.debug("使用缓存的 access_token")
            return self._token

        log.info("获取新的 access_token")
        base_url = os.getenv("WECOM_BASE_URL", "https://qyapi.weixin.qq.com")
        corp_id = os.getenv("WECOM_CORP_ID", "")
        contact_secret = os.getenv("WECOM_CONTACT_SECRET", "")

        url = f"{base_url}/cgi-bin/gettoken"
        params = {"corpid": corp_id, "corpsecret": contact_secret}
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            log.error(f"请求 token 失败: {e}")
            raise RuntimeError(f"无法获取 access_token: {e}")

        if not is_success(data):
            error = extract_error_from_response(data)
            log.error(f"获取 token 业务失败: {error}")
            raise RuntimeError(f"获取 token 失败: {error}")

        self.__class__._token = data["access_token"]
        expires_in = data.get("expires_in", 7200)
        self.__class__._expires_at = now + expires_in - 60
        log.info(f"获取 token 成功，有效期 {expires_in} 秒")
        return self.__class__._token

    def refresh(self) -> str:
        return self.get_token(force_refresh=True)

    def is_valid(self) -> bool:
        return self._token is not None and time.time() < self._expires_at


def get_token() -> str:
    return WeComTokenManager().get_token()
