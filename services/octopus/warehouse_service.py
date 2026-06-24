#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author：guowendong
@Desc: 仓库管理 Service
=================
职责：封装仓库的新增、查询、删除接口调用。

接口说明：
- 新增仓库  POST  /v1/wxorderware          body: JSON
- 查询仓库  GET   /v1/wxorderware?name=xxx
- 删除仓库  DELETE /v1/wxorderware/{id}
"""
from typing import Any, Dict

from common.log_utils import log
from integrations.octopus.api_client import OctopusClient


class WarehouseService:
    """仓库管理业务层"""

    def __init__(self, client: OctopusClient):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ======================== 新增仓库 ========================
    def add(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        新增仓库
        :param name: 仓库名称（必填）
        :param kwargs: 其他可选字段，如 type, cutTime, wxReceiveId 等
        :return: 服务器返回的 JSON 字典
        """
        # 构建请求体（不含群信息，必须通过 kwargs 传入）
        # 至少需要传：wxGroupNickname, wxReceiveId, wxGroupSsid, wxReceiveNickname
        body = {
            "name": name,
            "type": "0",
            "cutTime": "21:54",
            "pushEveryFewDays": 1,
            "pushStartDate": "2026-06-20",
            "exportTemplateId": "7100496",
            "pushExcelType": "0",
        }
        # kwargs 传入的字段会合并到 body 中（如群信息等）
        body.update(kwargs)

        log.info(f"🆕新增仓库: {name}")
        resp = self.client.post("/v1/wxorderware", json=body)
        log.info(f"✅新增仓库响应: {resp.status_code}")
        return resp.json()

    # ======================== 查询仓库 ========================
    def search(self, name: str) -> Dict[str, Any]:
        """
        按名称搜索仓库
        :param name: 仓库名称（支持模糊搜索）
        :return: 服务器返回的 JSON 字典
        """
        log.info(f"🔍搜索仓库: {name}")
        resp = self.client.get("/v1/wxorderware", params={"name": name})
        log.info(f"✅搜索仓库响应: {resp.status_code}")
        return resp.json()

    # ======================== 查询所有仓库 ========================
    def list_all(self) -> Dict[str, Any]:
        """
        查询所有仓库（不带 name 参数 = 全量查询）
        :return: 服务器返回的 JSON 字典
        """
        log.info("🔍查询所有仓库")
        resp = self.client.get("/v1/wxorderware")
        log.info(f"✅查询所有仓库响应: {resp.status_code}")
        return resp.json()

    # ======================== 删除仓库 ========================
    def delete(self, warehouse_id: int) -> Dict[str, Any]:
        """
        删除指定仓库
        :param warehouse_id: 仓库 ID
        :return: 服务器返回的 JSON 字典
        """
        log.info(f"🗑️删除仓库 ID: {warehouse_id}")
        resp = self.client.delete(f"/v1/wxorderware/{warehouse_id}")
        log.info(f"✅删除仓库响应: {resp.status_code}")
        return resp.json()
