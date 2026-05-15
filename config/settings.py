#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = "test"

API_BASE_URL = {
    "dev": "http://127.0.0.1:8000",
    "test": "https://test-api.xxx.com",
    "prod": "https://api.xxx.com"
}[ENV]

WEB_URL = {
    "dev": "http://localhost:8080",
    "test": "https://test.xxx.com",
    "prod": "https://xxx.com"
}[ENV]

TIMEOUT = 10

REPORT_DIR = os.path.join(ROOT_PATH, "report")
SCREENSHOT_DIR = os.path.join(ROOT_PATH, "screenshots")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)