from typing import Optional

from pydantic import BaseSettings, RedisDsn, AnyHttpUrl


class Settings(BaseSettings):
    base_path: str
    redis_path: RedisDsn
    endpoint_url: Optional[AnyHttpUrl] = None
    bucket_name: str
    debug: Optional[bool] = False


settings = Settings()
