#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 订单管理全流程：导入 → 匹配 → 关联 → 查询 → 改金额
"""
import os

from common.generate_orders import generate_order_excel
from services.octopus.order_service import OrderService

# =================== 测试数据 ===================
EXCEL_NAME = "工作簿14.xlsx"
CHANNEL_ID = "9910335"
CHANNEL_GOODS_ID = 103060
CHANNEL_GOODS_NAME = "魔法棒"
CONSIGNEE = "唐三"  # Excel 里的收货人
MOBILE = "13997463411"  # Excel 里的手机号


class TestOrder:

    def test_order_flow(self, api_client):
        """
        流程说明：
        1. 导入 Excel 文件
        2. 匹配表头（Excel 列 → 系统字段）
        3. 查询渠道商品（验证商品存在）
        4. 关联商品，生成订单
        5. 查订单（拿订单ID）
        6. 修改订单金额
        """
        service = OrderService(api_client)

        # ===== 1. 导入 Excel 文件 =====
        import_res = service.import_excel(channel_id=CHANNEL_ID, file_name=EXCEL_NAME)
        assert import_res.get("code") == "ok", f"导入失败: {import_res.get('error', import_res)}"
        excel_data_id = import_res["data"]["excelDataId"]
        print(f"✅ 1. Excel 导入成功, excelDataId={excel_data_id}")

        # ===== 2. 匹配表头（Excel列 → 系统字段映射）=====
        match_res = service.match_headers(excel_data_id)
        assert match_res.get("code") == "ok", f"匹配表头失败: {match_res.get('error', match_res)}"
        print(f"✅ 2. 表头匹配成功")

        # ===== 3. 查询渠道商品（验证商品可用）=====
        goods_res = service.get_channel_goods([CHANNEL_GOODS_ID])
        assert goods_res.get("code") == "ok", f"查询渠道商品失败: {goods_res.get('error', goods_res)}"
        print(f"✅ 3. 渠道商品查询成功")

        # ===== 4. 关联商品，触发系统生成订单 =====
        bind_res = service.bind_goods(
            excel_data_id, [{"channelGoodsName": CHANNEL_GOODS_NAME, "channelGoodsId": CHANNEL_GOODS_ID}]
        )
        # 系统异步处理，返回 "文件已转入系统后台处理"
        assert bind_res.get("code") == "ok", f"关联商品失败: {bind_res.get('error', bind_res)}"
        print(f"✅ 4. 商品关联成功，系统后台生成订单中")

        # ===== 5. 查询订单 =====
        search_res = service.search(consignee=CONSIGNEE, mobile=MOBILE)
        assert search_res.get("code") == "ok", f"查询订单失败: {search_res.get('error', search_res)}"
        rows = (search_res.get("data") or {}).get("rows", [])
        assert len(rows) > 0, "查询订单结果为空"
        order_id = rows[0].get("id")
        assert order_id, f"未能获取订单 ID"
        print(f"✅ 5. 查询到订单, order_id={order_id}")

        # ===== 6. 修改订单金额 =====
        modify_res = service.modify_amount(
            order_id=str(order_id),
            money_paid="99",
            shipping_price="11",
        )
        assert modify_res.get("code") == "ok", f"修改金额失败: {modify_res.get('error', modify_res)}"
        print("✅ 6. 订单金额修改成功")
        print("✅ 订单全流程测试通过")
