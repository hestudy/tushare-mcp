# External APIs
- **Purpose:** tushare 官方 API，提供行情、财务等数据。
- **Documentation:** https://tushare.pro/document/2
- **Base URL(s):** `https://api.tushare.pro`
- **Authentication:** Header `{"token": "<user_token>"}`，由 `Auth & Secrets Manager` 注入。
- **Rate Limits:** 单 Token 每分钟约 200 次调用；需结合接口公告调整。
- **Key Endpoints:** `daily_basic`, `income`, `stock_basic`, `trade_cal`（全部通过 POST `/` 调用）。
- **Integration Notes:** 统一请求格式，需处理分页参数、错误码映射、限频退避；响应为 `fields` + `items` 结构。
