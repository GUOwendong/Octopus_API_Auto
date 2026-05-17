#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 轻量基础 HTTP 客户端基类 | 薄封装、高扩展、无业务侵入
"""

# Python 类型注解标准库，Optional：可以是 None或指定类型，Dict:字典，Any:任意
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

# requests 所有网络异常的基类（连接失败，超时，DNS错误，500/404等）
from requests.exceptions import RequestException


class BaseApiClientError(Exception):
    """基础请求异常，保留原始 response"""

    def __init__(self, message: str, response: Optional[requests.Response] = None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response else None


class BaseApiClient:
    """
    高扩展 HTTP 客户端基类
    职责：会话管理、URL 拼接、请求分发、异常包装
    不包含：日志、重试、JSON 解析、业务校验、自动抛错
    所有能力均可通过钩子子类扩展
    """

    def __init__(self, base_url: str = None, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        self.base_url = (base_url or "").rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        # 默认基础头
        default_headers = {"User-Agent": "BaseApiClient/1.0", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)
        self.session.headers.update(default_headers)

    # ------------------------- 扩展钩子（子类可重写） -------------------------
    # URL拼接
    def _build_url(self, path: str) -> str:
        if not path:
            return self.base_url
        if not self.base_url:
            return path.lstrip("/")
        return urljoin(self.base_url + "/", path.lstrip("/"))

    # 准备请求参数
    def _prepare_request_kwargs(self, method: str, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault("timeout", self.timeout)
        return kwargs

    # 响应处理
    def _handle_response(self, response: requests.Response) -> requests.Response:
        return response

    # ------------------------------ 核心请求 --------------------------------
    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        kwargs = self._prepare_request_kwargs(method, **kwargs)

        try:
            resp = self.session.request(method, url, **kwargs)
            return self._handle_response(resp)
        except RequestException as e:
            raise BaseApiClientError(str(e), getattr(e, "response", None)) from e

    # ----------------------------- HTTP 方法 --------------------------------
    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._request("PATCH", path, **kwargs)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        return self._request(method.upper(), path, **kwargs)

    # ------------------------------- 会话管理 ---------------------------------
    def set_headers(self, headers: Dict[str, str]) -> None:
        self.session.headers.update(headers)

    def set_header(self, key: str, value: str) -> None:
        """单独设置一个请求头（方便动态 token 等场景）"""
        self.session.headers[key] = value

    def close(self) -> None:
        """关闭会话，幂等（可多次调用）"""
        if hasattr(self, "session") and self.session is not None:
            self.session.close()
            self.session = None  # 避免重复关闭

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
