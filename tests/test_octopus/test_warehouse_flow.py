#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 测试八爪鱼的仓库（供应商）创建，查询，删除全流程业务
"""
import pytest
import requests

from common.log_utils import log


@pytest.mark.run(order=1)
class TestWarehouseManager:
    BASE_URL = "http://api.wxorder.taover.com/v1/wxorderware"
    HEADERS = {
        "Authorization": "Bearer==eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiIsImF1ZCI6IjA5OGY2YmNkNDYyMWQzNzNjYWRlNGU4MzI2MjdiNGY2IiwidGVuYW50IjoiMjM3IiwidXNlcm5hbWUiOiIxNzYxMTIxOTgwMyIsInVzZXJpZCI6IjMzMiIsInBhc3N3b3JkIjoiYmE2NzY2NThlOWMxN2M3ZmU4ZjcxNTliNjZiZTVkZDAiLCJzdGF0dXMiOjEsImV4cCI6MTc4MjMyMDM5OSwibmJmIjoxNzgyMDk1ODk4fQ.iFt3Sr5uf5N7DI9ATDJetWddl0iKKUgDOSqTj5ddb8I"
    }
    ssid = None
    name = "郭文东"

    # 1.创建仓库
    @pytest.mark.run(order=1)
    def test_create_warehouse(self):
        log.info(f"🆕开始创建仓库, name={self.name}")

        response = requests.post(
            url=self.BASE_URL,
            json={
                "name": self.name,
                "type": "0",
                "cutTime": "21:54",
                "pushEveryFewDays": 1,
                "pushStartDate": "2026-06-20",
                "wxGroupNickname": "渠道测试3群",
                "wxReceiveId": "1688857021633656",
                "wxGroupSsid": "R:10799694107455775",
                "exportTemplateId": "7100496",
                "pushExcelType": "0",
                "wxReceiveNickname": "霍格沃兹-助教-三土",
            },
            headers=self.HEADERS,
        )

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["code"] == "ok", f"业务code异常: {data['code']}"
        assert data["error"] == "仓库创建成功", f"提示信息不符：{data['error']}"

        self.__class__.ssid = data["data"]
        log.info(f"✅ 仓库创建成功, ssid={self.__class__.ssid}")

    # 2.查询仓库
    @pytest.mark.run(order=2)
    def test_query_warehouse(self):
        log.info(f"🆕开始查询仓库, name={self.__class__.name}")

        response = requests.get(url=self.BASE_URL, params={"name": self.__class__.name}, headers=self.HEADERS)

        data = response.json()

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["error"] == "查询成功", f"提示信息不符：{data['error']}"

        rows = data["data"]["rows"]
        assert len(rows) > 0, "查询结果为空，未找到匹配的仓库"

        actual_name = rows[0]["name"]
        assert (
            actual_name == self.__class__.name
        ), f"仓库名称不匹配, 期望: '{self.__class__.name}', 实际: '{actual_name}'"
        assert str(rows[0]["ssid"]) == str(
            self.__class__.ssid
        ), f"ssid不一致, 创建: {self.__class__.ssid}, 查询: {rows[0]['ssid']}"

        log.info(f"✅ 查询校验通过, name={actual_name}")

    # 3.删除仓库
    @pytest.mark.run(order=3)
    def test_delete_warehouse(self):
        assert self.__class__.ssid is not None, "❌ ssid为空，请确认create用例是否执行成功"
        log.info(f"开始删除仓库, ssid={self.__class__.ssid}")

        response = requests.delete(url=f"{self.BASE_URL}/{self.__class__.ssid}", headers=self.HEADERS)

        data = response.json()
        print(data)

        # HTTP层断言
        assert response.status_code == 200, f"HTTP状态码异常: {response.status_code}"

        # 业务层断言
        assert data["error"] == "删除成功", f"提示信息不符：{data['error']}"

        log.info(f"✅ 删除成功, ssid={self.__class__.ssid}")
