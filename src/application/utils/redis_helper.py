from redis import Redis

from application import config


class RedisHelper:
    def __init__(self):
        redis_config = config.get("redis")

        self.redis = Redis(host=redis_config.get("host"), port=redis_config.get("port"))

    async def revoke_token(self, jti: str, expire: int) -> bool:
        return self.redis.set(jti, "", ex=expire)

    def check_revoke(self, jti: str) -> bytes:
        return self.redis.get(jti)
