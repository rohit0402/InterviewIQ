import json
from typing import Any
from redis.exceptions import RedisError
from app.core.redis import redis_client


class CacheService:
    DEFAULT_TTL = 300  # 5 minutes

    @staticmethod
    def get(key: str):
        try:
            value = redis_client.get(key)
            return json.loads(value) if value else None
        except RedisError:
            return None

    @staticmethod
    def set(
        key: str,
        value: Any,
        ttl: int = DEFAULT_TTL,
    ):
        try:
            redis_client.set(
    key,
    json.dumps(value),
    ex=ttl,
)
        except RedisError:
            pass

    @staticmethod
    def delete(key: str):
        try:
            redis_client.delete(key)
        except RedisError:
            pass

    @staticmethod
    def exists(key: str):
        try:
            return redis_client.exists(key)
        except RedisError:
            return False
    @staticmethod
    def ttl(key: str):
        try:
            return redis_client.ttl(key)
        except RedisError:
            return -1