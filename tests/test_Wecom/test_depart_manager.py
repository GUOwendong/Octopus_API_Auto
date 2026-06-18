#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 企业微信部门业务测试，仅调用Service层
"""

import allure
import pytest


@allure.feature("部门管理")
class TestDepartment:

    @allure.story("创建部门")
    @pytest.mark.smoke
    def test_create_department(self, dept_service):
        res = dept_service.create(name="广州研发中心", parentid=1, dept_id=111111)
        assert res["errcode"] == 0

    @allure.story("更新部门")
    @pytest.mark.smoke
    def test_update_department(self, dept_service):
        res = dept_service.update(dept_id=111111, name="地球研发中心")
        assert res["errcode"] == 0

    @allure.story("删除部门")
    @pytest.mark.smoke
    def test_delete_department(self, dept_service):
        res = dept_service.delete(dept_id=111111)
        assert res["errcode"] == 0

    @allure.story("查询部门列表")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="接口暂无权限")
    def test_list_departments(self, dept_service):
        res = dept_service.list()
        assert res["errcode"] == 0
        assert "department" in res
