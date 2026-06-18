#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信测试模块 conftest：ApiClient / Auth / Service 夹具"""

import os

import pytest

from common.log_utils import log
from integrations.wecom.api_client import ApiClient
from integrations.wecom.wecom_token import get_token
from services.wecom.department_service import DepartmentService


@pytest.fixture(scope="session")
def api_client():
    """企业微信 ApiClient（session 级别，自动注入 token）"""
    base_url = os.getenv("WECOM_BASE_URL", "https://qyapi.weixin.qq.com")
    client = ApiClient(base_url=base_url)
    token = get_token()
    client.set_access_token(token)
    log.info("✅ 企业微信 ApiClient 已初始化，Token 已注入")
    yield client
    client.close()
    log.info("企业微信 ApiClient 已关闭")


@pytest.fixture(scope="session")
def dept_service(api_client):
    """部门服务（自动把带 token 的 client 注入 Service）"""
    return DepartmentService(client=api_client)
