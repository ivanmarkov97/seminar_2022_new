from functools import wraps
from typing import Callable, Any

from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):

	cache: RedisCache = RedisCache(cache_config['redis'])
	ttl: int = cache_config['ttl']

	def wrapper_func(func: Callable) -> Callable:
		@wraps(func)
		def wrapper(*args, **kwargs) -> Any:
			cached_value = cache.get_value(cache_name)
			if cached_value:
				return cached_value
			response: Any = func(*args, **kwargs)
			cache.set_value(cache_name, response, ttl=ttl)
			return response
		return wrapper
	return wrapper_func
