# Test Strategy and Standards

## Testing Philosophy
- **Approach:** 单元测试优先 + 关键路径集成测试 + 定期端到端验证。
- **Coverage Goals:** 单元 ≥85%，关键模块 ≥90%，集成覆盖核心接口，端到端验证成功/失败路径。
- **Test Pyramid:** Unit → Integration → E2E，匹配量化场景需求。

## Test Types and Organization
- **单元测试：** pytest + pytest-asyncio，命名 `test_<module>.py`，位于 `service/tests/unit/`，全局覆盖公共函数。
- **集成测试：** FastAPI + SQLite + Mock tushare，位于 `service/tests/integration/`，使用 WireMock/httpx MockTransport。
- **端到端测试：** pytest + Typer CLI runner，运行于 docker-compose 环境，验证 CLI→API→tushare 模拟链路。

## Test Data Management
- **Strategy:** 版本化 fixtures（JSON/YAML）存于 `service/tests/fixtures/`。
- **Fixtures:** 包含行情分页、错误响应、元数据样本。
- **Factories:** 使用 `factory-boy` 构造 CommandTemplate/ExecutionLog。
- **Cleanup:** 测试结束清理临时数据库，集成/E2E 使用上下文管理器自动删除。

## Continuous Testing
- **CI Integration:** GitHub Actions（Lint → Unit → Integration → E2E），失败阻塞合并。
- **Performance Tests:** `pytest-benchmark` + locust（可选）验证 P95 < 1.5s。
- **Security Tests:** `bandit` + `pip-audit`，对 Token 流程编写安全测试脚本。
