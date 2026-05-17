#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 企业微信 API 客户端，继承 base_api_client 基类，仅保留企业微信业务逻辑
"""

from typing import Any, Dict, Optional

from base.base_api_client import BaseApiClient, BaseApiClientError
from common.log_utils import log
from config.global_config import TIMEOUT


class ApiClient(BaseApiClient):
    """企业微信专用 HTTP 客户端（自动带 token + 校验 errcode）"""

    def __init__(self, base_url: str, timeout: int = None):
        # 直接继承父类：session、headers、timeout、url 拼接全部父类处理
        super().__init__(base_url=base_url, timeout=timeout or TIMEOUT)
        self.access_token: Optional[str] = None
        self.log = log.bind(module="wecom_api_client")

    def set_access_token(self, token: str):
        """设置 access_token，所有请求自动携带"""
        self.access_token = token

    # ======================== 父类钩子：自动注入 token ============================
    def _prepare_request_kwargs(self, method: str, **kwargs) -> Dict[str, Any]:
        kwargs = super()._prepare_request_kwargs(method, **kwargs)

        # 企业微信：access_token 放在 URL 参数中
        if self.access_token:
            params = kwargs.get("params", {})
            params["access_token"] = self.access_token
            kwargs["params"] = params
        else:
            self.log.warning("access_token is None, request may fail")
        return kwargs

    # ============================== 企业微信响应校验 ===============================
    def _check_wecom_response(self, data: dict):
        """校验企业微信返回 errcode != 0 则抛异常"""
        if not isinstance(data, dict):
            raise BaseApiClientError("非法响应格式，非 JSON 对象")

        errcode = data.get("errcode", 0)
        errmsg = data.get("errmsg", "")
        if errcode != 0:
            raise BaseApiClientError(f"企业微信接口错误 {errcode}: {errmsg}", response=None)  # 若需要可传入 resp

    # ======================= 业务层常用方法（给 service 调用） ========================
    def get_json(self, path: str, **kwargs) -> Dict[str, Any]:
        resp = self.get(path, **kwargs)
        data = resp.json()
        self._check_wecom_response(data)
        return data

    def post_json(self, path: str, **kwargs) -> Dict[str, Any]:
        resp = self.post(path, **kwargs)
        data = resp.json()
        self._check_wecom_response(data)
        return data
