#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import os
import json
import yaml
import pandas as pd
from common.log_utils import log
from config.global_config import base_dir


class FileUtil:

# ======================================= Excel 操作 ===========================================
    @staticmethod
    def read_excel(file_name, sheet_name=0):
        file_path = os.path.join(base_dir, "data", file_name)
        if not os.path.exists(file_path):
            log.error(f"❌ EXCEL Read failure: File does not exist {file_path}")
            raise FileNotFoundError(f"Excel file does not exist：{file_path}")
        try:
            data_file = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
            data_file = data_file.fillna("")
            log.info(f"✅ EXCEL Read failure：{file_path}")
            return data_file.to_dict("records")
        except Exception as e:
            log.error(f"❌ EXCEL Read failure：{file_path}，error：{str(e)}")
            raise

    @staticmethod
    def write_excel(file_name, data):
        file_path = os.path.join(base_dir, "data", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not data:
            log.warning(f"⚠️ EXCEL 写入警告：数据为空，文件：{file_path}")
        try:
            data_file = pd.DataFrame(data)
            data_file = data_file.fillna("")  # 新增：空值转空字符串，避免Excel显示NaN
            data_file.to_excel(file_path, index=False, engine="openpyxl")
            log.info(f"✅ EXCEL 写入成功：{file_path}")  # 新增：写入成功日志
        except Exception as e:
            log.error(f"❌ EXCEL 写入失败：{file_path}，错误：{str(e)}")
            raise

# ======================================== JSON 操作 =============================================
    @staticmethod
    def read_json(file_name, encoding="utf-8"):
        file_path = os.path.join(base_dir, "data", file_name)
        # 新增：检查文件是否存在
        if not os.path.exists(file_path):
            log.error(f"❌ JSON 读取失败：文件不存在 {file_path}")
            raise FileNotFoundError(f"JSON文件不存在：{file_path}")
        try:
            with open(file_path, "r", encoding=encoding) as f:
                data = json.load(f)
                log.info(f"✅ JSON 读取成功：{file_path}")
                return data
        except Exception as e:
            log.error(f"❌ JSON 读取失败：{file_path}，错误：{str(e)}")
            raise

    @staticmethod
    def write_json(file_name, data, encoding="utf-8"):
        file_path = os.path.join(base_dir, "data", file_name)
        # 新增1：自动创建data文件夹
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            log.info(f"✅ JSON 写入成功：{file_path}")  # 新增：写入成功日志
        except Exception as e:
            log.error(f"❌ JSON 写入失败：{file_path}，错误：{str(e)}")
            raise

# ======================================== YAML 操作 ================================================
    @staticmethod
    def read_yaml(file_name, encoding="utf-8"):
        file_path = os.path.join(base_dir, "data", file_name)
        # 新增：检查文件是否存在
        if not os.path.exists(file_path):
            log.error(f"❌ YAML 读取失败：文件不存在 {file_path}")
            raise FileNotFoundError(f"YAML文件不存在：{file_path}")
        try:
            with open(file_path, "r", encoding=encoding) as f:
                data = yaml.safe_load(f) or {}  # 新增：空YAML返回空字典，避免None
                log.info(f"✅ YAML 读取成功：{file_path}")
                return data
        except Exception as e:
            log.error(f"❌ YAML 读取失败：{file_path}，错误：{str(e)}")
            raise

    @staticmethod
    def write_yaml(file_name, data, encoding="utf-8"):
        file_path = os.path.join(base_dir, "data", file_name)
        # 新增1：自动创建data文件夹
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding=encoding) as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            log.info(f"✅ YAML 写入成功：{file_path}")  # 新增：写入成功日志
        except Exception as e:
            log.error(f"❌ YAML 写入失败：{file_path}，错误：{str(e)}")
            raise