# High Level Architecture

## Technical Summary
`tushare MCP Service` 采用分层单体架构，FastAPI/uvicorn 作为入口，将业务拆分为元数据管线、指令生成、调用代理与观测性模块。核心流程包括解析 tushare SDK、批量生成 MCP 指令、在运行时协调限频分页与日志记录，并统一返回结构化响应。该架构与 PRD 中的 Monorepo、Python 技术假设一致，确保在单体内高效协作并为后续扩展提供清晰边界。

## High Level Overview
- **架构风格：** 分层单体结构，内部按“元数据 → 指令生成 → 调用代理 → 观测性”划分，满足快速迭代需求。
- **仓库结构：** Monorepo，目录涵盖 `metadata/`、`mcp_commands/`、`service/`、`docs/` 等，便于统一管理。
- **服务架构决策：** 单体内部模块化，减少微服务带来的运维复杂度，并保留未来拆分空间。
- **主要数据流：** CLI/IDE 用户发起请求 → 认证模块解密 Token → 调用代理执行 tushare → 限频/分页策略保障稳定 → 日志与监控记录指标 → 返回标准化响应。
- **关键决策：** 选用 FastAPI + Python 3.11 以获得类型化与 async 体验；使用 SQLite/JSON 起步，未来平滑升级 PostgreSQL；统一日志/监控钩子满足可观测性要求。

## High Level Project Diagram
```mermaid
graph TD
    subgraph CLI/IDE Client
        UserRequests
    end

    subgraph MCP Backend (FastAPI Monolith)
        Auth[Auth & Secrets Manager]
        MetadataRepo[Metadata Repository]
        CmdGenerator[MCP Command Generator]
        Orchestrator[Execution Orchestrator]
        Pagination[Pagination & Rate Limit Adapter]
        Logger[Logging & Metrics]
    end

    Tushare[tushare SDK & API]
    Storage[(SQLite/JSON Metadata Store)]
    MetricsSink[(Observability / Metrics Exporter)]

    UserRequests --> Auth
    Auth --> Orchestrator
    Orchestrator --> MetadataRepo
    MetadataRepo --> CmdGenerator
    CmdGenerator --> Orchestrator
    Orchestrator --> Pagination
    Pagination --> Tushare
    Tushare --> Pagination
    Pagination --> Orchestrator
    Orchestrator --> Logger
    Logger --> MetricsSink
    MetadataRepo --> Storage
    Storage --> MetadataRepo
```

## Architectural and Design Patterns
- **分层架构 (Layered Architecture)：** 在单体内按表示层、应用层、领域层、基础设施层划分，保证职责清晰。
- **仓储模式 (Repository Pattern)：** 为元数据、指令配置与日志提供数据访问抽象，便于迁移不同存储。
- **命令模式 + 模板方法：** MCP 指令生成与执行代理通过命令对象和模板流程保持一致性。
- **重试与限频策略：** 结合指数量身定制的退避算法与熔断机制，提升高频调用稳定性。
- **请求追踪 (Correlation ID)：** 全链路保留请求 ID，支持日志与响应对齐，便于排障。
