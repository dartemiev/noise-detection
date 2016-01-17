import logging
from configparser import ConfigParser

from config.data import Pins, ADCConfig
from data import Storage

logger = logging.getLogger()


class AppConfigParser(object):
	"""
	Parser for configuration file which contains all needed setting and data for normal
	application start and collection data. This config provides settings all over the
	application.
	"""

	def __init__(self):
		super().__init__()
		self.__adc_config = None
		self.__storage = Storage

	@staticmethod
	def __read_adc_pins(config: ConfigParser) -> Pins:
		"""
		Reads configuration for ADC by used pins
		:param config: The content of configuration file (*.ini)
		"""
		miso = config.get("ADC", "MISO")
		mosi = config.get("ADC", "MOSI")
		clk = config.get("ADC", "CLK")
		cs = config.get("ADC", "CS")
		return Pins(miso=int(miso), mosi=int(mosi), clk=int(clk), cs=int(cs))

	def parse(self, file: str) -> None:
		"""
			Reads configuration file (config.ini) which contains all settings for application
			by different sections like: Storage, GPIO, etc.
			:param file:
		"""
		config = ConfigParser()
		config.read(file)

		channel = config.get("ADC", "channel")
		pins = self.__read_adc_pins(config)
		self.__adc_config = ADCConfig(channel=int(channel), pins=pins)

		logger.info("ADC CHANNEL = {}".format(channel))
		logger.info("ADC PINS SETUP:")
		logger.info("    MISO = {}".format(pins.miso))
		logger.info("    MOSI = {}".format(pins.mosi))
		logger.info("    CLK  = {}".format(pins.clk))
		logger.info("    CS   = {}".format(pins.cs))

		# self.__storage.interval = self.__config.get("Storage", "interval")
		# self.__storage.url = self.__config.get("Storage", "url")

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
	def adc(self) -> ADCConfig:
		"""
		Configuration for ADC (pins, channels, setup) to activate read data from sensor as
		analog data and convert it to digital representation to use it in analyzer.
		:return: ADC Configuration
		"""
		return self.__adc_config

	def __validate(self):
		"""
		Validates all properties of configuration file.
		"""
		# assert self.storage_interval is not None and self.storage_interval is not 0
		# assert self.storage_url is not None and len(self.storage_url) is not 0
		assert isinstance(self.adc, ADCConfig) and self.adc is not None
