from typing import Callable, Any
from functools import wraps

from cache.connection import RedisCache


def fetch_from_cache(cache_name, cache_config):

	cache: RedisCache = RedisCache(cache_config['redis'])
	ttl: int = cache_config['ttl']

	def wrapper_func(func: Callable) -> Callable:
		@wraps(func)
		def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
			cache.update_connect_if_need()
			cached_value: str = cache.get_value(cache_name)
			if cached_value:
				return cached_value
			response: Any = func(*args, **kwargs)
			cache.set_value(cache_name, response, ttl=ttl)
			return response
		return wrapper
	return wrapper_func
