#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 订单管理 Service
==================
职责：封装订单的导入、匹配表头、商品关联、订单生成、订单查询、修改订单金额接口调用。

接口速查：
  订单导入   POST
  匹配表头   POST
  商品关联   POST
  订单生成   POST
  订单查询   GET
  修改订单金额   PUT
"""
from typing import Any, Dict

import requests

from common.log_utils import log


class OrderService:
    """订单管理业务层"""

    def __init__(self, client):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ===================== 导入订单 ====================
    def load_order(self, order):
        pass

    # ===================== 匹配表头 ====================
    def get_order_batchNo(self, order):
        pass

    # ===================== 订单查询 =====================
    def search_order(self, order):
        pass

    # ==================== 修改订单金额 ===================
    def modify_order_amount(self, order):
        pass
