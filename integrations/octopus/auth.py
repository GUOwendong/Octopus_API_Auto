#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证层 (Auth Layer)
====================
职责：从环境变量 .env 中读取 token，提供给 api_client 使用。
每个企业系统需要写自己的 Auth 类，继承框架的 AuthProvider 抽象基类。

使用方式：
    auth = OctopusAuth()        # 实例化，自动从 .env 读取 token
    token = auth.get_token()    # 获取 token 字符串
"""

# os 模块：读取系统环境变量（.env 文件通过 python-dotenv 自动加载到环境变量中）
import os

# 导入框架提供的认证抽象基类，所有企业的 Auth 类都要继承它
from integrations.auth_provider import AuthProvider


class OctopusAuth(AuthProvider):
    """
    八爪鱼系统认证类
    ----------------
    认证方式：JWT Bearer Token（静态 token，从浏览器手动提取后配置在 .env 中）
    继承 AuthProvider，必须实现 get_token() 方法
    """

    def __init__(self):
        """
        初始化时从环境变量 OCTOPUS_TOKEN 读取 token
        os.getenv("KEY", "默认值") → 读环境变量，不存在则返回默认值
        """
        self._token = os.getenv("OCTOPUS_TOKEN", "")

    def get_token(self, force_refresh=False):
        """
        获取认证 token（AuthProvider 要求实现的方法）
        参数 force_refresh：是否强制刷新，此处 token 是静态的，忽略此参数
        返回：token 字符串
        """
        return self._token

    def is_valid(self):
        """
        判断当前 token 是否有效
        此处简单判断 token 是否为空字符串
        """
        return bool(self._token)
