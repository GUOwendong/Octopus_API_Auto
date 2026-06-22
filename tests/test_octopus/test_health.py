#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连通性测试 (Health Check)
==========================
接入新系统后，第一个测试用例：验证 token 是否有效，网络是否通畅。
通过就跑绿，不通就排查 .env 配置或 token 是否过期。
"""


def test_login_check(api_client):
    """
    验证 token 和网络连通性
    ========================
    api_client 参数由 conftest.py 中的 fixture 自动注入，无需手动创建。

    执行逻辑：
    1. 用 api_client 向 /login 发 GET 请求
    2. 打印 HTTP 状态码（200 表示请求成功到达服务器）
    3. 打印响应内容（查看服务器返回了什么）

    如果返回 200，说明：网络通 + token 能被服务器接受
    如果返回 401/403，说明 token 过期或无效，需要重新从浏览器抓取
    如果超时/连接失败，检查 BASE_URL 是否正确
    """
    # api_client.get("/login") → 相当于发送 GET http://api.wxorder.taover.com/login
    # Authorization: Bearer xxx 请求头已经由 client 自动带上了
    resp = api_client.get("/login")

    # 打印状态码（如 200、401、500）
    print(resp.status_code)

    # 打印服务器返回的内容
    print(resp.text)
