#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八爪鱼系统 (Octopus) 集成模块
==============================

STANDARD NEW ENTERPRISE SETUP FLOW:
====================================
每次接入一个新企业的 API，固定创建以下文件（共 5 个核心文件 + 1 个辅助文件）：

  integrations/<企业名>/
  ├── __init__.py            ← 第 1 步：包标识（空文件即可）
  ├── auth.py               ← 第 2 步：认证层，继承 AuthProvider，从 .env 读 token
  ├── api_client.py         ← 第 3 步：HTTP 客户端，继承 BaseApiClient，设置 token 到请求头
  └── error_code.py         ← 第 4 步：错误码映射（可选，后续补充）

  tests/<企业名>/
  ├── __init__.py            ← 第 5 步：包标识（空文件即可）
  ├── conftest.py            ← 第 6 步：pytest 夹具，创建 api_client fixture
  └── test_xxx.py            ← 第 7 步：写测试用例

  .env                        ← 第 0 步：添加 BASE_URL 和 TOKEN 环境变量

  services/<企业名>/          ← 第 8 步：业务服务层（可选，接口多了再抽象）
  └── xxx_service.py

之后每加一个新模块（如仓库管理、商品管理），只在 tests/ 下加测试文件即可。
"""
