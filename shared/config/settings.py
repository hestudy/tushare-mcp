"""应用设置与凭证钩子。

该模块提供统一的配置入口，并通过环境变量或后续密钥管理方案
注入 tushare Token，避免将敏感信息硬编码到仓库中。
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """项目通用配置。"""

    environment: str = "development"
    tushare_token: Optional[str] = None
    api_key: Optional[str] = None
    rate_limit_per_minute: Optional[int] = 60

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """缓存并返回应用设置实例。"""

    return AppSettings()


def get_tushare_token() -> Optional[str]:
    """提供 tushare Token 读取钩子，若未配置则返回 None。"""

    return get_settings().tushare_token


def reset_settings_cache() -> None:
    """清空设置缓存，便于测试在修改环境变量后重新加载。"""

    get_settings.cache_clear()
