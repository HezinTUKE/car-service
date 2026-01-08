from redis import Redis

from application import config


class RedisHelper:
    def __init__(self):
        redis_config = config.redis
        self.redis = Redis(host=redis_config.host, port=redis_config.port, db=redis_config.db)

    def revoke_token(self, jti: str):
        self.redis.set(jti, "", ex=config.security.token_expire)

    def check_revoke(self, jti: str) -> bool:
        revoked_token = self.redis.get(jti)
        if revoked_token:
            return True
        return False
