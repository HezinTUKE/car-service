from redis import Redis

from application import config


class RedisHelper:
    def __init__(self):
        redis_config = config.get("redis")

        client = Redis(
            host=redis_config.get("host"),
            port=redis_config.get("port")
        )
