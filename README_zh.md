# 接口自动化框架

轻量、可扩展、多企业即插即用的 API 自动化框架。克隆、配置、运行——零改动适配你自身的业务。

[English Documentation](README.md)

## 特性

- **多企业即插即用** — 可插拔的 `AuthProvider` + `ApiClient`，换企业不需要改框架代码。
- **分层架构** — `base`（HTTP 客户端）→ `integrations`（认证 + API 客户端）→ `services`（业务逻辑）→ `tests`（测试用例）。
- **数据驱动** — 支持 JSON / YAML / Excel 测试数据；`pytest.mark.parametrize` 集成。
- **随机数据生成** — `generate_orders.py` 每次生成唯一测试数据，避免重复冲突。
- **Allure 报告** — 内建 Allure 集成，自动生成 HTML 测试报告。
- **CI/CD 就绪** — 预配置 GitHub Actions、GitLab CI、Gitee 流水线（含钉钉/企微/邮件通知）。
- **代码质量** — 开箱即用的 `black` + `isort` + `pre-commit`。
- **失败快照** — 测试失败自动保存上下文快照，快速定位问题。

## 技术栈

| 工具 | 版本 |
|------|------|
| Python | >= 3.13 |
| uv | latest |
| pytest | >= 9.0 |
| requests | >= 2.34 |
| Allure | >= 2.16 (pytest 插件) |
| loguru | >= 0.7 |
| pandas / openpyxl | Excel 数据读写 |
| PyYAML | YAML 数据读写 |

## 快速开始

