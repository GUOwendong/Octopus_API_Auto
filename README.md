# Interface Automation Framework

A lightweight, extensible, multi-enterprise API automation framework. Clone, configure, and run — zero adaptation needed for your own business.

[中文文档](README_zh.md)

## Features

- **Multi-Enterprise Ready** — Pluggable `AuthProvider` and `ApiClient`; no framework code changes when switching enterprises.
- **Layered Architecture** — `base` (HTTP client) → `integrations` (auth + API client) → `services` (business logic) → `tests` (test cases).
- **Data-Driven** — Supports JSON / YAML / Excel test data; `pytest.mark.parametrize` integration.
- **Random Data Generation** — `generate_orders.py` creates unique test data per run, avoiding conflicts.
- **Allure Reports** — Built-in Allure integration with automatic HTML report generation.
- **CI/CD Ready** — Pre-configured pipelines for GitHub Actions, GitLab CI, and Gitee (with DingTalk/WeCom/email notifications).
- **Code Quality** — `black` + `isort` + `pre-commit` hooks out of the box.
- **Failure Snapshots** — Automatic context snapshot saved when a test fails, for fast triage.

## Tech Stack

| Tool | Version |
|------|---------|
| Python | >= 3.13 |
| uv | latest |
| pytest | >= 9.0 |
| requests | >= 2.34 |
| Allure | >= 2.16 (pytest plugin) |
| loguru | >= 0.7 |
| pandas / openpyxl | for Excel data |
| PyYAML | for YAML data |

## Quick Start

### 1. Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- [Allure CLI](https://docs.qameta.io/allure/) (for report generation)
- Java 8+ (required by Allure CLI)

### 2. Clone & Install

```bash
git clone <your-repo-url>
cd <project-dir>

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv automatically)
uv sync

# Install pre-commit hooks (optional)
uv run pre-commit install
```

### 3. Configuration

Create a `.env` file in the project root:

```env
# =================== Octopus System ===================
OCTOPUS_BASE_URL=http://api.wxorder.taover.com
OCTOPUS_TOKEN=<JWT token copied from browser DevTools>

# =================== General ==========================
TEST_ENV=test
API_TIMEOUT=30
```

> Get `OCTOPUS_TOKEN` from browser F12 → Network → any request → Request Headers → copy the value after `Authorization: Bearer==`.

### 4. Run Tests

```bash
# Run all Octopus tests
uv run pytest tests/test_octopus/ -v -s

# Run individual modules
uv run pytest tests/test_octopus/test_warehouse_flow.py -v -s     # Warehouse
uv run pytest tests/test_octopus/test_product_flow.py -v -s       # Product
uv run pytest tests/test_octopus/test_channel_flow.py -v -s       # Channel
uv run pytest tests/test_octopus/test_order_flow.py -v -s         # Order

# Health check (verify token is valid)
uv run pytest tests/test_octopus/test_health.py -v -s

# Run with Allure report
uv run pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### 5. One-Click Run + Report

```bash
uv run python main.py -e test
```

## Project Structure

```
Octopus_API_Auto/
│
├── base/                              # Framework core (zero business logic)
│   └── base_api_client.py             #   Generic HTTP client base class
│
├── common/                            # Shared utilities
│   ├── log_utils.py                   #   loguru-based logging
│   ├── file_utils.py                  #   Excel / JSON / YAML reader & writer
│   └── generate_orders.py             #   Random order Excel generator ★
│
├── config/
│   └── global_config.py               #   Paths, env, API URLs (env-var driven)
│
├── integrations/                      # External system integrations (set up once)
│   ├── auth_provider.py               #   AuthProvider ABC + StaticTokenAuth
│   └── octopus/                       #   Octopus system integration
│       ├── __init__.py                #     Standard setup flow documentation
│       ├── auth.py                    #     Reads OCTOPUS_TOKEN from .env
│       ├── api_client.py              #     HTTP client (Bearer== format)
│       └── error_code.py              #     Error code mapping (TBD)
│
├── services/octopus/                  # Business service layer ★
│   ├── warehouse_service.py           #   Warehouse: add / search / list_all / delete
│   ├── product_service.py             #   Product: create / search / delist / relist / delete
│   ├── channel_service.py             #   Channel: add / search / delete
│   └── order_service.py               #   Order: import / match / bind / search / modify
│
├── tests/test_octopus/                # Test cases ★
│   ├── conftest.py                    #   api_client fixture (session-scoped, auto-injected)
│   ├── test_health.py                 #   Connectivity check
│   ├── test_warehouse_flow.py         #   Warehouse flow: borrow → create → search → delete
│   ├── test_product_flow.py           #   Product flow: create → search → delist → relist → delete
│   ├── test_channel_flow.py           #   Channel flow: create → search → delete
│   └── test_order_flow.py             #   Order flow: import → match → bind → search → modify
│
├── data/                              # Test data
│   ├── json/
│   ├── xlsx/
│   └── yaml/
│
├── conftest.py                        # Global fixtures (auto failure snapshot)
├── main.py                            # CLI entry point (env switching + Allure)
├── pyproject.toml                     # Project config & dependencies
└── uv.lock                            # Locked dependency versions
```

## Architecture

### Three-Layer Separation

```
tests layer         →  Only knows "did the API work?"
                       service.add() / service.search() / service.delete()

