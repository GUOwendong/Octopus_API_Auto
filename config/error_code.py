#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
from enum import IntEnum

class WeComErrorCode(IntEnum):
    SUCCESS = 0
    INVALID_TOKEN = 40001
    MISSING_TOKEN = 41001
    INVALID_PARTY_ID = 60123
    PARENT_DEPT_NOT_FOUND = 60004

ERROR_MSG = {
    0: "ok",
    60123: "invalid party id",
    60004: "parent department not found",
}

def get_errmsg(code: int) -> str:
    return ERROR_MSG.get(code, "unknown error")