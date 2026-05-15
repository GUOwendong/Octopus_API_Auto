#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import logging
from typing import Optional, Dict, Any, Union
from requests.exceptions import RequestException, Timeout, ConnectionError
import requests
from config import API_BASE_URL, TIMEOUT


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = TIMEOUT
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': 'ApiClient/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, path: str, raise_for_status: bool = True,
                 **kwargs) -> requests.Response:
        """
        统一请求方法
        :param method: HTTP方法 (GET, POST, PUT, DELETE等)
        :param path: API路径
        :param raise_for_status: 是否自动抛出HTTP错误状态码异常
        :param kwargs: 其他requests参数
        :return: Response对象
        """
        url = self.base_url + path

        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if raise_for_status:
                resp.raise_for_status()
            return resp
        except Timeout:
            self.logger.error(f"Request timeout: {method} {url}")
            raise
        except ConnectionError:
            self.logger.error(f"Connection error: {method} {url}")
            raise
        except RequestException as e:
            self.logger.error(f"Request failed: {method} {url}, error: {e}")
            raise

    def get(self, path: str, params: Optional[Dict] = None,
            headers: Optional[Dict] = None, raise_for_status: bool = True) -> requests.Response:
        """
        发送GET请求
        :param path: API路径
        :param params: URL查询参数
        :param headers: 请求头
        :param raise_for_status: 是否自动抛出HTTP错误
        :return: Response对象
        """
        return self._request('GET', path, params=params, headers=headers,
                             raise_for_status=raise_for_status)

    def post(self, path: str, data: Optional[Dict] = None,
             json: Optional[Dict] = None, headers: Optional[Dict] = None,
             raise_for_status: bool = True) -> requests.Response:
        """
        发送POST请求
        :param path: API路径
        :param data: 表单数据
        :param json: JSON数据
        :param headers: 请求头
        :param raise_for_status: 是否自动抛出HTTP错误
        :return: Response对象
        """
        return self._request('POST', path, data=data, json=json, headers=headers,
                             raise_for_status=raise_for_status)

    def put(self, path: str, json: Optional[Dict] = None,
            headers: Optional[Dict] = None, raise_for_status: bool = True) -> requests.Response:
        """
        发送PUT请求
        :param path: API路径
        :param json: JSON数据
        :param headers: 请求头
        :param raise_for_status: 是否自动抛出HTTP错误
        :return: Response对象
        """
        return self._request('PUT', path, json=json, headers=headers,
                             raise_for_status=raise_for_status)

    def delete(self, path: str, headers: Optional[Dict] = None,
               raise_for_status: bool = True) -> requests.Response:
        """
        发送DELETE请求
        :param path: API路径
        :param headers: 请求头
        :param raise_for_status: 是否自动抛出HTTP错误
        :return: Response对象
        """
        return self._request('DELETE', path, headers=headers,
                             raise_for_status=raise_for_status)

    def patch(self, path: str, json: Optional[Dict] = None,
              headers: Optional[Dict] = None, raise_for_status: bool = True) -> requests.Response:
        """
        发送PATCH请求
        :param path: API路径
        :param json: JSON数据
        :param headers: 请求头
        :param raise_for_status: 是否自动抛出HTTP错误
        :return: Response对象
        """
        return self._request('PATCH', path, json=json, headers=headers,
                             raise_for_status=raise_for_status)

    def get_json(self, path: str, params: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Union[Dict, Any]:
        """
        发送GET请求并返回JSON数据
        :param path: API路径
        :param params: URL查询参数
        :param headers: 请求头
        :return: JSON数据
        """
        resp = self.get(path, params=params, headers=headers)
        return resp.json() if resp.content else None

    def post_json(self, path: str, json: Optional[Dict] = None,
                  headers: Optional[Dict] = None) -> Union[Dict, Any]:
        """
        发送POST请求并返回JSON数据
        :param path: API路径
        :param json: JSON数据
        :param headers: 请求头
        :return: JSON数据
        """
        resp = self.post(path, json=json, headers=headers)
        return resp.json() if resp.content else None

    def set_auth_token(self, token: str):
        """
        设置认证Token
        :param token: Bearer token
        """
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def set_header(self, key: str, value: str):
        """
        设置自定义请求头
        :param key: 请求头键
        :param value: 请求头值
        """
        self.session.headers.update({key: value})

    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)

    # 使用方式1：基本使用
    client = ApiClient()
    try:
        # GET请求
        response = client.get('/users/123')
        print(f"Status: {response.status_code}")
        print(f"Data: {response.json()}")

        # POST请求
        new_user = {"name": "John Doe", "email": "john@example.com"}
        response = client.post('/users', json=new_user)

    except RequestException as e:
        print(f"Request error: {e}")
    finally:
        client.close()

    # 使用方式2：上下文管理器
    with ApiClient() as client:
        # 设置认证token
        client.set_auth_token("your_token_here")

        # 获取JSON数据
        data = client.get_json('/users/123')
        print(f"User data: {data}")

        # 发送JSON数据
        result = client.post_json('/users', json={"name": "Jane"})
        print(f"Result: {result}")