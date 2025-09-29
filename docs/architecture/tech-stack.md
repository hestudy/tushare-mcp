# Tech Stack

## Cloud Infrastructure
- **自托管（推荐）：** macOS/Linux 本地部署 + Docker 化，后续可迁移至 Kubernetes。
- **AWS（备选）：** EKS/Lambda + API Gateway，享受托管监控与 Secrets Manager。
- **阿里云（备选）：** ACK 或函数计算，贴近国内量化团队习惯。

## Technology Selection Table
| Category           | Technology                | Version    | Purpose                                   | Rationale |
|--------------------|---------------------------|------------|-------------------------------------------|-----------|
| Language           | Python                    | 3.11.8     | 后端主语言                               | 性能提升、兼容 tushare SDK |
| Runtime            | uvicorn + gunicorn        | 0.30 / 22.0| 异步服务运行时                           | 多进程 + asyncio 保证吞吐 |
| Web Framework      | FastAPI                   | 0.111      | 构建 REST API 与校验                      | 类型提示友好、async 支持强 |
| Async Toolkit      | anyio                     | 4.x        | 协程协调                                 | 提供统一异步接口 |
| Storage            | SQLite (MVP) / PostgreSQL | 3.45 / 16  | 元数据与日志存储                         | 轻量起步，可平滑升级 |
| ORM                | SQLModel                  | 0.0.16     | 数据层抽象                               | 结合 Pydantic 与 SQLAlchemy |
| HTTP 客户端        | httpx                     | 0.27       | tushare 调用                             | 支持 async/同步双模式 |
| Validation         | Pydantic                  | 2.8        | 模型验证与序列化                         | 与 FastAPI 深度集成 |
| Authentication     | cryptography (Fernet)     | 42.x       | Token 加密                               | 满足本地安全需求 |
| Logging            | structlog + OpenTelemetry | 24.1 / 1.25| 结构化日志与指标                         | 满足观测性与追踪需求 |
| Testing            | pytest + pytest-asyncio   | 8.3 / 0.23 | 单元与集成测试                           | 覆盖 async 场景 |
| CLI 框架           | Typer                     | 0.12       | 构建命令行工具                           | 简洁、类型安全 |
| 文档生成           | MkDocs + material         | 1.6        | 指令文档与架构文档                       | 易于发布与维护 |
| 容器化             | Docker + docker-compose   | 27 / 2.28  | 本地与 PoC 部署                         | 社区成熟、易于协作 |
