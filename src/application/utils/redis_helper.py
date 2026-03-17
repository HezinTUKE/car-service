import os

from dotenv import load_dotenv
from redis import Redis

load_dotenv()


class RedisHelper:
    def __init__(self):

        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        db = int(os.getenv("REDIS_DB", 0))

        self.token_expiration = int(os.getenv("REDIS_TOKEN_EXPIRATION", 3600))

        self.redis = Redis(host=host, port=port, db=db)

    def revoke_token(self, jti: str):
        self.redis.set(jti, "", ex=self.token_expiration)

    def check_revoke(self, jti: str) -> bool:
        revoked_token = self.redis.get(jti)
        if revoked_token:
            return True
        return False
