#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import pytest
import requests
from config.token_manager import get_token
token = get_token()

# 1.创建部门
@pytest.mark.smoke
def test_creat_department():
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/create"
    params = {
        "access_token": token
    }
    body = {
        "name": "广州研发中心",
        "parentid": 1,
        "id": 111111
    }
    response = requests.post(url=url, params=params, json=body)

    assert response.status_code == 200, f"请求失败，状态码：{response.status_code}"
    assert response.json()["errcode"] == 0  , f"❌ 创建部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"


# 2.更新部门
@pytest.mark.smoke
def test_update_department():
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/update"
    params = {
        "access_token": token
    }
    body = {
        "id": 111111,
        "name": "地球研发中心"
    }
    response = requests.post(url=url, params=params, json=body)

    assert response.status_code == 200, f"实际响应状态码：{response.status_code}"
    assert response.json()["errcode"] == 0  , f"❌ 更新部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"


# 3.删除部门
@pytest.mark.smoke
def test_delete_department():
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/delete"
    params = {
        "access_token": token,
        "id": 111111
    }
    response = requests.get(url=url, params=params)

    assert response.status_code == 200, f"实际响应状态码：{response.status_code}"
    assert response.json()["errcode"] == 0  , f"❌ 删除部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"


# 4.获取部门列表
@pytest.mark.smoke
def test_list_departments():
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/list"
    params = {
        "access_token": token
    }
    response = requests.get(url=url, params=params)

    assert response.status_code == 200
    # assert response.json()["errcode"] == 0  , f"❌ 查询部门列表失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"