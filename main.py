#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import os
import sys
import subprocess

def run_tests(env: str = "test"):
    """运行测试用例"""
    os.environ["TEST_ENV"] = env
    # 执行 pytest
    pytest_cmd = ["pytest", f"--env={env}"]
    subprocess.run(pytest_cmd, check=True)
    # 生成 allure 报告
    allure_cmd = ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"]
    subprocess.run(allure_cmd, check=True)

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "test"
    run_tests(env)