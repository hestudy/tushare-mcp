# Source Tree
```plaintext
tushare-mcp/
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── commands/
│   │   └── index.md
│   └── qa/
├── metadata/
│   ├── raw/
│   └── normalized/
├── mcp_commands/
│   ├── templates/
│   ├── generated/
│   └── cli/
├── service/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── orchestrator/
│   │   ├── rate_limit/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── security/
│   ├── tasks/
│   │   ├── metadata_ingest.py
│   │   └── command_generate.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   └── scripts/
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── terraform/
│   └── ops/
├── shared/
│   ├── utils/
│   ├── telemetry/
│   └── config/
├── tests/
├── pyproject.toml
├── README.md
└── Makefile
```
