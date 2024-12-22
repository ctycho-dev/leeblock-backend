from redis import Redis, ConnectionError
from app.config.config import settings
from tenacity import retry, wait_fixed, stop_after_delay


redis_client = Redis(host=settings.redis_host, port=settings.redis_port)


@retry(wait=wait_fixed(2), stop=stop_after_delay(30), reraise=True)
def connect_to_redis():
    """Ensure the Redis client can connect."""
    redis_client.ping()
    return redis_client


def get_redis_client():
    """Get Redis client with a retry mechanism."""
    try:
        return connect_to_redis()
    except ConnectionError as e:
        raise RuntimeError(f"Could not connect to Redis: {e}") from e
