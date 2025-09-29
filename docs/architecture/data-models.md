# Data Models

## `DataSource`
- **Purpose:** 描述 tushare 数据源、认证、限频策略。
- **Key Attributes:** `source_id`, `name`, `rate_limit`, `auth_required`。
- **Relationships:** 1 对多 `InterfaceMetadata`、1 对多 `RateLimitPolicy`（逻辑层面）。

## `InterfaceMetadata`
- **Purpose:** 存储接口参数、字段、频率描述，为 MCP 指令生成提供核心输入。
- **Key Attributes:** `interface_name`, `parameters`, `response_fields`, `throttle_hint`。
- **Relationships:** 多对一 `DataSource`; 一对多 `CommandTemplate`; 一对多 `FieldAliasRule`。

## `CommandTemplate`
- **Purpose:** 表示基于元数据生成的 MCP 指令模板。
- **Key Attributes:** `command_id`, `metadata_ref`, `parameter_schema`, `execution_profile`。
- **Relationships:** 多对一 `InterfaceMetadata`; 一对多 `CommandVersion`; 一对多 `ExecutionLog`。

## `ExecutionLog`
- **Purpose:** 记录每次执行的上下文、耗时、重试和错误信息。
- **Key Attributes:** `request_id`, `command_id`, `status`, `retry_count`, `duration_ms`, `error_payload`。
- **Relationships:** 多对一 `CommandTemplate`; 多对一 `TokenCredential`。

## `TokenCredential`
- **Purpose:** 管理 tushare Token 的加密存储、轮换与审计。
- **Key Attributes:** `credential_id`, `encrypted_token`, `salt`, `last_rotated_at`, `owner`。
- **Relationships:** 一对多 `ExecutionLog`; 一对多 `CredentialAudit`。
