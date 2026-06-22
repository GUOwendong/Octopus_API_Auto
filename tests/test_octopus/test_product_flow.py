#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import io

import pandas as pd
import requests

from common.log_utils import log

BASE_URL = "http://api.wxorder.taover.com/v1"
HEADERS = {
    "Authorization": "Bearer==eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiIsImF1ZCI6IjA5OGY2YmNkNDYyMWQzNzNjYWRlNGU4MzI2MjdiNGY2IiwidGVuYW50IjoiMjM3IiwidXNlcm5hbWUiOiIxNzYxMTIxOTgwMyIsInVzZXJpZCI6IjMzMiIsInBhc3N3b3JkIjoiYmE2NzY2NThlOWMxN2M3ZmU4ZjcxNTliNjZiZTVkZDAiLCJzdGF0dXMiOjEsImV4cCI6MTc4MjMyMDM5OSwibmJmIjoxNzgyMDk1ODk4fQ.iFt3Sr5uf5N7DI9ATDJetWddl0iKKUgDOSqTj5ddb8I"
}
ID = None
SKU_ID = None
GOODS_NAME = "西瓜"


class TestProductManager:

    def test_create_product(self):
        global SKU_ID, GOODS_NAME
        log.info(f"🆕开始创建商品：{GOODS_NAME}...")

        response = requests.post(
            url=f"{BASE_URL}/goodsbase",
            headers=HEADERS,
            json={
                "goodsName": GOODS_NAME,
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
            },
        )

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["code"] == "ok", f"业务code异常: {data['code']}"
        assert data["error"] == "创建成功", f"提示信息不符：{data['error']}"

        SKU_ID = data["data"]["firstSkuId"]
        log.info(f"✅ 商品创建成功，🆔：{data['data']['firstSkuId']}，Name：{GOODS_NAME}")

    def test_query_product(self):
        global ID
        log.info("🔍开始搜索商品...")
        response = requests.get(
            url=f"{BASE_URL}/goodsbase", headers=HEADERS, params={"goodsName": GOODS_NAME, "saleStatus": "1"}
        )

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["code"] == "ok", f"业务code异常: {data['code']}"
        assert (
            data["data"]["rows"][0]["goodsName"] == GOODS_NAME
        ), f"查询结果与预期不同，实际商品名称：{data['data']['rows'][0]['goodsName']}"

        ID = data["data"]["rows"][0]["id"]
        log.info(f"🔍搜索出来的是{GOODS_NAME}，🆔：{ID}")

    def test_delisting_product(self):
        log.info("⬇️开始下架商品...")
        response = requests.put(
            url=f"{BASE_URL}/wxordergoodsbasesku/updownstatus/0/sku/{SKU_ID}",
            headers=HEADERS,
            json={"sendMessageStatus": "0", "message": ""},
        )

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["code"] == "ok", f"业务code异常: {data['code']}"
        assert data["error"] == "操作成功", f"提示信息不符：{data['error']}"

        log.info("⬇️商品下架🏅")

    def test_listing_product(self):
        log.info("⬆️开始上架商品...")
        response = requests.put(
            url=f"{BASE_URL}/wxordergoodsbasesku/updownstatus/1/sku/{SKU_ID}",
            headers=HEADERS,
            json={"sendMessageStatus": "0", "message": ""},
        )

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["code"] == "ok", f"业务code异常: {data['code']}"
        assert data["error"] == "操作成功", f"提示信息不符：{data['error']}"

        log.info("⬆️商品上架🏅")

    def test_delete_product(self):
        log.info("🗑️开始删除商品...")
        response = requests.get(url=f"{BASE_URL}/goodsbase/deleteGoods", headers=HEADERS, params={"idList": ID})

        df = pd.read_excel(io.BytesIO(response.content))
        data = df.to_dict(orient="records")
        print(data)

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert len(data) > 0, "删除结果 Excel 为空！"
        assert data[0]["处理结果"] == "删除成功"
        assert int(data[0]["商品ID"]) == int(ID)

        log.info("🗑️商品删除成功🏅")
