#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import os

#================================ 项目核心路径 ====================================
#项目根目录（自动获取，永远不用改）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#================================ 全局通用配置 ====================================

#全局超时时间
global_timeout = 10

#截图保存路径
screenshot_path = os.path.join(base_dir, "temp/screenshots")  # noqa

# Allure 原始结果路径(json数据)
allure_result_path = os.path.join(base_dir, "reports/allure-results")  # noqa

# 测试报告路径（html报告）
allure_report_path = os.path.join(base_dir, "reports/allure-reports")   # noqa

# 日志文件夹（用来创建目录）
log_dir = os.path.join(base_dir, "logs")                   # noqa

# 日志文件（给 logger 写入用）
log_path = os.path.join(log_dir, "interface_auto.log")           # noqa