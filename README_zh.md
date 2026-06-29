# 八爪鱼接口自动化

轻量、可扩展的八爪鱼系统 API 自动化测试项目。克隆、配置、运行。

[English Documentation](README.md)

## 特性

- **框架基类** — `AuthProvider` 抽象基类 + `BaseApiClient` HTTP 客户端，换系统无需改底层代码。
- **分层架构** — `base`（HTTP 客户端）→ `integrations`（认证 + API 客户端）→ `services`（业务逻辑）→ `tests`（测试用例）。
- **自动登录** — 通过账号密码自动获取 token，过期自动刷新，无需手动从浏览器复制。
- **数据驱动** — 支持 JSON / YAML / Excel 测试数据；`pytest.mark.parametrize` 集成。
- **随机数据生成** — `generate_orders.py` 每次生成唯一测试数据，避免重复冲突。
- **Allure 报告** — 内建 Allure 集成，自动生成 HTML 测试报告。
- **多平台 CI/CD** — GitHub Actions / GitLab CI / Gitee / Jenkins 四套流水线，含钉钉/企微/飞书/邮件通知。
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
OCTOPUS_USERNAME=你的手机号
OCTOPUS_PASSWORD=你的密码

# =================== 通用配置 ===================
TEST_ENV=test
API_TIMEOUT=30
```

> 程序启动时会自动调用 `/login` 接口，用 `OCTOPUS_USERNAME` + `OCTOPUS_PASSWORD` 换取 token。token 过期后自动重新登录，无需手动维护。

### 4. 运行测试

```bash
# 运行全部八爪鱼测试
uv run pytest tests/test_octopus/ -v -s

# 运行单个模块
uv run pytest tests/test_octopus/test_warehouse_flow.py -v -s     # 仓库管理
uv run pytest tests/test_octopus/test_product_flow.py -v -s       # 商品管理
uv run pytest tests/test_octopus/test_channel_flow.py -v -s       # 渠道管理
uv run pytest tests/test_octopus/test_order_flow.py -v -s         # 订单管理

# 健康检查（验证连通性）
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
│       ├── auth.py                    #     通过账号密码登录获取 token（自动刷新）
│       ├── api_client.py              #     HTTP 客户端（Bearer== 格式）
│       └── error_code.py              #     错误码映射
│
├── services/octopus/                  # 业务服务层 ★
│   ├── warehouse_service.py           #   仓库管理：新增 / 查询 / 列表 / 删除
│   ├── product_service.py             #   商品管理：新增 / 查询 / 下架 / 上架 / 删除
│   ├── channel_service.py             #   渠道管理：新增 / 查询 / 删除
│   └── order_service.py               #   订单管理：导入Excel / 匹配表头 / 绑定商品 / 查询 / 改金额
│
├── tests/test_octopus/                # 测试用例 ★
│   ├── conftest.py                    #   api_client fixture（session级别，自动注入）
│   ├── test_health.py                 #   连通性测试
│   ├── test_warehouse_flow.py         #   仓库全流程：借群 → 新增 → 查询 → 删除
│   ├── test_product_flow.py           #   商品全流程：新增 → 查询 → 下架 → 上架 → 删除
│   ├── test_channel_flow.py           #   渠道全流程：新增 → 查询 → 删除
│   └── test_order_flow.py             #   订单全流程：导入 → 匹配 → 绑定 → 查询 → 改金额
│
├── data/                              # 测试数据
│   ├── json/
│   ├── xlsx/
│   └── yaml/
│
├── .github/workflows/ci.yaml          # GitHub Actions CI 流水线
├── .gitlab-ci.yml                     # GitLab CI 流水线
├── .gitee/workflows/ci.yaml           # Gitee CI 流水线
├── Jenkinsfile                        # Jenkins Pipeline ★
├── conftest.py                        # 全局夹具（失败自动快照）
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

