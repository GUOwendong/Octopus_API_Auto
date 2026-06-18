#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全局配置：路径、环境、API 地址、超时等（与具体企业无关）"""
import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ==================== 项目路径 ====================
# 取当前文件的绝对路径，.parent回退到上一级，回到项目根目录下
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
REPORTS_DIR = BASE_DIR / "reports"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
ALLURE_REPORT_DIR = REPORTS_DIR / "allure-report"

# 自动创建必要目录
for d in [LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ===================== 环境配置 ====================
class Env(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


CURRENT_ENV = Env(os.getenv("TEST_ENV", "test"))

# API 基础地址（按环境区分，通过环境变量覆盖，默认为本地地址）
API_BASE_URL_MAP = {
    Env.DEV: os.getenv("API_BASE_URL_DEV", "http://127.0.0.1:8000"),
    Env.TEST: os.getenv("API_BASE_URL_TEST", "http://127.0.0.1:8000"),
    Env.PROD: os.getenv("API_BASE_URL_PROD", "http://127.0.0.1:8000"),
}
API_BASE_URL = API_BASE_URL_MAP[CURRENT_ENV]
TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
