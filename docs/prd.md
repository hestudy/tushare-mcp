# tushare MCP Service Product Requirements Document (PRD)

## Goals and Background Context

### Goals
- **G1** 完成 tushare 高频行情与财务接口的 MCP 封装，使量化分析师能通过统一指令快速拉取数据。
- **G2** 将量化团队的数据接入周期缩短 50%，减少重复脚本维护工作。
- **G3** 为至少 3 个 AI 量化项目提供可复用的数据管道实践并验证可行性。
- **G4** 建立稳定的认证、分页与限频处理机制，确保调用链可追踪且易于排错。

### Background Context
- **背景概述**：当前 tushare 官方 Python SDK 缺乏结构化元数据，接口信息散落在文档与示例代码中，造成自动化封装困难。量化研究人员需在脚本中反复实现分页、限频与错误处理逻辑，阻碍策略迭代效率。
- **解决动机**：本项目计划构建元数据仓库并据此自动生成 MCP 指令配置，提供统一认证与错误透传策略，从而为本地 AI 工作流提供可信的数据入口，降低维护成本并提升数据接入稳定性。

### Change Log
| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2025-09-29 | v0.1 | 创建 PRD 初稿结构并填充目标、背景与核心需求 | John (PM) |

## Requirements

### Functional Requirements
1. **FR1**：MCP 服务必须解析 tushare SDK 元数据并生成结构化指令配置，包含参数、字段及频率描述。
2. **FR2**：系统需提供统一的认证模块，允许用户配置 tushare Token 并在调用链中安全透传。
3. **FR3**：MCP 指令执行时需自动处理 tushare 的分页、限频与重试策略，并向上游返回标准化状态。
4. **FR4**：服务端需支持调用日志与错误信息的统一格式输出，5 分钟内可定位问题。
5. **FR5**：提供基本的 CLI/REST 接入层，便于本地 IDE 或脚本调用。

### Non-Functional Requirements
1. **NFR1**：P95 响应时间需控制在 1.5 秒以内，并在限频情况下保证 98% 成功重试率。
2. **NFR2**：解决方案需支持本地部署于 macOS/Linux 环境，可扩展至容器化。
3. **NFR3**：元数据与凭证存储需保证安全，Token 仅在本地加密保存并记录审计日志。
4. **NFR4**：接口变更应能在一个迭代内通过元数据仓库更新并回归测试，保证可维护性。

## User Interface Design Goals

### Overall UX Vision
- 以 CLI 与 IDE 插件的命令式调用为核心，目标是在终端或 IDE 面板中快速检索 MCP 指令、查看元数据说明，并在错误时获得清晰提示。

### Key Interaction Paradigms
- **命令查询与执行**：通过 IDE 命令面板或 CLI 输入 `mcp tushare <command>`，返回参数说明与执行结果。
- **参数引导与校验**：调用时即时提示必填/可选参数，提供默认值或示例，并在参数异常时提供修正建议。
- **状态与错误反馈**：实时输出分页进度、限频重试情况及标准化错误日志，便于排查。

### Core Screens and Views
1. **CLI/IDE 命令执行视图**：展示可用 MCP 指令列表及调用示例。
2. **参数提示面板**：列出参数说明、类型、默认值及限频说明。
3. **调用结果输出区**：以表格或 JSON 呈现数据响应，并包含分页状态。
4. **错误诊断视图**：集中展示错误代码、限频信息和修复建议。

### Accessibility
- 当前交互以命令行与 IDE 插件为主，依赖宿主环境的可访问性能力，暂不额外定制。

### Branding
- 暂无专属品牌规范，沿用 tushare 官方术语体系并保持文档表述一致性。

### Target Device and Platforms
- 支持 macOS/Linux 终端与 VSCode、JetBrains 等主流 IDE，未来可扩展至容器化部署或 Web 控制台。

## Technical Assumptions

### Repository Structure
- 采用 **Monorepo**，统一管理 `metadata/`、`mcp_commands/`、`service/`、`docs/` 等模块，便于协作与 CI/CD。

### Service Architecture
- 采用分层单体架构：以 FastAPI/uvicorn 提供服务接口，内部划分元数据解析、指令生成、调用代理模块，为未来扩展预留接口。

### Testing Requirements
- 实施“单元测试 + 集成测试”策略：核心逻辑编写单元测试，调用链路使用集成测试验证分页、限频与错误透传。

### Additional Technical Assumptions and Requests
- 使用 Python 3.10+ 与 tushare 官方 SDK；数据存储初期使用 SQLite/JSON，随规模升级至 PostgreSQL。
- 认证信息本地加密存储，未来容器化时提供密钥管理接口。
- 集成基础日志与监控钩子，便于后续接入企业监控体系。

