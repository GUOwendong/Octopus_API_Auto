#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误码映射 (Error Code Mapping)
================================
职责：把服务器返回的业务错误码（如 1001、2001）翻译成人类可读的错误信息。

用法示例：
    from integrations.octopus.error_code import get_error_message
    msg = get_error_message(1001)  # 返回 "商品不存在" 之类的描述

当前为空壳，等你抓完接口后，根据实际业务错误码补充。
"""


# TODO: 抓完接口后，把错误码和错误信息填在这里
# 格式参考：
# ERROR_CODE_MAP = {
#     1001: "商品不存在",
#     2001: "仓库已满",
#     3001: "渠道信息不全",
# }
#
# def get_error_message(code: int) -> str:
#     return ERROR_CODE_MAP.get(code, f"未知错误({code})")
