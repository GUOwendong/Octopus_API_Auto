#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import os.path
from config.global_config import base_dir
from common.file_utils import FileUtil

xlsx_data = os.path.join(base_dir, "data", "xlsx", "create_department.xlsx")
yaml_dir = os.path.join(base_dir, "data", "yaml", "update_department.yaml")

data = FileUtil.read_excel(xlsx_data)

FileUtil.write_yaml(yaml_dir, data)



