#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc：商品管理 Service
=================
职责：封装商品的新增、查询、上架、下架、删除接口调用。

接口速查：
  新增商品  POST   /v1/goodsbase                              body: JSON
  查询商品  GET    /v1/goodsbase?goodsName=xxx&saleStatus=1
  下架商品  PUT    /v1/wxordergoodsbasesku/updownstatus/0/sku/{skuId}
  上架商品  PUT    /v1/wxordergoodsbasesku/updownstatus/1/sku/{skuId}
  删除商品  GET    /v1/goodsbase/deleteGoods?idList=xxx       返回: Excel 文件
"""
from typing import Any, Dict

import requests

from common.log_utils import log


class ProductService:
    """商品管理业务层"""

    def __init__(self, client):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ======================== 新增商品 ========================
    def create(self, goods_name: str, **kwargs) -> Dict[str, Any]:
        """
        新增商品
        :param goods_name: 商品名称
        :param kwargs: 可覆盖 goodsCode, wareList, goodsImage, goodsBaseSkuList 等
        :return: {'code':'ok', 'data': {'firstSkuId': 'xxx'}}
        """
        body = {
            "goodsName": goods_name,
            "goodsCode": "XG94930913",
            "wareList": [{"wareSsid": "2276", "shippingId": "4302630", "wareShippingId": "4302630"}],
            "goodsImage": "https://8zyun-base-api.oss-cn-beijing.aliyuncs.com/8zyun-wxorder-com/2026/06/21/uploadfile/goodsbase/ASYre6/豆包.png",
            "goodsBaseSkuList": [
                {
                    "skuName": "新疆",
                    "skuCode": "skuBW7CTVEC9669",
                    "basicPrice": "32",
                    "suggestPrice": "45",
                    "inventory": "10000",
                    "shippingId": "4302630",
                    "wareShippingId": "4302630",
                }
            ],
        }
        body.update(kwargs)

        log.info(f"🆕新增商品: {goods_name}")
        resp = self.client.post("/v1/goodsbase", json=body)
        return resp.json()

    # ======================== 查询商品 ========================
    def search(self, goods_name: str, sale_status: str = "1") -> Dict[str, Any]:
        """
        按名称搜索商品
        :param goods_name: 商品名称
        :param sale_status: 销售状态（1=在售）
        :return: {'code':'ok', 'data': {'rows': [...]}}
        """
        log.info(f"🔍查询商品: {goods_name}")
        resp = self.client.get("/v1/goodsbase", params={"goodsName": goods_name, "saleStatus": sale_status})
        return resp.json()

    # ======================== 下架商品 ========================
    def delist(self, sku_id: str) -> Dict[str, Any]:
        """
        下架商品（updownstatus=0）
        :param sku_id: SKU ID
        """
        log.info(f"⬇️下架商品 SKU: {sku_id}")
        resp = self.client.put(
            f"/v1/wxordergoodsbasesku/updownstatus/0/sku/{sku_id}",
            json={"sendMessageStatus": "0", "message": ""},
        )
        return resp.json()

    # ======================== 上架商品 ========================
    def relist(self, sku_id: str) -> Dict[str, Any]:
        """
        上架商品（updownstatus=1）
        :param sku_id: SKU ID
        """
        log.info(f"⬆️上架商品 SKU: {sku_id}")
        resp = self.client.put(
            f"/v1/wxordergoodsbasesku/updownstatus/1/sku/{sku_id}",
            json={"sendMessageStatus": "0", "message": ""},
        )
        return resp.json()

    # ======================== 删除商品 ========================
    def delete(self, goods_id: int) -> requests.Response:
        """
        删除商品（返回 Excel 文件，不是 JSON）
        :param goods_id: 商品 ID
        :return: requests.Response（调用方自行解析 Excel）
        """
        log.info(f"🗑️删除商品 ID: {goods_id}")
        resp = self.client.get("/v1/goodsbase/deleteGoods", params={"idList": goods_id})
        return resp  # 不调 .json()，因为是 Excel 流
