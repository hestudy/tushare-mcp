# Infrastructure and Deployment

## Infrastructure as Code
- **Tool:** Terraform 1.8（需求扩大后启用）。
- **Location:** `infrastructure/terraform/`。
- **Approach:** MVP 阶段使用 docker-compose 管理本地与 PoC，后续以 Terraform 管理容器、数据库与监控资源。

## Deployment Strategy
- **Strategy:** 容器化部署 + 蓝绿发布，PoC 使用 docker-compose，生产预留 K8s/ECS 蓝绿切换。
- **CI/CD Platform:** GitHub Actions → 可迁移 GitLab CI/Jenkins。
- **Pipeline Configuration:** `infrastructure/ops/pipelines/`，阶段为 Lint/Test → Build → Integration → Staging Deploy → Promote to Prod。

## Environments
- **Development:** 本地 docker-compose，FastAPI + SQLite，支持热重载。
- **Staging:** 内部测试环境（Docker Swarm/K8s Namespace） + PostgreSQL，供集成测试与用户试用。
- **Production:** 正式环境，部署于私有或公有云，支持水平扩展、集中式日志与监控。

## Environment Promotion Flow
```text
Developer Branch -> Pull Request (Lint/Test) -> Merge to Main -> Build & Publish Image -> Deploy to Staging -> Smoke & Load Tests -> Manual Approval -> Deploy to Production (Blue/Green) -> Traffic Switch & Monitor
```

## Rollback Strategy
- **Primary Method:** 蓝绿回滚，保留上一版本容器并快速切换流量。
- **Trigger Conditions:** 错误率 > 1%、P95 > 1.5s、关键指令失败、巡检脚本异常。
- **Recovery Time Objective:** < 15 分钟，通过保留旧版镜像与数据库快照实现。
