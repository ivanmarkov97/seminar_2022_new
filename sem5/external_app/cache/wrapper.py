from functools import wraps

from cache.connection import RedisCache


def fetch_from_cache(cache_name, cache_config):

	cache = RedisCache(cache_config['redis'])
	ttl = cache_config['ttl']

	def wrapper_func(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			cache.update_connect_if_need()
			cached_value = cache.get_value(cache_name)
			if cached_value:
				print('value from cache')
				return cached_value
			print('original value')
			response = func(*args, **kwargs)
			cache.set_value(cache_name, response, ttl=ttl)
			return response
		return wrapper
	return wrapper_func
