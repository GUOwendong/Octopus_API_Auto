# Interface Automation Framework

A lightweight, extensible, multi-enterprise API automation framework. Clone, configure, and run — zero adaptation to your own business.

[中文文档](README_zh.md)

## Features

- **Multi-Enterprise Ready** — Pluggable `AuthProvider` and `ApiClient`; no framework code changes needed when switching enterprises.
- **Layered Architecture** — `base` (HTTP client) → `integrations` (auth + API client) → `services` (business logic) → `tests` (test cases).
- **Data-Driven** — Supports JSON / YAML / Excel test data; `pytest.mark.parametrize` integration.
- **Allure Reports** — Built-in Allure integration with automatic report generation.
- **CI/CD** — Pre-configured pipelines for GitHub Actions, GitLab CI, and Gitee.
- **Code Quality** — `black` + `isort` + `pre-commit` hooks out of the box.
- **Failure Snapshots** — Automatic snapshot saved when a test fails, for fast triage.

## Tech Stack

| Tool | Version |
|------|---------|
| Python | >= 3.13 |
| uv | latest |
| pytest | >= 9.0 |
| requests | >= 2.34 |
| Allure | >= 2.16 (pytest plugin) |
| loguru | >= 0.7 |
| openpyxl / pandas | for Excel data |
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

```bash
# Copy the template and fill in your values
cp .env.example .env
```

Edit `.env`:

```env
# Environment: dev / test / prod
TEST_ENV=test

# API base URLs per environment
API_BASE_URL_DEV=http://127.0.0.1:8000
API_BASE_URL_TEST=http://127.0.0.1:8000
API_BASE_URL_PROD=http://127.0.0.1:8000

# Timeout (seconds)
API_TIMEOUT=30

# Enterprise-specific credentials (example: WeCom)
WECOM_BASE_URL=https://qyapi.weixin.qq.com
WECOM_CORP_ID=your_corp_id
WECOM_CONTACT_SECRET=your_secret
```

### 4. Run Tests

```bash
# Run all tests
uv run pytest

# Run tests for a specific environment
uv run python main.py -e test

# Run with markers
uv run pytest -m smoke

# Run a specific test file
uv run pytest tests/test_Wecom/test_create_department.py -v
```

### 5. View Report

```bash
# Generate Allure report
uv run python main.py -e test

# Open report
allure open reports/allure-report
```

Or start a local server:

```bash
cd reports/allure-report && python -m http.server 8080
```

## Project Structure

```
.
├── base/                        # Framework core (zero business logic)
│   └── base_api_client.py       #   Generic HTTP client base class
├── common/                      # Shared utilities
│   ├── file_utils.py            #   Excel / JSON / YAML reader & writer
│   └── log_utils.py             #   loguru-based logging
├── config/
│   └── global_config.py         #   Paths, env, API URLs (env-var driven)
├── integrations/                # External system integrations
│   ├── auth_provider.py         #   AuthProvider ABC + StaticTokenAuth
│   └── wecom/                   #   WeCom integration (example)
│       ├── api_client.py        #     WeCom-specific HTTP client
│       ├── wecom_token.py       #     Token manager (implements AuthProvider)
│       └── wecom_error_code.py  #     Error code mapping
├── services/                    # Business service layer
│   └── wecom/
│       └── department_service.py #   WeCom department CRUD
├── tests/                       # Test cases
│   └── test_Wecom/
│       ├── conftest.py          #   WeCom fixtures (api_client, dept_service)
│       ├── test_create_department.py
│       ├── test_update_department.py
│       ├── test_delete_department.py
│       └── test_depart_manager.py
├── data/                        # Test data
│   ├── xlsx/                    #   Excel test data
│   └── yaml/                    #   YAML test data
├── .env.example                 # Environment variable template
├── conftest.py                  # Global pytest fixtures (framework-level)
├── main.py                      # CLI entry point (env switching + Allure)
├── pyproject.toml               # Project config & dependencies
└── uv.lock                      # Locked dependency versions
```

## Architecture

