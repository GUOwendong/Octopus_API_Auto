#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author：guowendong
@Desc: 订单管理 Service
=================
职责：封装订单的上传，匹配表头，查询渠道商品，关联生成订单，查询订单，修改订单金额 6 个接口调用。

接口说明：
- 1. 导入Excel     POST   /v1/wxorderorder/file                        form-data: channelId + orderFile
- 2. 匹配表头      POST   /v1/excelorder/excelheader/excel/{excelDataId}   json: keyMapping...
- 3. 查询渠道商品   POST   /v1/wxorderchannelgoods/getGoodsAndWareInfoByIdList  json: channelGoodsIdList
- 4. 关联生成订单   POST   /v1/excelorder/channelGoodsBase/excelData/{excelDataId}  json: [{"channelGoodsName","channelGoodsId"}]
- 5. 查询订单      GET    /v1/wxorderorder?consignee=xxx&mobile=xxx
- 6. 修改订单金额   PUT    /v1/wxorderorder/money                        json: [{"id","moneyPaid","shippingPrice"}]
"""
from typing import Any, Dict, List

from common.file_utils import FileUtil
from common.log_utils import log
from integrations.octopus.api_client import OctopusClient


class OrderService:
    """订单管理业务层"""

    def __init__(self, client: OctopusClient):
        """client 由 conftest 的 api_client fixture 自动注入"""
        self.client = client

    # ====================== 1. 导入 Excel 文件 ======================
    def import_excel(self, channel_id: str, file_name: str) -> Dict[str, Any]:
        """
        上传订单 Excel 文件
        :param channel_id: 渠道 ID
        :param file_name: 本地 Excel 文件名称
        :return: {"code":"ok", "data": {"excelDataId":"11301", "progressStep":1}}
        """
        log.info(f"📤导入 Excel: {file_name}, 渠道: {channel_id}")
        # 用户传入文件名，转为本地文件的绝对路径
        file_path = FileUtil.resolve_path(file_name)
        with open(file_path, "rb") as f:
            resp = self.client.post(
                # 请求路径
                "/v1/wxorderorder/file",
                # from-data独有的传参形式
                data={"channelId": channel_id},
                # 文件名称，读成byte的文件，固定格式让服务器知道这是excel形式的文件
                files={
                    "orderFile": (
                        file_path.name,
                        f,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
            )
        log.info(f"✅导入 Excel 响应: {resp.status_code}")
        return resp.json()

    # ====================== 2. 匹配表头 ======================
    def match_headers(self, excel_data_id: str, key_mapping: Dict[str, int] = None) -> Dict[str, Any]:
        """
        将 Excel 表头列与系统字段做映射
        :param excel_data_id: 步骤1返回的 excelDataId
        :param key_mapping: 列名→列索引映射, 默认: {consignee:0, mobile:1, PCDaddress:2, channelGoodsName:3, num:4}
        :return: {"code":"ok", "data": {"excelssid":"11301"}}
        """
        if key_mapping is None:
            key_mapping = {
                "consignee": 0,  # 收货人
                "mobile": 1,  # 手机号
                "PCDaddress": 2,  # 省市区地址
                "channelGoodsName": 3,  # 渠道商品名
                "num": 4,  # 数量
            }

        body = {
            "keyMapping": key_mapping,
            "excelTitleIndex": 0,
            "newColumnMapping": [],
            "sheetName": "0",
        }

        log.info(f"🎯匹配表头: excelDataId={excel_data_id}")
        resp = self.client.post(f"/v1/excelorder/excelheader/excel/{excel_data_id}", json=body)
        log.info(f"✅匹配表头响应: {resp.status_code}")
        return resp.json()

    # ====================== 3. 查询渠道商品列表 ======================
    def get_channel_goods(self, channel_goods_id_list: List[int]) -> Dict[str, Any]:
        """
        查询渠道商品信息（为关联做准备）
        :param channel_goods_id_list: 渠道商品 ID 列表, 如 [103060]
        :return: 商品信息
        """
        log.info(f"🔍查询渠道商品: {channel_goods_id_list}")
        resp = self.client.post(
            "/v1/wxorderchannelgoods/getGoodsAndWareInfoByIdList",
            json={"channelGoodsIdList": channel_goods_id_list},
        )
        log.info(f"✅查询渠道商品响应: {resp.status_code}")
        return resp.json()

    # ====================== 4. 关联产品生成订单 ======================
    def bind_goods(self, excel_data_id: str, goods_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        将渠道商品与导入的数据关联，触发系统生成订单
        :param excel_data_id: 步骤1返回的 excelDataId
        :param goods_list: 商品列表, 如 [{"channelGoodsName":"挖掘机","channelGoodsId":103060}]
        :return: {"code":"ok", "error":"文件已转入系统后台处理"}
        """
        log.info(f"🔗关联商品生成订单: excelDataId={excel_data_id}")
        resp = self.client.post(
            f"/v1/excelorder/channelGoodsBase/excelData/{excel_data_id}",
            json=goods_list,
        )
        log.info(f"✅关联商品响应: {resp.status_code}")
        return resp.json()

    # ====================== 5. 查询订单 ======================
    def search(self, consignee: str, mobile: str) -> Dict[str, Any]:
        """
        按收货人和手机号查询订单
        :param consignee: 收货人姓名
        :param mobile: 手机号
        :return: {"code":"ok", "data": {"rows": [...]}}
        """
        log.info(f"🔍查询订单: {consignee} / {mobile}")
        resp = self.client.get("/v1/wxorderorder", params={"consignee": consignee, "mobile": mobile})
        log.info(f"✅查询订单响应: {resp.status_code}")
        return resp.json()

    # ====================== 6. 修改订单金额 ======================
    def modify_amount(self, order_id: str, money_paid: str, shipping_price: str) -> Dict[str, Any]:
        """
        修改订单实付金额和运费
        :param order_id: 订单 ID
        :param money_paid: 实付金额
        :param shipping_price: 运费
        :return: {"code":"ok", "error":"共更新1条记录，全部成功"}
        """
        log.info(f"✏️修改订单金额: id={order_id}, 实付={money_paid}, 运费={shipping_price}")
        resp = self.client.put(
            "/v1/wxorderorder/money",
            json=[{"id": order_id, "moneyPaid": money_paid, "shippingPrice": shipping_price}],
        )
        log.info(f"✅修改金额响应: {resp.status_code}")
        return resp.json()
