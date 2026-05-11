from redis import Redis

from application.configs import settings


class RedisHelper:
    def __init__(self):
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        db = settings.REDIS_DB

        self.token_expiration = settings.REDIS_TOKEN_EXPIRATION

        self.redis = Redis(host=host, port=port, db=db)

    def revoke_token(self, jti: str):
        self.redis.set(jti, "", ex=self.token_expiration)

    def check_revoke(self, jti: str) -> bool:
        revoked_token = self.redis.get(jti)
        if revoked_token:
            return True
        return False
