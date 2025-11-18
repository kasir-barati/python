from functools import lru_cache

from common.config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

print(settings.env)
print(settings.redis.url)
print(settings.rabbitmq_uri)
