from redis import asyncio as aioredis
from redis import Redis
from datetime import datetime

redis: Redis = None


async def get_redis() -> Redis:
    global redis
    if redis is None:
        redis = await aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    return redis


async def increment_promo_count(user_id: int):
    redis = await get_redis()
    current_month = datetime.now().strftime("%Y-%m")  # 2025-05
    key = f"user:{user_id}:promos:{current_month}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 31*24*60*60)  # Maksimal 31 kun TTL
    return count

async def get_promo_count(user_id: int):
    redis = await get_redis()
    current_month = datetime.now().strftime("%Y-%m")
    key = f"user:{user_id}:promos:{current_month}"
    count = await redis.get(key)
    return int(count) if count else 0
