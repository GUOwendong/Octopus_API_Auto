#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 能直接跑通的宠物诊所接口测试用例
"""

import os
import json
import requests

# 1.断言状态码
def test_find_pet_owner():
    url = "https://spring-petclinic-rest.k8s.hogwarts.ceshiren.com/petclinic/api/owners"
    params = {}
    response = requests.get(url, params=params)
    assert response.status_code == 200

    result = response.json()
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    response_path = os.path.join(base_dir, 'data', 'response_json')
    with open(response_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

# 2.断言“nanjing”
def test_assert_nanjing():
    url = "https://spring-petclinic-rest.k8s.hogwarts.ceshiren.com/petclinic/api/owners"
    params = {}
    response = requests.get(url, params=params)
    assert response.status_code == 200

    result = response.json()
    assert any(item.get("city") != "nanjing" for item in result)

# 3.断言 name = "Black" 状态结果判断
def test_Black_status_code():
    url = "https://spring-petclinic-rest.k8s.hogwarts.ceshiren.com/petclinic/api/owners"
    params = {
        "lastName": "Black",
    }
    response = requests.get(url, params=params)
    assert response.status_code == 200

# 4.不存在的宠物主人，断言相应状态码
def test_not_exist_owner():
    url = "https://spring-petclinic-rest.k8s.hogwarts.ceshiren.com/petclinic/api/owners"
    params = {
        "lastName": "guowendong",
    }
    response = requests.get(url, params=params)
    assert response.status_code == 404