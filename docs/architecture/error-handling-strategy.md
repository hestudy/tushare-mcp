# Error Handling Strategy

## General Approach
- **错误模型：** 定义 `AuthError`、`ParameterError`、`RateLimitError`、`ServiceError`、`UnknownError`，向上层统一映射。
- **异常层级：** FastAPI 捕获 → Orchestrator 分类封装 → 下层限频/仓储抛出具象异常。
- **传播规则：** 所有异常需附带 `request_id`、`command_id` 并写入 `execution_logs`；可重试错误执行退避后再抛出。

## Logging Standards
- **日志库：** structlog 24.1（JSON 格式），OpenTelemetry 1.25 推送指标。
- **固定字段：** `timestamp`, `level`, `request_id`, `command_id`, `event`, `duration_ms`, `retries`。
- **日志级别：** INFO（正常）、WARN（限频/参数矫正）、ERROR（执行失败/SLA 超时）。
- **上下文要求：** Correlation ID 全链路传递；Service Context（service、component）；User Context 记录 owner/credential_id（无明文 Token）。

## Error Handling Patterns
- **外部 API 错误：** 指数退避（500ms 起、最多 3 次）、连续 5 次失败熔断 60 秒、调用超时 3 秒，错误映射为 RATE_LIMIT/SERVICE。
- **业务逻辑错误：** `BusinessRuleError` 提供明确提示，如参数超限；错误码 `AUTH-001`、`PARAM-101`、`RATE-201`、`SERVICE-301`、`UNK-999`。
- **数据一致性：** 解析/生成使用事务，失败回滚；指令生成失败记录失败集合；执行接口支持 `request_id` 幂等。
