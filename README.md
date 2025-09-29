# tushare-mcp

基于 FastAPI 的 Tushare MCP 服务骨架，提供统一的命令与元数据处理能力。本仓库遵循 Monorepo 结构，覆盖服务端、命令生成、文档与基础设施配置。

## 目录结构

```plaintext
metadata/            # 原始与归一化元数据占位
mcp_commands/        # MCP 命令模板、生成产物与 CLI 入口
service/             # FastAPI 应用、任务脚本与测试
shared/              # 公共配置、工具与遥测组件
infrastructure/      # Docker、Terraform 与运维脚本
docs/                # PRD、架构、QA 与故事文档
.github/workflows/   # CI 配置
pyproject.toml       # 依赖与工具链声明
Makefile             # 常用开发命令
```

## 快速开始

```bash
# 安装项目依赖（含开发工具）
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

# 运行格式化与静态检查
make lint

# 执行单元测试
make test

# 本地启动服务（默认 0.0.0.0:8000）
make run
```

启动后访问 `GET /health`，可验证服务健康状态与统一响应结构。

## 安全与速率限制

- 设置 `MCP_API_KEY` 环境变量以启用 API Key 校验，默认情况下端点允许未认证访问，便于开发调试。
- 通过 `MCP_RATE_LIMIT_PER_MINUTE` 控制每分钟允许的请求数，默认 60。
- CI 会执行额外的安全配置自检，确保仓库中未硬编码敏感凭证。

## 依赖版本

- Python 3.11.8
- FastAPI 0.111.0
- uvicorn 0.30.0
- httpx 0.27.0
- pytest 8.3.2 / pytest-asyncio 0.23.8
- black 24.8.0
- ruff 0.5.6

## 部署与环境演进

- **本地开发**：默认使用 `uvicorn` + 热重载，可通过 `docker-compose`（后续故事）扩展。
- **容器化**：`infrastructure/docker/` 将存放 Dockerfile 与运行脚本。
- **云端扩展**：保留 `infrastructure/terraform/` 与 `infrastructure/ops/` 目录，以便未来迁移至 Kubernetes / AWS / 阿里云 等环境。

## 功能扩展规划

- `service/app/orchestrator/`：执行指令编排逻辑。
- `service/app/rate_limit/`：封装 Tushare 限频控制器。
- `shared/telemetry/`：对接 OpenTelemetry 与结构化日志。
- `shared/config/`：统一密钥加载与运行时配置（含 Tushare Token 钩子）。
- `mcp_commands/templates/`：MCP 指令模板仓库。

随着后续故事推进，将逐步实现命令生成、调度管线、限频适配与观测指标。
