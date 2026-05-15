#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
# 全局夹具 + 用例失败钩子
import pytest
from common.api_client import ApiClient
from common.log_utils import logger
from config import SCREENSHOT_DIR
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="session")
def login_client():
    client = ApiClient()
    logger.info("开始执行全局登录")

    login_data = {
        "username": "test_user",
        "password": "123456"
    }
    resp = client.post("/api/login", json=login_data)
    assert resp.status_code == 200
    json_data = resp.json()
    assert json_data.get("code") == 0

    token = json_data["data"]["token"]
    client.session.headers.update({"Authorization": f"Bearer {token}"})
    logger.info("登录成功，已全局注入Token")

    yield client
    logger.info("测试会话结束")

@pytest.fixture(autouse=True)
def auto_save_screenshot(request):
    yield
    if request.node.rep_call.failed:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        logger.error(f"用例失败：{request.node.name}，可在此追加截图逻辑")