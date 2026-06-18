#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证提供者抽象基类

任何企业接入方只需继承 AuthProvider 并实现 get_token()，
框架的 ApiClient / Service 层即可无缝工作。
"""

from abc import ABC, abstractmethod
from typing import Optional


class AuthProvider(ABC):
    """认证提供者抽象接口"""

    @abstractmethod
    def get_token(self, force_refresh: bool = False) -> str:
        """获取认证令牌"""
        ...

    def refresh(self) -> str:
        """强制刷新令牌，默认委托给 get_token(force_refresh=True)"""
        return self.get_token(force_refresh=True)

    def is_valid(self) -> bool:
        """判断当前令牌是否有效，子类按需覆盖"""
        return False


class StaticTokenAuth(AuthProvider):
    """最简单的静态 Token 认证（适用于固定 API Key 场景）"""

    def __init__(self, token: str):
        self._token = token

    def get_token(self, force_refresh: bool = False) -> str:
        return self._token

    def is_valid(self) -> bool:
        return bool(self._token)
