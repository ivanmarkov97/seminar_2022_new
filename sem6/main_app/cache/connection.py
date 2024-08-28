import json

import redis
from loguru import logger


class RedisCache:

	def __init__(self, config):
		self.config = config
		self.conn = self._connect()

	def _connect(self):
		return redis.Redis(**self.config)

	def update_connect_if_need(self):
		try:
			_ = self.conn.ping()
		except redis.ConnectionError:
			self.conn = self._connect()

	def set_value(self, name, value, ttl=0):
		try:
			self.conn.set(name=name, value=json.dumps(value))
			if ttl > 0:
				self.conn.expire(name, ttl)
			return True
		except redis.DataError as e:
			logger.error(f"error while setting key-value: {str(e)}")
			return False

	def get_value(self, name):
		value = self.conn.get(name)
		if value:
			return json.loads(value)
		return None
