# Database Schema

## SQLite (MVP)
```sql
CREATE TABLE data_sources (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rate_limit JSON NOT NULL,
    auth_required BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interface_metadata (
    interface_name TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES data_sources(source_id),
    parameters JSON NOT NULL,
    response_fields JSON NOT NULL,
    throttle_hint TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE command_templates (
    command_id TEXT PRIMARY KEY,
    interface_name TEXT NOT NULL REFERENCES interface_metadata(interface_name),
    parameter_schema JSON NOT NULL,
    execution_profile JSON NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE command_versions (
    command_id TEXT NOT NULL REFERENCES command_templates(command_id),
    version INTEGER NOT NULL,
    changelog TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (command_id, version)
);

CREATE TABLE token_credentials (
    credential_id TEXT PRIMARY KEY,
    encrypted_token BLOB NOT NULL,
    salt BLOB NOT NULL,
    owner TEXT NOT NULL,
    last_rotated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE execution_logs (
    request_id TEXT PRIMARY KEY,
    command_id TEXT NOT NULL REFERENCES command_templates(command_id),
    credential_id TEXT REFERENCES token_credentials(credential_id),
    status TEXT NOT NULL,
    retries INTEGER NOT NULL DEFAULT 0,
    duration_ms INTEGER NOT NULL,
    rate_limit_hits INTEGER NOT NULL DEFAULT 0,
    response_size INTEGER,
    error_payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE credential_audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    credential_id TEXT NOT NULL REFERENCES token_credentials(credential_id),
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    meta JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE field_alias_rules (
    alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
    interface_name TEXT NOT NULL REFERENCES interface_metadata(interface_name),
    field_name TEXT NOT NULL,
    alias TEXT NOT NULL,
    locale TEXT DEFAULT 'zh-CN'
);
```

## PostgreSQL 扩展建议
- 使用 `UUID` 类型替换文本主键，并启用 `JSONB` 字段及 GIN 索引。
- 对 `execution_logs` 按月份分区以降低历史查询成本。
- 为 `command_templates(interface_name, is_active)`、`execution_logs(status, command_id)` 添加复合索引。
- 引入 Materialized View 缓存常用指令列表，提升查询性能。