### 1. 前置条件

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)（极速 Python 包管理器）
- [Allure CLI](https://docs.qameta.io/allure/)（用于生成报告）
- Java 8+（Allure CLI 依赖）

### 2. 克隆并安装

```bash
git clone <仓库地址>
cd <项目目录>

# 如果没有 uv，先安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖（自动创建 .venv 虚拟环境）
uv sync

# 安装 pre-commit 钩子（可选）
uv run pre-commit install
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# =================== 八爪鱼系统 ===================
OCTOPUS_BASE_URL=http://api.wxorder.taover.com
OCTOPUS_TOKEN=<从浏览器F12抓取的JWT Token>

# =================== 通用配置 ===================
TEST_ENV=test
API_TIMEOUT=30
```

> `OCTOPUS_TOKEN` 从浏览器 F12 → Network → 任一请求 → Request Headers → `Authorization: Bearer==xxx` 复制 `xxx` 部分。

### 4. 运行测试

```bash
# 运行全部八爪鱼测试
uv run pytest tests/test_octopus/ -v -s

# 运行单个模块
uv run pytest tests/test_octopus/test_warehouse_flow.py -v -s     # 仓库管理
uv run pytest tests/test_octopus/test_product_flow.py -v -s       # 商品管理
uv run pytest tests/test_octopus/test_channel_flow.py -v -s       # 渠道管理
uv run pytest tests/test_octopus/test_order_flow.py -v -s         # 订单管理

# 连通性测试（验证 token 是否有效）
uv run pytest tests/test_octopus/test_health.py -v -s

# 运行并生成 Allure 报告
uv run pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### 5. 一键运行 + 报告

```bash
uv run python main.py -e test
```

## 项目结构

```
Octopus_API_Auto/
│
├── base/                              # 框架核心（零业务逻辑）
│   └── base_api_client.py             #   通用 HTTP 客户端基类
│
├── common/                            # 通用工具
│   ├── log_utils.py                   #   基于 loguru 的日志配置
│   ├── file_utils.py                  #   Excel / JSON / YAML 读写
│   └── generate_orders.py             #   随机生成订单 Excel 数据 ★
│
├── config/
│   └── global_config.py               #   路径、环境、API 地址（环境变量驱动）
│
├── integrations/                      # 外部系统集成层（接入一次，不再改动）
│   ├── auth_provider.py               #   AuthProvider 抽象基类 + StaticTokenAuth
│   └── octopus/                       #   八爪鱼系统集成
│       ├── __init__.py                #     接入新企业的标准流程文档
│       ├── auth.py                    #     从 .env 读 OCTOPUS_TOKEN
│       ├── api_client.py              #     HTTP 客户端（Bearer== 格式）
│       └── error_code.py              #     错误码映射（待补充）
│
├── services/octopus/                  # 业务服务层 ★
│   ├── warehouse_service.py           #   仓库管理：新增 / 查询 / 列表 / 删除
│   ├── product_service.py             #   商品管理：新增 / 查询 / 下架 / 上架 / 删除
│   ├── channel_service.py             #   渠道管理：新增 / 查询 / 删除
│   └── order_service.py               #   订单管理：导入Excel / 匹配表头 / 关联 / 查询 / 改金额
│
├── tests/test_octopus/                # 测试用例 ★
│   ├── conftest.py                    #   api_client fixture（session级别，自动注入）
│   ├── test_health.py                 #   连通性测试
│   ├── test_warehouse_flow.py         #   仓库全流程：借群 → 新增 → 查询 → 删除
│   ├── test_product_flow.py           #   商品全流程：新增 → 查询 → 下架 → 上架 → 删除
│   ├── test_channel_flow.py           #   渠道全流程：新增 → 查询 → 删除
│   └── test_order_flow.py             #   订单全流程：导入 → 匹配 → 关联 → 查询 → 改金额
│
├── data/                              # 测试数据
│   ├── json/
│   ├── xlsx/
│   └── yaml/
│
├── conftest.py                        # 全局夹具（失败自动截图）
├── main.py                            # CLI 入口（环境切换 + Allure）
├── pyproject.toml                     # 项目配置与依赖
└── uv.lock                            # 锁定依赖版本
```

## 架构设计

### 三层分工

```
测试层 (tests)        →  只管"这个接口通了没有"
                        service.add() / service.search() / service.delete()

业务层 (services)     →  只管"URL 是什么 / 方法是什么 / 传什么参数"
                        self.client.post("/v1/xxx", json={...})

集成层 (integrations) →  只管"Token 怎么带 / Base URL 是什么"
                        "Authorization", "Bearer==xxx"
```

### 数据流

```
test_warehouse_flow.py              # 测试用例
  │  service = WarehouseService(api_client)
  │  service.add(name="测试仓库", **group_info)
  ▼
warehouse_service.py                # 业务层
  │  self.client.post("/v1/wxorderware", json=body)
  ▼
api_client.py                       # 集成层
  │  self.set_header("Authorization", f"Bearer=={token}")
  ▼
base_api_client.py                  # 框架层
  │  self.session.request("POST", base_url + path, ...)
  ▼
api.wxorder.taover.com              # 服务器
```

### 核心设计原则

1. **根 `conftest.py` 与企业无关** — 只包含框架级别的夹具（如失败快照）。
2. **每个企业独立管理自己的 `api_client` fixture** — 在 `tests/<企业>/conftest.py` 中定义。
3. **认证是可插拔接口** — `AuthProvider` 抽象基类；八爪鱼的 `OctopusAuth` 只是其中一个实现。
4. **所有配置通过环境变量** — 零硬编码的 URL 和凭据。

## 接入新企业

假设你需要测试"阿里云"的 API：

### 第一步：创建集成层

```
integrations/alicloud/
├── __init__.py
├── api_client.py      # class AliCloudClient(BaseApiClient)
├── auth.py            # class AliCloudAuth(AuthProvider)
└── error_code.py
```

`integrations/alicloud/auth.py`：

```python
import os
from integrations.auth_provider import AuthProvider

class AliCloudAuth(AuthProvider):
    def get_token(self, force_refresh=False):
        return os.getenv("ALICLOUD_ACCESS_TOKEN", "")

    def is_valid(self):
        return bool(self._get_cached_token())
```

`integrations/alicloud/api_client.py`：

```python
from base.base_api_client import BaseApiClient
from config.global_config import TIMEOUT

class AliCloudClient(BaseApiClient):
    def __init__(self, base_url: str, timeout: int = None):
        super().__init__(base_url=base_url, timeout=timeout or TIMEOUT)

    def set_access_token(self, token: str):
        self.set_header("Authorization", f"Bearer {token}")
```

### 第二步：创建服务层

```
services/alicloud/
├── __init__.py
└── ecs_service.py
```

### 第三步：创建测试夹具

```
tests/test_AliCloud/
├── __init__.py
├── conftest.py
└── test_ecs.py
```

`tests/test_AliCloud/conftest.py`：

```python
import os
import pytest
from integrations.alicloud.api_client import AliCloudClient
from integrations.alicloud.auth import AliCloudAuth
from services.alicloud.ecs_service import ECSService

@pytest.fixture(scope="session")
def api_client():
    auth = AliCloudAuth()
    base_url = os.getenv("ALICLOUD_BASE_URL", "https://ecs.aliyun.com")
    client = AliCloudClient(base_url=base_url)
    client.set_access_token(auth.get_token())
    yield client
    client.close()
```

### 第四步：在 `.env` 中添加凭据

```env
ALICLOUD_BASE_URL=https://ecs.aliyun.com
ALICLOUD_ACCESS_TOKEN=你的token
```

**框架文件（`base/`、`common/`、`config/`、根 `conftest.py`）无需任何修改。**

## 照猫画虎：新增一个模块

以"渠道管理"为例，每个模块只需要 2 个文件：

**1. `services/octopus/channel_service.py`（接口封装）：**

```python
class ChannelService:
    def __init__(self, client):
        self.client = client

    def add(self, name, **kwargs):
        resp = self.client.post("/v1/wxorderchannel", json={"name": name, **kwargs})
        return resp.json()

    def search(self, name):
        resp = self.client.get("/v1/wxorderchannel", params={"name": name})
        return resp.json()

    def delete(self, channel_id):
        resp = self.client.delete(f"/v1/wxorderchannel/{channel_id}")
        return resp.json()
```

**2. `tests/test_octopus/test_channel_flow.py`（测试用例）：**

```python
from services.octopus.channel_service import ChannelService

class TestChannel:
    def test_channel_flow(self, api_client):
        service = ChannelService(api_client)

        add_res = service.add(name="测试渠道")
        assert add_res.get("code") == "ok"

        search_res = service.search(name="测试渠道")
        assert search_res.get("code") == "ok"

        channel_id = search_res["data"]["rows"][0]["id"]
        del_res = service.delete(channel_id)
        assert del_res.get("code") == "ok"
```

## CI/CD

### GitHub Actions

需要在 GitHub 仓库 `Settings → Secrets and variables → Actions` 中配置：

| Secret | 说明 |
|--------|------|
| `OCTOPUS_TOKEN` | 八爪鱼 JWT Token（必填） |
| `WECOM_CORP_ID` | 企业微信 Corp ID |
| `WECOM_CONTACT_SECRET` | 企业微信通讯录 Secret |
| `DING_WEBHOOK` | 钉钉机器人 Webhook |
| `WECOM_WEBHOOK` | 企业微信机器人 Webhook |

### GitLab CI

在 GitLab 项目 `Settings → CI/CD → Variables` 中添加：

- `OCTOPUS_TOKEN`
- `WECOM_CORP_ID`
- `WECOM_CONTACT_SECRET`

### Gitee

在项目设置 → 密钥管理中添加 `OCTOPUS_TOKEN` 等。

## 代码质量

```bash
# 运行所有 pre-commit 检查
uv run pre-commit run --all-files

# 代码格式化
uv run black .
uv run isort .
```

## 常见问题

### Q: 运行测试提示 `not_authorized`？

token 过期了。打开浏览器 F12 → 复制新的 `Authorization: Bearer==xxx` 值 → 更新 `.env` 中的 `OCTOPUS_TOKEN`。

### Q: 仓库测试报 `该群已被仓库使用`？

一个微信群只能绑定一个仓库。`test_warehouse_flow.py` 采用了"借群"策略：先查所有仓库，找一个带群的删掉释放群资源，再用这个群创建测试仓库。

### Q: 订单测试报 `该Excel文件正处于其他操作流程中`？

订单是异步生成的，上一次测试的 Excel 文件还在后台处理。等几分钟再跑，或者换个收货人姓名。

### Q: 如何添加新的依赖包？

```bash
uv add <包名>
```

### Q: 如何并行执行测试？

```bash
uv add pytest-xdist
uv run pytest -n auto
```

## License
