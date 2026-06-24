#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 仓库管理全流程：借群释放 → 新增 → 查询 → 删除
"""
import time
import uuid

from services.octopus.warehouse_service import WarehouseService


class TestWarehouse:

    def test_warehouse_flow(self, api_client):
        service = WarehouseService(api_client)

        # ===== 0. 借群（查所有仓库，找一个带群的删掉释放群）=====
        all_res = service.list_all(size=100)  # size=100 避免漏掉后面页的数据
        group_info = {}
        if all_res.get("code") == "ok" and all_res.get("data"):
            rows = all_res["data"].get("rows", [])
            for r in rows:
                gid = r.get("ssid") or r.get("id")
                gsid = r.get("wxGroupSsid")
                if gid and gsid:
                    del_res = service.delete(int(gid))
                    # 必须确认删除业务上也成功了（code=="ok"），否则群没释放
                    if del_res.get("code") == "ok":
                        time.sleep(0.5)  # 等服务器真正释放群资源
                        group_info = {
                            "wxGroupNickname": r.get("wxGroupNickname", ""),
                            "wxReceiveId": r.get("wxReceiveId", ""),
                            "wxGroupSsid": gsid,
                            "wxReceiveNickname": r.get("wxReceiveNickname", ""),
                        }
                        break
        assert group_info, "没有找到可用群信息，所有仓库的群都删除失败"

        # ===== 1. 新增仓库 =====
        warehouse_name = f"测试_{uuid.uuid4().hex[:4]}"
        add_res = service.add(name=warehouse_name, **group_info)
        assert add_res.get("code") == "ok", f"新增失败: {add_res.get('error', add_res)}"

        wid = add_res.get("data")  # 直接是数字 ID
        if isinstance(wid, dict):
            wid = wid.get("id") or wid.get("ssid")

        # ===== 2. 查询仓库（验证新增成功）=====
        sr = service.search(name=warehouse_name)
        assert sr.get("code") == "ok", f"查询失败: {sr.get('error', sr)}"

        if not wid:
            rows = (sr.get("data") or {}).get("rows") or []
            if rows:
                wid = rows[0].get("ssid") or rows[0].get("id")

        # ===== 3. 删除仓库（清理）=====
        assert wid, "未能获取仓库 ID"
        dr = service.delete(int(wid))
        assert dr.get("code") == "ok", f"删除失败: {dr.get('error', dr)}"
        print("✅ 仓库全流程测试通过")
