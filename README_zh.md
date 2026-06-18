# 接口自动化框架

轻量、可扩展、多企业即插即用的 API 自动化框架。克隆、配置、运行——零改动适配你自身的业务。

[English Documentation](README.md)

## 特性

- **多企业即插即用** — 可插拔的 `AuthProvider` + `ApiClient`，换企业不需要改框架代码。
- **分层架构** — `base`（HTTP 客户端）→ `integrations`（认证 + API 客户端）→ `services`（业务逻辑）→ `tests`（测试用例）。
- **数据驱动** — 支持 JSON / YAML / Excel 测试数据，原生集成 `pytest.mark.parametrize`。
- **Allure 报告** — 内建 Allure 集成，自动生成 HTML 测试报告。
- **CI/CD 就绪** — 预配置 GitHub Actions、GitLab CI、Gitee 流水线。
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
| openpyxl / pandas | Excel 数据读写 |
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

```bash
# 复制模板并填入实际值
cp .env.example .env
```

编辑 `.env`：

```env
# 环境选择：dev / test / prod
TEST_ENV=test

# 各环境 API 基础地址
API_BASE_URL_DEV=http://127.0.0.1:8000
API_BASE_URL_TEST=http://127.0.0.1:8000
API_BASE_URL_PROD=http://127.0.0.1:8000

# HTTP 请求超时（秒）
API_TIMEOUT=30

# 企业特有凭据（示例：企业微信）
WECOM_BASE_URL=https://qyapi.weixin.qq.com
WECOM_CORP_ID=你的企业ID
WECOM_CONTACT_SECRET=你的应用Secret
```

### 4. 运行测试

```bash
# 运行全部测试
uv run pytest

# 指定环境运行
uv run python main.py -e test

# 按标记运行
uv run pytest -m smoke

# 运行单个测试文件
uv run pytest tests/test_Wecom/test_create_department.py -v
```

### 5. 查看报告

```bash
# 一键运行 + 生成报告
uv run python main.py -e test

# 打开 Allure 报告
allure open reports/allure-report
```

或启动本地静态服务器：

```bash
cd reports/allure-report && python -m http.server 8080
```

## 项目结构

```
.
├── base/                        # 框架核心（零业务逻辑）
│   └── base_api_client.py       #   通用 HTTP 客户端基类
├── common/                      # 通用工具
│   ├── file_utils.py            #   Excel / JSON / YAML 读写
│   └── log_utils.py             #   基于 loguru 的日志配置
├── config/
│   └── global_config.py         #   路径、环境、API 地址（环境变量驱动）
├── integrations/                # 外部系统集成
│   ├── auth_provider.py         #   AuthProvider 抽象基类 + StaticTokenAuth
│   └── wecom/                   #   企业微信集成（示例）
│       ├── api_client.py        #     企业微信专用 HTTP 客户端
│       ├── wecom_token.py       #     Token 管理器（实现 AuthProvider）
│       └── wecom_error_code.py  #     错误码映射
├── services/                    # 业务服务层
│   └── wecom/
│       └── department_service.py #   企业微信部门 CRUD
├── tests/                       # 测试用例
│   └── test_Wecom/
│       ├── conftest.py          #   企业微信夹具（api_client, dept_service）
│       ├── test_create_department.py
│       ├── test_update_department.py
│       ├── test_delete_department.py
│       └── test_depart_manager.py
├── data/                        # 测试数据
│   ├── xlsx/                    #   Excel 测试数据
│   └── yaml/                    #   YAML 测试数据
├── .env.example                 # 环境变量模板
├── conftest.py                  # 全局 pytest 夹具（框架级别）
├── main.py                      # CLI 入口（环境切换 + Allure 报告）
├── pyproject.toml               # 项目配置与依赖
└── uv.lock                      # 锁定依赖版本
```

## 架构设计

```
┌──────────────────────────────────────────────────┐
│                    tests/                         │
│   conftest.py → api_client fixture                │
│   （每个企业、每个模块独立定义）                      │
└────────────────────┬─────────────────────────────┘
                     │ 依赖
┌────────────────────▼─────────────────────────────┐
│                  services/                        │
│   业务逻辑，调用 integrations.ApiClient             │
└────────────────────┬─────────────────────────────┘
                     │ 依赖
┌────────────────────▼─────────────────────────────┐
│               integrations/                       │
│   ├── auth_provider.py    (AuthProvider 抽象)      │
│   └── <企业名称>/                                  │
│       ├── api_client.py   (继承 BaseApiClient)     │
│       ├── auth.py         (继承 AuthProvider)      │
│       └── error_code.py                           │
└────────────────────┬─────────────────────────────┘
                     │ 依赖
┌────────────────────▼─────────────────────────────┐
│                   base/                           │
│   base_api_client.py  （纯 HTTP，无任何业务）       │
└──────────────────────────────────────────────────┘
```