集成层 (integrations) →  只管"Token 怎么获取 / Base URL 是什么"
                       login() 获取 token → "Authorization", "Bearer==xxx"
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
5. **Token 自动管理** — `OctopusAuth.login()` 通过账号密码获取 token，`get_token()` 判断过期自动刷新，上层无需感知。

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
        assert add_res.get("code") == "ok", f"新增失败: {add_res.get('error', add_res)}"

        search_res = service.search(name="测试渠道")
        assert search_res.get("code") == "ok", f"查询失败: {search_res.get('error', search_res)}"

        channel_id = search_res.get("data", {}).get("rows", [{}])[0].get("id")
        del_res = service.delete(channel_id)
        assert del_res.get("code") == "ok", f"删除失败: {del_res.get('error', del_res)}"
```

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

## CI/CD

### 各平台 Secret 配置

所有平台需要配置以下 Secret 才能正常运行 CI：

| Secret | 说明 | 必填 |
|--------|------|------|
| `OCTOPUS_USERNAME` | 八爪鱼登录手机号 | **是** |
| `OCTOPUS_PASSWORD` | 八爪鱼登录密码 | **是** |
| `DINGTALK_WEBHOOK` | 钉钉机器人 Webhook | 否 |
| `WECOM_WEBHOOK` | 企业微信机器人 Webhook | 否 |
| `FEISHU_WEBHOOK` | 飞书机器人 Webhook | 否 |
| `MAIL_USERNAME` | 邮件发送账号 | 否 |
| `MAIL_PASSWORD` | 邮件 SMTP 授权码 | 否 |
| `MAIL_TO` | 邮件接收人 | 否 |

### GitHub Actions

配置路径：`Settings → Secrets and variables → Actions → New repository secret`

预配置 `.github/workflows/ci.yaml`，推送代码自动触发。通知支持：钉钉 / 企业微信 / 飞书 / 邮件。

### GitLab CI

配置路径：`Settings → CI/CD → Variables → Add variable`

预配置 `.gitlab-ci.yml`，推送或 MR 自动触发。

### Gitee

配置路径：`企业管理 → Secrets`

预配置 `.gitee/workflows/ci.yaml`。

### Jenkins

配置路径：`Dashboard → 凭据 → 全局凭据 → Add Credentials`（类型选 Secret Text）

| Credential ID | 值 | 必填 |
|--------------|-----|------|
| `octopus-username` | 你的手机号 | **是** |
| `octopus-password` | 你的密码 | **是** |
| `dingtalk-webhook` | 钉钉机器人 URL | 否 |
| `wecom-webhook` | 企业微信机器人 URL | 否 |
| `feishu-webhook` | 飞书机器人 URL | 否 |
| `mail-to` | 收件人邮箱 | 否 |

Jenkins 流水线通过 `Jenkinsfile` 定义，支持定时触发（每天早晚）、GitLab Push/MR 触发、手动触发。

> **注意**：GitHub Actions / GitLab CI 的公共 Runner 位于海外机房，无法访问内网服务器 `api.wxorder.taover.com`。如需 CI 真正跑通测试，需要在内网机器上部署自建 Runner。

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

一般为 token 过期。程序已支持自动登录刷新，通常不会出现此问题。如果仍然出现，检查 `.env` 中的 `OCTOPUS_USERNAME` / `OCTOPUS_PASSWORD` 是否正确，或账号是否被锁定。

### Q: 仓库测试报 `该群已被仓库使用`？

一个微信群只能绑定一个仓库。`test_warehouse_flow.py` 采用了"借群"策略：先查所有仓库（`size=100`），找一个带群的删掉释放群资源，再用这个群创建测试仓库。如果线上所有仓库都有关联数据（订单/商品），无法删除释放群，则需要联系运维创建一个专用测试群。

### Q: 订单测试报 `该Excel文件正处于其他操作流程中`？

订单是异步生成的，上一次测试的 Excel 文件还在后台处理。等几分钟再跑，或者换一个收件人姓名（`generate_orders.py` 每次随机生成）。

### Q: 查询订单结果为空？

订单绑定商品后有异步处理延迟，需要在 `bind_goods` 步骤后 `time.sleep(3)` 等待服务器处理完毕。

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
