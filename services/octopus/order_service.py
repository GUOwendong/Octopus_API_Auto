#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 订单管理 Service
==================
职责：封装订单的导入、匹配表头、选择渠道产品、关联产品、订单查询、修改订单金额接口调用。

接口说明：
- 订单导入      POST    /v1/wxorderorder/file       body: from-data
- 匹配表头      POST    /v1/excelorder/excelheader/excel/{excel_id}
- 选择渠道产品   POST    /v1/wxorderchannelgoods/getGoodsAndWareInfoByIdList      body: JSON
- 关联产品      POST    /v1/excelorder/channelGoodsBase/excelData/{excel_id}     body: JSON
- 订单查询      GET     /v1/wxorderorder
- 修改订单金额   PUT    /v1/wxorderorder/money      body: JSON
"""
from typing import Any, Dict

from common.log_utils import log
from integrations.octopus.api_client import OctopusClient


class OrderService:
    """订单管理业务层"""

    def __init__(self, client):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ===================== 导入订单 ====================
    def upload_order(self, order):
        pass

    # ===================== 匹配表头 ====================
    def match_header(self, order):
        pass

    # =================== 选择渠道产品 ===================
    def choose_channel_product(self, order):
        pass

    # ===================== 关联产品 =====================
    def associate_product(self, order):
        pass

    # ===================== 订单查询 =====================
    def search_order(self, order):
        pass

    # ==================== 修改订单金额 ===================
    def modify_order_amount(self, order):
        pass