### 核心设计原则

1. **根 `conftest.py` 与企业无关** — 只包含框架级别的夹具（如失败快照）。
2. **每个企业独立管理自己的 `api_client` fixture** — 在 `tests/<企业>/conftest.py` 中定义。
3. **认证是可插拔接口** — `AuthProvider` 抽象基类；企业微信的 `WeComTokenManager` 只是其中一个实现。
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
        # 在这里实现你的认证逻辑
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

@pytest.fixture(scope="session")
def ecs_service(api_client):
    return ECSService(client=api_client)
```

### 第四步：在 `.env` 中添加凭据

```env
ALICLOUD_BASE_URL=https://ecs.aliyun.com
ALICLOUD_ACCESS_TOKEN=你的token
```

**框架文件（`base/`、`common/`、`config/`、根 `conftest.py`）无需任何修改。**

## 按标记运行

```bash
# 仅冒烟测试
uv run pytest -m smoke

# 回归测试
uv run pytest -m regression

# 某个企业的测试
uv run pytest -m wecom

# 组合标记
uv run pytest -m "smoke and wecom"
```

## 只运行失败的用例

```bash
uv run pytest --lf       # 仅上次失败的
uv run pytest --ff       # 先跑失败的，再跑其余的
```

## 失败重跑

```bash
uv run pytest --reruns 2 --reruns-delay 1
```

## CI/CD

### GitHub Actions

推送到 `main` 分支或创建 PR 时自动触发。流水线步骤：
1. 安装 uv + 项目依赖
2. 执行 pytest 生成 Allure 原始数据
3. 生成 Allure HTML 报告
4. 上传报告 artifact
5. 部署到 GitHub Pages
6. 发送通知（钉钉 / 企业微信 / 邮件）

需要在 GitHub 仓库 `Settings → Secrets` 中配置：

| Secret | 说明 |
|--------|------|
| `WECOM_CORP_ID` | 企业微信 Corp ID |
| `WECOM_CONTACT_SECRET` | 企业微信通讯录 Secret |
| `DING_WEBHOOK` | 钉钉机器人 Webhook |
| `WECOM_WEBHOOK` | 企业微信机器人 Webhook |
| `MAIL_USERNAME` | SMTP 发件邮箱 |
| `MAIL_PASSWORD` | SMTP 邮箱密码/授权码 |
| `MAIL_TO` | 收件邮箱 |

### GitLab CI

`.gitlab-ci.yaml` 已预配置。在 GitLab 项目 `Settings → CI/CD → Variables` 中添加：

- `WECOM_CORP_ID`
- `WECOM_CONTACT_SECRET`

### Gitee

`.gitee/workflows/ci.yaml` 已预配置。

## 代码质量

```bash
# 运行所有 pre-commit 检查
uv run pre-commit run --all-files

# 代码格式化
uv run black .
uv run isort .

# 代码检查
uv run flake8 .
```

## 常见问题

### Q: 如何添加新的依赖包？

```bash
uv add <包名>
```

这会同时更新 `pyproject.toml` 和 `uv.lock`。

### Q: 如何更换 Python 版本？

修改 `pyproject.toml` 中的 `requires-python`，然后运行：

```bash
uv sync
```

### Q: 提示 allure 命令找不到？

```bash
# macOS
brew install allure

# Linux（手动安装）
wget -qO allure.tgz https://github.com/allure-framework/allure2/releases/download/2.39.0/allure-2.39.0.tgz
tar -zxf allure.tgz
sudo mv allure-2.39.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure
```

### Q: 如何并行执行测试？

```bash
uv add pytest-xdist
uv run pytest -n auto
```

### Q: 框架支持 gRPC / WebSocket 吗？

目前不支持 — 本框架定位为 RESTful HTTP API 自动化。如需其他协议，可在 `base_api_client.py` 基础上扩展。

## License

Internal use.
