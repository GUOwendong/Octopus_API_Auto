#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import pytest
from common import ApiClient, read_yaml, log_utils

case_data = read_yaml("demo_case.yaml")

@pytest.mark.regress
@pytest.mark.parametrize("case", case_data)
def test_login_param(case):
    logger.info(f"执行用例：{case['case_name']}")
    client = ApiClient()
    res = client.post("/api/login", json=case)
    assert res.status_code == 200