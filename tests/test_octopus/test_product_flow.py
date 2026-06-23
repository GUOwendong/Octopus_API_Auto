#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品管理测试用例 — framework 风格
===================================
接口调用 → ProductService（services 层）
HTTP / 认证 → api_client fixture（conftest 自动注入）

对照你原来的写法：
  旧: requests.post(url, headers=HEADERS, json={...})
  新: service.create(goods_name="西瓜")
"""

import io

import pandas as pd

from services.octopus.product_service import ProductService


class TestProduct:
    """商品管理全流程：新增 → 查询 → 下架 → 上架 → 删除"""

    def test_product_flow(self, api_client):
        """
        流程说明：
        1. 新增商品 → 拿到 SKU_ID
        2. 查询商品 → 验证新增成功，拿到商品 ID
        3. 下架商品
        4. 上架商品
        5. 删除商品（返回 Excel，解析验证）
        """
        service = ProductService(api_client)
        goods_name = "西瓜"

        # ===== 1. 新增商品 =====
        create_res = service.create(goods_name=goods_name)
        assert create_res["code"] == "ok", f"新增失败: {create_res.get('error', create_res)}"
        sku_id = create_res["data"]["firstSkuId"]
        print(f"✅ 商品创建成功, SKU_ID={sku_id}")

        # ===== 2. 查询商品（验证新增）=====
        query_res = service.search(goods_name=goods_name)
        assert query_res["code"] == "ok", f"查询失败: {query_res.get('error', query_res)}"
        rows = query_res["data"]["rows"]
        assert len(rows) > 0, "查询结果为空"
        assert rows[0]["goodsName"] == goods_name, f"商品名称不匹配: {rows[0]['goodsName']}"
        goods_id = rows[0]["id"]
        print(f"✅ 查询成功, goods_id={goods_id}")

        # ===== 3. 下架商品 =====
        delist_res = service.delist(sku_id)
        assert delist_res["code"] == "ok", f"下架失败: {delist_res.get('error', delist_res)}"
        print("✅ 下架成功")

        # ===== 4. 上架商品 =====
        relist_res = service.relist(sku_id)
        assert relist_res["code"] == "ok", f"上架失败: {relist_res.get('error', relist_res)}"
        print("✅ 上架成功")

        # ===== 5. 删除商品（响应是 Excel 文件）=====
        del_resp = service.delete(goods_id)
        assert del_resp.status_code == 200, f"删除 HTTP 异常: {del_resp.status_code}"
        # 解析 Excel 验证删除成功
        df = pd.read_excel(io.BytesIO(del_resp.content))
        data = df.to_dict(orient="records")
        assert len(data) > 0, "删除结果 Excel 为空"
        assert data[0]["处理结果"] == "删除成功", f"删除失败: {data[0]}"
        print("✅ 商品全流程测试通过")
