#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author：guowendong
@Desc: 企业微信部门业务服务层（纯业务层，无任何底层细节）
"""

from typing import Any, Dict

from common.log_utils import log
from integrations.wecom.api_client import ApiClient
from integrations.wecom.wecom_error_code import extract_error_from_response, is_success


class DepartmentService:
    # 🔥 只接收注入好的 client（自带 token、自带地址）
    def __init__(self, client: ApiClient):
        self.client = client

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        # 🔥 这里只发请求，不管 token、不管地址
        if method.upper() == "GET":
            resp = self.client.get_json(path, **kwargs)
        elif method.upper() == "POST":
            resp = self.client.post_json(path, **kwargs)
        else:
            raise ValueError(f"不支持的方法: {method}")

        if not is_success(resp):
            error = extract_error_from_response(resp)
            log.error(f"企业微信 API 错误: {error}")
            raise RuntimeError(f"部门服务调用失败: {error}")
        return resp

    def create(self, name: str, parentid: int = 1, dept_id: int = None) -> Dict:
        path = "/cgi-bin/department/create"
        body = {"name": name, "parentid": parentid}
        if dept_id:
            body["id"] = dept_id
        return self._request("POST", path, json=body)

    def update(self, dept_id: int, name: str = None, parentid: int = None) -> Dict:
        path = "/cgi-bin/department/update"
        body = {"id": dept_id}
        if name:
            body["name"] = name
        if parentid:
            body["parentid"] = parentid
        return self._request("POST", path, json=body)

    def delete(self, dept_id: int) -> Dict:
        path = "/cgi-bin/department/delete"
        return self._request("GET", path, params={"id": dept_id})

    def list(self, parent_id: int = None) -> Dict:
        path = "/cgi-bin/department/list"
        params = {}
        if parent_id:
            params["id"] = parent_id
        return self._request("GET", path, params=params)
