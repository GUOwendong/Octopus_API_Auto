#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import os
import requests
from common.wecom_token import get_token

# 1. 获取 access_token
token = get_token()
print(f"获取到的 access_token: {token[:20]}...")

# 2. 尝试用它调用一个简单的API接口
test_url = "https://qyapi.weixin.qq.com/cgi-bin/department/list"
params = {"access_token": token}
resp = requests.get(test_url, params=params)

print(f"请求状态码: {resp.status_code}")
print(f"API返回内容: {resp.text}")