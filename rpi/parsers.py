from configparser import ConfigParser
from os import path

from data import Storage


class AppConfigParser(object):
	"""
	Parser for configuration file which contains all needed setting and data for normal
	application start and collection data. This config provides settings all over the
	application.
	"""
	def __init__(self):
		super().__init__()
		self.__active_pin = -1
		self.__storage = Storage
		self.__config = ConfigParser()

	def parse(self):
		"""
		Reads configuration file (config.ini) which contains all settings for application
		by different sections like: Storage, GPIO, etc.
		"""
		self.__config.read(path.join(path.dirname(__file__), "config.ini"))
		# read all properties from configuration file
		self.__storage.interval = self.__config.get("Storage", "interval")
		self.__storage.url = self.__config.get("Storage", "url")
		self.__active_pin = self.__config.get("GPIO", "active_pin")
		# validate all properties before actual collecting execution
		self.__validate()

	@property
	def storage_url(self) -> str:
		"""
		The url to web service which provides public API for tracking data received
		from RPi and sensor (microphone) to detect noise level in the room and build
		dashboard, analysing noise by thresholds, etc.
		:return: The url to web storage as string (e.g. http://localhost:3000)
		:func:`Storage.url`
		"""
		return self.__storage.url

	@property
	def storage_interval(self) -> int:
		"""
		The amount of milliseconds between every storage phase - sending data to public
		web service defined by :func:`AppArgumentsParser.storage_url`
		:return: The amount of milliseconds between every storage phase
		"""
		return self.__storage.interval

	@property
	def active_pin(self) -> int:
		"""
		Active PIN on PRi board to which sensor (microphone) is connected. By this PIN
		data will be gathered and than depends on conditions and rules stored/processed/
		analyzed/etc.
		:return: The number of PIN on RPi board
		"""
		return self.__active_pin

	def __validate(self):
		assert self.storage_interval is not None and self.storage_interval is not 0
		assert self.storage_url is not None and len(self.storage_url) is not 0
		assert self.active_pin is not None and self.active_pin is not -1
