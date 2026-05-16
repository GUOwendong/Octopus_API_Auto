#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
from base.api_client import ApiClient
from base.wecom_token import WeComTokenManager

class DepartmentService:
    PATH = "/cgi-bin/department"

    def __init__(self):
        self.client = ApiClient("https://qyapi.weixin.qq.com")
        self.token = WeComTokenManager.get_token()

    def create(self, name, parentid):
        return self.client.request(
            "POST",
            f"{self.PATH}/create",
            params={"access_token": self.token},
            json={"name": name, "parentid": parentid}
        )

    def delete(self, id):
        return self.client.request(
            "GET",
            f"{self.PATH}/delete",
            params={"access_token": self.token, "id": id}
        )