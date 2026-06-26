#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 渠道管理 Service
=================
职责：封装渠道的新增、查询、删除接口调用。

接口说明：
- 新增渠道  POST   /v1/wxorderchannel             body:  JSON
- 查询渠道  GET    /v1/wxorderchannel?name=xxx
- 删除渠道  DELETE   /v1/wxorderchannel/{id}
"""
import os
from typing import Any, Dict

from common.log_utils import log
from integrations.octopus.api_client import OctopusClient


class ChannelService:
    """渠道管理业务层"""

    def __init__(self, client: OctopusClient):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ========================= 新增渠道 ========================
    def add(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        新增渠道
        :param name: 渠道名称（必填）
        :param kwargs: 其他可选字段，如 manager，managerNickname, wxGroupNickname 等
        :return: 服务器返回的 JSON 字典
        """
        # 构建请求体，可从环境变量覆盖（避免硬编码失效）
        body = {
            "name": name,
            "manager": os.getenv("CHANNEL_MANAGER", "S:1688851806310976_1688857021633656"),
            "managerNickname": os.getenv("CHANNEL_MANAGER_NICKNAME", "王田甜"),
            "wxGroupNickname": os.getenv("CHANNEL_WX_GROUP_NICKNAME", "钱老师-大课"),
            "wxReceiveNickname": os.getenv("CHANNEL_WX_RECEIVE_NICKNAME", "修然"),
        }
        # kwargs 传入的字段会合并到 body 中
        body.update(kwargs)

        log.info(f"🆕新增渠道：{name}")
        resp = self.client.post("/v1/wxorderchannel", json=body)
        log.info(f"✅ 新增渠道响应：{resp.status_code}")
        return resp.json()

    # ========================= 查询渠道 =========================
    def search(self, name: str) -> Dict[str, Any]:
        """
        按名称搜索渠道
        :param name: 渠道名称（支持模糊搜索）
        :return: 服务器返回 JSON 字典
        """
        log.info(f"🔍搜索渠道：{name}")
        resp = self.client.get("/v1/wxorderchannel", params={"name": name})
        log.info(f"✅搜索渠道响应：{resp.status_code}")
        return resp.json()

    # ========================== 删除渠道 ========================
    def delete_channel(self, channel_id: int) -> Dict[str, Any]:
        """
        删除指定渠道
        :param channel_id: 渠道 ID
        :return: 服务器返回的 JSON 字典
        """
        log.info(f"🗑️删除渠道 ID：{channel_id}")
        resp = self.client.delete(f"/v1/wxorderchannel/{channel_id}")
        log.info(f"✅删除渠道响应：{resp.status_code}")
        return resp.json()