## Epic List
- **Epic 1：平台基础与最小可用接口** — 搭建 MCP 服务基础设施并封装首个 tushare 行情接口。
- **Epic 2：元数据管线与批量指令生成** — 构建自动化元数据解析与校验流程，批量生成 MCP 指令配置。
- **Epic 3：稳定性增强与观测性** — 完善分页、限频、错误透传与日志监控，提升高频调用稳定性。

## Epic 1 平台基础与最小可用接口

### Epic Goal
- 建立可运行的 MCP 服务基础设施，确保代码结构、CI/CD 与认证占位完整。
- 封装首个 tushare 行情接口，验证端到端认证、调用、分页与日志链路。

### Story 1.1 项目骨架与持续集成
```
As a 后端工程师,
I want 初始化 MCP 服务仓库与基础框架,
so that 团队可以在统一结构下协作并自动验证提交。
```
- **验收标准**
  1. 配置 Monorepo 结构，包含 `metadata/`、`mcp_commands/`、`service/`、`docs/` 目录。
  2. 引入 FastAPI/uvicorn 并提供基础健康检查路由。
  3. 建立 CI（Lint + Unit Test）流程，PR 合并需自动执行。
  4. 编写 README 说明启动方式与目录结构。

### Story 1.2 认证配置与安全占位
```
As a DevOps 工程师,
I want 建立 tushare Token 的配置与加密存储流程,
so that 用户调用接口时可复用统一认证方案并确保凭证安全。
```
- **验收标准**
  1. 支持从环境变量或配置文件读取 tushare Token。
  2. Token 本地加密存储，并提供解密与轮换钩子。
  3. 调用日志中不得出现明文 Token。
  4. 文档说明 Token 配置步骤与审计策略。

### Story 1.3 首个 MCP 指令封装与调用演示
```
As a AI 量化分析师,
I want 通过 MCP 指令调用示例行情接口,
so that 可以验证端到端流程并快速获取数据样本。
```
- **验收标准**
  1. 选定 tushare 高频行情接口（如 `daily_basic`）并封装为 MCP 指令。
  2. MCP 指令调用 FastAPI 服务并返回 JSON，包含请求 ID。
  3. 处理分页参数并在响应中附带分页状态。
  4. 提供调用示例脚本与 README 演示输出。

## Epic 2 元数据管线与批量指令生成

### Epic Goal
- 构建可持续运转的元数据解析与校验管线，覆盖主流行情/财务接口。
- 基于元数据批量生成 MCP 指令配置，保证参数映射一致并降低维护成本。

### Story 2.1 元数据解析与校验框架
```
As a 数据工程师,
I want 自动解析 tushare SDK 的接口签名与返回字段,
so that 可以得到结构化元数据供指令生成使用。
```
- **验收标准**
  1. 构建解析脚本，输出接口名称、参数、字段、频率限制等结构化数据。
  2. 设计 schema 校验逻辑，缺失或异常字段需产生告警。
  3. 将元数据写入 `metadata/` 并纳入版本控制。
  4. 提供解析流程及扩展方法的文档。

### Story 2.2 MCP 指令模板与批量生成
```
As a 后端工程师,
I want 基于元数据批量生成 MCP 指令配置,
so that 可以快速扩展接口覆盖并保持参数一致性。
```
- **验收标准**
  1. 根据元数据生成标准化 MCP 指令文件，含参数描述、默认值、分页策略。
  2. 字段命名与 tushare SDK 对齐，支持自定义别名。
  3. 在 `mcp_commands/` 输出至少 10 个高频接口配置。
  4. 编写生成脚本的使用说明和参数选项。

### Story 2.3 指令目录与检索体验
```
As a AI 量化分析师,
I want 通过命令或文档快速查找 MCP 指令信息,
so that 可以更高效选择合适接口并了解参数要求。
```
- **验收标准**
  1. 提供 CLI/IDE 指令列出可用接口，支持分类或关键词搜索。
  2. 输出参数说明、限频提示与示例调用片段。
  3. 在 `docs/` 中生成指令目录文档，与 CLI 内容一致。
  4. 支持按接口版本或更新时间过滤。

## Epic 3 稳定性增强与观测性

### Epic Goal
- 完善分页、限频与错误处理机制，提升高频调用稳定性。
- 建立日志和性能指标，确保问题可在 5 分钟内定位。

