# Security

## Input Validation
- **Library:** Pydantic 2.8。
- **Location:** FastAPI 路由 + Orchestrator 二次校验。
- **规则：** 外部输入需通过 Schema 校验，使用白名单方式控制参数范围。

## Authentication & Authorization
- **方法：** Token 基于 `Auth & Secrets Manager` 加密存储，执行时解密。
- **会话管理：** 每次请求生成短期 session（`request_id` + `credential_id`），可选轻量 API Key 区分调用者。
- **要求：** Token 缺失返回 `AUTH-001`；CLI/REST 可使用 `X-MCP-Token` 头区分凭证。

## Secrets Management
- **开发环境：** `.env` + `python-dotenv` 提供密钥，Token 加密存储。
- **生产环境：** 借助 Vault/AWS Secrets Manager 管理主密钥。
- **代码要求：** 禁止输出明文 Token，仅通过配置服务访问密钥。

## API Security
- **限频：** Rate Limit Adapter 管理 Token 级窗口，记录命中次数。
- **CORS：** 默认拒绝跨域，若引入 Web 控制台再配置白名单。
- **安全头：** `HSTS`、`X-Content-Type-Options`、`X-Frame-Options` 等；远程环境必须使用 HTTPS。

## Data Protection
- **静态加密：** 数据库磁盘加密；Token 字段使用 Fernet。
- **传输加密：** 客户端与 tushare 均使用 TLS。
- **PII 处理：** 当前无 PII；如后续引入需记录敏感性与访问控制。
- **日志限制：** 禁止记录 Token/原始请求体，敏感字段需脱敏。

## Dependency Security
- **扫描工具:** `pip-audit` + `safety`。
- **更新策略:** 关键依赖每月审查，安全公告触发立即升级。
- **审批流程:** 新依赖需在 PR 中说明用途与风险，获批后合并。

## Security Testing
- **SAST:** `bandit`。
- **DAST:** OWASP ZAP/Nikto（阶段性）。
- **渗透测试:** MVP 后安排内部测试，重点关注认证、限频与日志泄露。
