#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八爪鱼 API 客户端，继承 BaseApiClient，仅保留八爪鱼业务逻辑
"""
from base.base_api_client import BaseApiClient
from config.global_config import TIMEOUT


class OctopusClient(BaseApiClient):
    """八爪鱼专用 HTTP 客户端，继承 BaseApiClient，只需写 set_token() 一个方法"""

    def __init__(self, base_url: str, timeout: int = None):
        # 直接继承父类：session、headers、timeout、URL 拼接全部父类处理
        super().__init__(base_url=base_url, timeout=timeout or TIMEOUT)

    def set_token(self, token: str):
        """设置 Bearer Token 到 Authorization 请求头（格式：Bearer==xxx，注意是双等号）"""
        self.set_header("Authorization", f"{token}")
