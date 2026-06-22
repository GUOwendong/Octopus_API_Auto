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

# OctopusAuth：你的认证类，负责从 .env 读取 token
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
    1. 创建 OctopusAuth 实例，从 .env 读 token
    2. 创建 OctopusClient 实例，设置 base_url
    3. 把 token 注入客户端
    4. yield client → 测试用例拿到 client 开始执行
    5. 测试全部结束后，client.close() 关闭 HTTP 连接
    """
    # 1. 创建认证对象，自动从环境变量 OCTOPUS_TOKEN 读取 token
    auth = OctopusAuth()

    # 2. 从环境变量 OCTOPUS_BASE_URL 读取 API 地址，没有则用默认值
    base_url = os.getenv("OCTOPUS_BASE_URL", "http://api.wxorder.taover.com")

    # 3. 创建 HTTP 客户端
    client = OctopusClient(base_url=base_url)

    # 4. 把 token 注入客户端（设置到 Authorization 请求头）
    token = auth.get_token()
    client.set_token(token)

    # 5. 日志记录
    log.info("🚀 Octopus ApiClient 已初始化")

    # yield：把 client 交给测试用例使用
    yield client

    # 所有测试用例执行完毕后，关闭客户端（释放 HTTP 连接）
    client.close()
    log.info("🔚 Octopus ApiClient 已关闭")