services layer      →  Only knows "what URL / method / parameters?"
                       self.client.post("/v1/xxx", json={...})

integrations layer  →  Only knows "how to attach the token?"
                       "Authorization", "Bearer==xxx"
```

### Request Flow

```
test_warehouse_flow.py              # Test case
  │  service = WarehouseService(api_client)
  │  service.add(name="test_warehouse", **group_info)
  ▼
warehouse_service.py                # Service layer
  │  self.client.post("/v1/wxorderware", json=body)
  ▼
api_client.py                       # Integration layer
  │  self.set_header("Authorization", f"Bearer=={token}")
  ▼
base_api_client.py                  # Framework layer
  │  self.session.request("POST", base_url + path, ...)
  ▼
api.wxorder.taover.com              # Server
```

### Key Design Principles

1. **Root `conftest.py` is enterprise-agnostic** — only contains framework-level fixtures (failure snapshots).
2. **Each enterprise owns its `api_client` fixture** — defined in `tests/<enterprise>/conftest.py`.
3. **Auth is a pluggable interface** — `AuthProvider` ABC; `OctopusAuth` is just one implementation.
4. **All configuration via environment variables** — no hard-coded URLs or credentials.

## Adding a New Enterprise

Suppose you need to test "AliCloud" APIs:

### Step 1: Create integration layer

```
integrations/alicloud/
├── __init__.py
├── api_client.py      # class AliCloudClient(BaseApiClient)
├── auth.py            # class AliCloudAuth(AuthProvider)
└── error_code.py
```

`integrations/alicloud/auth.py`:

```python
import os
from integrations.auth_provider import AuthProvider

class AliCloudAuth(AuthProvider):
    def get_token(self, force_refresh=False):
        return os.getenv("ALICLOUD_ACCESS_TOKEN", "")

    def is_valid(self):
        return bool(self._get_cached_token())
```

`integrations/alicloud/api_client.py`:

```python
from base.base_api_client import BaseApiClient
from config.global_config import TIMEOUT

class AliCloudClient(BaseApiClient):
    def __init__(self, base_url: str, timeout: int = None):
        super().__init__(base_url=base_url, timeout=timeout or TIMEOUT)

    def set_access_token(self, token: str):
        self.set_header("Authorization", f"Bearer {token}")
```

### Step 2: Create service layer

```
services/alicloud/
├── __init__.py
└── ecs_service.py
```

### Step 3: Create test fixtures

```
tests/test_AliCloud/
├── __init__.py
├── conftest.py
└── test_ecs.py
```

### Step 4: Add credentials to `.env`

```env
ALICLOUD_BASE_URL=https://ecs.aliyun.com
ALICLOUD_ACCESS_TOKEN=your_token
```

**No framework files (`base/`, `common/`, `config/`, root `conftest.py`) need any changes.**

## Adding a New Module (Copycat Pattern)

Using "Channel" as an example, each module needs only 2 files:

**1. `services/octopus/channel_service.py` (API encapsulation):**

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

**2. `tests/test_octopus/test_channel_flow.py` (test case):**

```python
from services.octopus.channel_service import ChannelService

class TestChannel:
    def test_channel_flow(self, api_client):
        service = ChannelService(api_client)

        add_res = service.add(name="test_channel")
        assert add_res.get("code") == "ok"

        search_res = service.search(name="test_channel")
        assert search_res.get("code") == "ok"

        channel_id = search_res["data"]["rows"][0]["id"]
        del_res = service.delete(channel_id)
        assert del_res.get("code") == "ok"
```

## CI/CD

### GitHub Actions

Configure these secrets in GitHub `Settings → Secrets and variables → Actions`:

| Secret | Description |
|--------|-------------|
| `OCTOPUS_TOKEN` | Octopus JWT Token (required) |
| `WECOM_CORP_ID` | WeCom Corp ID |
| `WECOM_CONTACT_SECRET` | WeCom Contact Secret |
| `DING_WEBHOOK` | DingTalk bot webhook URL |
| `WECOM_WEBHOOK` | WeCom bot webhook URL |

### GitLab CI

Set CI/CD variables in GitLab project `Settings → CI/CD → Variables`:

- `OCTOPUS_TOKEN`
- `WECOM_CORP_ID`
- `WECOM_CONTACT_SECRET`

### Gitee

Add `OCTOPUS_TOKEN` etc. in project settings → Secrets.

## Code Quality

```bash
# Run all pre-commit checks
uv run pre-commit run --all-files

# Format code
uv run black .
uv run isort .
```

## FAQ

### Q: Tests return `not_authorized`?

Your token has expired. Open browser DevTools (F12), copy the new `Authorization: Bearer==xxx` value, and update `OCTOPUS_TOKEN` in `.env`.

### Q: Warehouse test fails with "this group is already in use"?

Each WeChat group can only be bound to one warehouse. `test_warehouse_flow.py` uses a "borrow group" strategy: list all warehouses, delete one to free its group, then reuse that group for the test.

### Q: Order test fails with "Excel file is being processed"?

Order generation is asynchronous. Wait a minute and re-run, or change the consignee name.

### Q: How do I add a new dependency?

```bash
uv add <package-name>
```

### Q: How do I run tests in parallel?

```bash
uv add pytest-xdist
uv run pytest -n auto
```

## License