```
┌──────────────────────────────────────────────────┐
│                    tests/                         │
│   conftest.py → api_client fixture                │
│   (per enterprise, per module)                    │
└────────────────────┬─────────────────────────────┘
                     │ depends on
┌────────────────────▼─────────────────────────────┐
│                  services/                        │
│   Business logic, calls integrations.ApiClient    │
└────────────────────┬─────────────────────────────┘
                     │ depends on
┌────────────────────▼─────────────────────────────┐
│               integrations/                       │
│   ├── auth_provider.py    (AuthProvider ABC)      │
│   └── <enterprise>/                                │
│       ├── api_client.py   (extends BaseApiClient) │
│       ├── auth.py         (extends AuthProvider)  │
│       └── error_code.py                           │
└────────────────────┬─────────────────────────────┘
                     │ depends on
┌────────────────────▼─────────────────────────────┐
│                   base/                           │
│   base_api_client.py  (pure HTTP, no business)    │
└──────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Root `conftest.py` is enterprise-agnostic** — only contains framework-level fixtures (failure snapshots).
2. **Each enterprise owns its `api_client` fixture** — defined in `tests/<enterprise>/conftest.py`.
3. **Auth is a pluggable interface** — `AuthProvider` ABC; WeCom's `WeComTokenManager` is one implementation.
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
        # Your auth logic here
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

`tests/test_AliCloud/conftest.py`:

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

### Step 4: Add credentials to `.env`

```env
ALICLOUD_BASE_URL=https://ecs.aliyun.com
ALICLOUD_ACCESS_TOKEN=your_token
```

**No framework files (`base/`, `common/`, `config/`, root `conftest.py`) need any changes.**

## Running with Markers

```bash
# Smoke tests only
uv run pytest -m smoke

# Regression tests
uv run pytest -m regression

# Tests for a specific enterprise
uv run pytest -m wecom

# Combine markers
uv run pytest -m "smoke and wecom"
```

## Running Failed Tests Only

```bash
uv run pytest --lf       # last failed
uv run pytest --ff       # first failed, then rest
```

## Rerun Flaky Tests

```bash
uv run pytest --reruns 2 --reruns-delay 1
```

## CI/CD

### GitHub Actions

Push to `main` or create a PR. Pipeline steps:
1. Install uv + dependencies
2. Run pytest with Allure results
3. Generate Allure HTML report
4. Upload report artifact
5. Deploy to GitHub Pages
6. Send notifications (DingTalk / WeCom / Email)

Configure these GitHub Secrets:

| Secret | Description |
|--------|-------------|
| `WECOM_CORP_ID` | WeCom Corp ID |
| `WECOM_CONTACT_SECRET` | WeCom Contact Secret |
| `DING_WEBHOOK` | DingTalk bot webhook URL |
| `WECOM_WEBHOOK` | WeCom bot webhook URL |
| `MAIL_USERNAME` | SMTP username |
| `MAIL_PASSWORD` | SMTP password |
| `MAIL_TO` | Recipient email |

### GitLab CI

`.gitlab-ci.yaml` is pre-configured. Set CI/CD variables in GitLab project settings:

- `WECOM_CORP_ID`
- `WECOM_CONTACT_SECRET`

### Gitee

`.gitee/workflows/ci.yaml` is pre-configured.

## Code Quality

```bash
# Run all pre-commit checks
uv run pre-commit run --all-files

# Format code
uv run black .
uv run isort .

# Lint
uv run flake8 .
```

## FAQ

### Q: How do I add a new dependency?

```bash
uv add <package-name>
```

This updates both `pyproject.toml` and `uv.lock`.

### Q: How do I change Python version?

Edit `requires-python` in `pyproject.toml`, then run:

```bash
uv sync
```

### Q: Allure command not found?

```bash
# macOS
brew install allure

# Linux (manual)
wget -qO allure.tgz https://github.com/allure-framework/allure2/releases/download/2.39.0/allure-2.39.0.tgz
tar -zxf allure.tgz
sudo mv allure-2.39.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure
```

### Q: How do I run tests in parallel?

```bash
uv add pytest-xdist
uv run pytest -n auto
```

### Q: Does the framework support gRPC / WebSocket?

No — it's designed for RESTful HTTP APIs. You can extend `base_api_client.py` for other protocols.

## License

Internal use.
