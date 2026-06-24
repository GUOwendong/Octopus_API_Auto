#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 渠道管理全流程：新增 —> 查询 —> 删除
"""
from services.octopus.channel_service import ChannelService


class TestChannel:

    def test_channel_flow(self, api_client):
        service = ChannelService(api_client)
        name = "放羊的东东娃"

        # ============ 1. 新增渠道 ===========
        add_res = service.add(name=name)
        assert add_res.get("code") == "ok", f"新增失败: {add_res.get('error', add_res)}"
        print(f"✅ 渠道创建成功，渠道名称：{name}")

        # ======== 2. 查询渠道（验证新增）========
        query_res = service.search(name=name)
        assert query_res.get("code") == "ok", f"查询失败: {query_res.get('error', query_res)}"
        rows = (query_res.get("data") or {}).get("rows", [])
        assert len(rows) > 0, "查询结果为空"
        assert rows[0].get("name") == name, f"渠道名称不匹配: {rows[0].get('name')}"
        channel_id = rows[0].get("id")
        print(f"✅ 查询成功，channel_id={channel_id}")

        # ============= 3. 删除渠道 ============
        assert channel_id, "未获取到渠道 ID"
        del_resp = service.delete_channel(int(channel_id))
        assert del_resp.get("code") == "ok", f"删除失败: {del_resp.get('error', del_resp)}"
        print(f"✅ 渠道全流程测试通过")
