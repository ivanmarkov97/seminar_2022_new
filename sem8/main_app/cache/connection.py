import json
from typing import Any

import redis
from loguru import logger


class RedisCache:

	def __init__(self, config: dict) -> None:
		self.config: dict = config
		self.conn: redis.Redis = self._connect()

	def _connect(self) -> redis.Redis:
		return redis.Redis(**self.config)

	def update_connect_if_need(self) -> None:
		try:
			_ = self.conn.ping()
		except redis.ConnectionError:
			self.conn = self._connect()

	def set_value(self, name: str, value: Any, ttl: int = 0) -> bool:
		try:
			self.conn.set(name=name, value=json.dumps(value))
			if ttl > 0:
				self.conn.expire(name, ttl)
			return True
		except redis.DataError as e:
			logger.error(f"error while setting key-value: {str(e)}")
			return False

	def get_value(self, name: Any) -> Any:
		value: str = str(self.conn.get(name))
		if value:
			return json.loads(value)
		return None