### Story 3.1 分页与限频适配层
```
As a 后端工程师,
I want 在 MCP 服务端实现分页与限频处理逻辑,
so that 在高频调用下仍能稳定拉取完整数据。
```
- **验收标准**
  1. 支持 tushare 标准分页参数，自动轮询直至数据获取完毕。
  2. 实现限频控制与重试，并记录重试次数。
  3. 响应中包含分页及限频状态描述。
  4. 对超限等异常给出明确错误码与恢复建议。

### Story 3.2 日志与监控指标
```
As a 数据平台工程师,
I want 输出标准化日志与关键性能指标,
so that 能够在 5 分钟内定位调用问题并监控系统健康。
```
- **验收标准**
  1. 统一日志格式，记录请求 ID、接口名称、耗时、重试信息。
  2. 暴露 P95 响应时间、成功率、限频命中次数等基础指标。
  3. 支持本地与容器部署下的日志采集配置。
  4. 提供对接企业监控系统的指南。

### Story 3.3 错误透传与恢复指引
```
As a AI 量化分析师,
I want 获取清晰的错误透传信息与恢复建议,
so that 可以快速排查问题并调整调用策略。
```
- **验收标准**
  1. 定义错误分类（认证失败、参数错误、限频、服务异常等）及消息模板。
  2. 在 CLI/IDE 输出中展示错误原因、建议操作与文档链接。
  3. 对可重试错误自动触发重试并记录日志。
  4. 在文档中维护错误码对照表与诊断流程。

## Checklist Results Report

### Executive Summary
- **整体完整度**：约 82%（5 个类别通过，4 个类别部分达标）
- **MVP 范围评估**：Just Right —— 功能聚焦于元数据管线与稳定性核心需求
- **架构阶段准备度**：Nearly Ready —— 需补充用户流程细节与部分非功能约束
- **关键关注点**：缺少端到端用户流程、数据治理策略与可用性度量，需在进入架构阶段前进一步澄清

### Category Analysis
| Category | Status | Critical Issues |
| --- | --- | --- |
| 1. Problem Definition & Context | PASS | — |
| 2. MVP Scope Definition | PASS | — |
| 3. User Experience Requirements | PARTIAL | 缺少完整用户路径与异常场景说明 |
| 4. Functional Requirements | PASS | — |
| 5. Non-Functional Requirements | PARTIAL | 尚未覆盖可用性/弹性/备份策略 |
| 6. Epic & Story Structure | PASS | — |
| 7. Technical Guidance | PARTIAL | 需补充技术风险与债务控制策略 |
| 8. Cross-Functional Requirements | PARTIAL | 数据治理、集成测试与运维要求待细化 |
| 9. Clarity & Communication | PASS | — |

### Top Issues by Priority
- **BLOCKERS**：暂无
- **HIGH**：
  - 明确关键用户流程（从查找指令至处理错误的端到端步骤），补充边界与回退策略
  - 定义数据保留、备份与容灾要求，保障量化回放使用场景
- **MEDIUM**：
  - 描述监控指标上报路径与告警责任人
  - 补充技术债务处理原则与阶段性评审点
- **LOW**：
  - 提供 CLI/IDE 交互示意或信息架构草图

### MVP Scope Assessment
- **可裁剪项**：当前范围集中于最小可用数据服务，无明显可删功能
- **缺失项**：需新增用户旅程与运维策略文档以支撑 MVP 上线
- **复杂度评估**：Epic 结构合理，但限频与监控可能在资源紧张时成为风险
- **时间预期**：12 周内完成 MVP 可行，但需提前规划限频策略验证与 QA 资源

### Technical Readiness
- 技术约束：已明确语言、架构与部署形态，但密钥管理与日志落地方案需进一步定义
- 技术风险：分页限频实现复杂、元数据解析对 SDK 变更敏感
- 深入研究：建议建筑师评估日志/监控集成、数据存储迁移路径与高频限流方案

### Recommendations
- 在 `docs/` 补充用户操作流程图或文字说明，并扩展错误恢复用例
- 与数据平台团队对齐数据保留、备份与审核政策，形成可执行指引
- 预先制定监控指标上报与告警流程，明确责任人和工具链
- 在技术决策记录中加入潜在技术债务和缓解计划，为后续迭代提供治理框架

### Final Decision
- **NEEDS REFINEMENT** —— 完成上述高优先级补充后，即可进入架构设计阶段

## Next Steps

### UX Expert Prompt
> 使用本 PRD 的 "User Interface Design Goals" 与 "Epic 2/3" 内容，为命令式数据服务设计简洁的交互提示与错误展示策略，并识别潜在的可视化机会。

### Architect Prompt
> 基于本 PRD 中的 "Technical Assumptions"、各 Epic 与 Story 验收标准，输出系统级架构方案，重点考虑元数据管线、分页限频策略与部署扩展性。
