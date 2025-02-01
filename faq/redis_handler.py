import redis
import json
from django.core.cache import cache
from django.db import transaction

class RedisHandler:
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)

    def get_cache(self, key):
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value 
        return None

    def set_cache(self, key, value, timeout=3600):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.client.setex(key, timeout, value)

    @transaction.atomic
    def set_cache_with_transaction(self, key, value, timeout=3600):
        self.set_cache(key, value, timeout)
