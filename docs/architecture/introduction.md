# Introduction

`tushare MCP Service` 的后端架构文档旨在为 AI 驱动的开发团队提供统一蓝图，指导如何解析 tushare SDK 元数据、封装 MCP 指令并通过 CLI/REST 暴露给量化分析师。方案以分层单体架构为核心，聚焦元数据管线、认证安全、分页限频处理以及观测性，确保满足 PRD 中的业务目标与非功能约束。

## Starter Template or Existing Project
- 项目为绿地（Greenfield），基于 Monorepo 自建结构（`metadata/`、`mcp_commands/`、`service/`、`docs/`）。
- 推荐结合 FastAPI 官方脚手架及 Cookiecutter 作为初始化参考，以加速目录、依赖与测试框架搭建；随后为元数据与 MCP 模块补充自定义结构。
- 如选择完全手工搭建，则需额外投入配置时间，但不影响后续架构设计。

## Change Log
| Date       | Version | Description                         | Author  |
|------------|---------|-------------------------------------|---------|
| 2025-09-29 | v0.1    | 创建 tushare MCP 后端架构文档初稿 | Winston |
