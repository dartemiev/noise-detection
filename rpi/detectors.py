import logging
import random

from RPi import GPIO

from controllers.MCP3008 import MCP3008
from parsers import AppConfigParser

logger = logging.getLogger()


class Detectors(object):
	SENSOR = 1
	RANDOM = 2


class NoiseDetector(object):
	"""
	Base class for every noise detection implementation.
	"""

	def __init__(self, config: AppConfigParser):
		"""
		:param config: Configuration file (e.g. config.ini) where are all application
		settings
		"""
		assert config is not None

	def detect(self) -> int:
		"""
		Detects and returns level of noise
		:return: Current value of detected noise
		"""
		pass


class SensorDetector(NoiseDetector):
	"""
	An implementation for real sensor (microphone) connected to RPi
	"""
	__doc__ = NoiseDetector.__doc__

	def __init__(self, config: AppConfigParser):
		super().__init__(config)
		self.__pin = config.active_pin

		logger.info("RPi listens pin {0} from sensor".format(self.__pin))
		GPIO.setmode(GPIO.BCM)
		self.__adc = MCP3008(pin_clk=7, pin_cs=24, pin_miso=8, pin_mosi=25)

	def detect(self) -> int:
		return self.__adc.read(0)


class RandomDetector(NoiseDetector):
	"""
	An implementation for random value (for testing purpose only)
	"""
	__doc__ = NoiseDetector.__doc__

	def detect(self) -> int:
		result = 0
		for _ in range(10):
			result <<= 1
			if random.random() <= 0.5:
				result |= 0x1
		return result


def get_detector(detector: Detectors, config: AppConfigParser) -> NoiseDetector:
	"""
	Factory method for retrieving noise detector depends on given type and its configuration.
	:param detector: Enum of available noise detector types
	:param config: Application configuration
	:return: New instance of noise detector
	:exception If noise detection is not implemented by given detector type
	"""
	if detector is Detectors.SENSOR:
		return SensorDetector(config)
	elif detector is Detectors.RANDOM:
		return RandomDetector(config)

	raise NotImplemented("No implementation for given detector type (0)".format(detector))
