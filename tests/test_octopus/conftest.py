#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试夹具 (Test Fixtures)
=========================
conftest.py 是 pytest 的约定文件名，pytest 会自动发现并加载。
在这里定义 session 级别的 api_client fixture，整个测试会话只创建一次客户端。
测试用例函数只需在参数中写 api_client 即可自动注入。

使用方式（在测试用例中）：
    def test_xxx(api_client):
        resp = api_client.get("/api/xxx")
        assert resp.status_code == 200
"""

# os：读取环境变量
import os

# pytest：pytest 测试框架，提供 fixture 装饰器
import pytest

# log：框架的日志工具
from common.log_utils import log

# OctopusClient：你的 HTTP 客户端，负责发请求
from integrations.octopus.api_client import OctopusClient

# OctopusAuth：你的认证类，负责通过账号密码登录获取 token
from integrations.octopus.auth import OctopusAuth


@pytest.fixture(scope="session")
def api_client():
    """
    session 级别的 api_client fixture
    ================================
    scope="session" 意思是整个 pytest 运行期间只创建一次这个客户端，
    所有测试用例共享它，不用每次都重新认证。
    使用 yield 确保测试结束后自动关闭客户端。

    执行流程：
    1. 创建 OctopusAuth 实例，从 .env 读用户名密码
    2. 调用 get_token() 自动登录，获取 JWT Token
    3. 创建 OctopusClient 实例，注入 token
    4. yield client → 测试用例拿到 client 执行
    5. 测试结束后关闭客户端
    """
    # 1. 创建认证对象，从 .env 读 OCTOPUS_USERNAME / OCTOPUS_PASSWORD
    auth = OctopusAuth()

    # 2. 获取 token（首次调用会自动登录）
    token = auth.get_token()

    # 3. 从环境变量读 API 地址
    base_url = os.getenv("OCTOPUS_BASE_URL", "http://api.wxorder.taover.com")

    # 4. 创建 HTTP 客户端，注入 token
    client = OctopusClient(base_url=base_url)
    client.set_token(token)

    log.info("✅ Octopus ApiClient 已初始化")

    # yield：把 client 交给测试用例使用
    yield client

    # 所有测试用例执行完毕后，关闭客户端
    client.close()
    log.info("Octopus ApiClient 已关闭")
