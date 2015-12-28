import logging
import random
import time

from RPi import GPIO

from parsers import AppConfigParser

logger = logging.getLogger()


@enumerate
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

	def detect(self) -> float:
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
		# GPIO.setup(self.__pin, GPIO.IN)

	def detect(self) -> float:
		# return GPIO.input(self.__pin)
		return self.__read_analog(self.__pin)

	# Define function to measure charge time
	def __read_analog(self, pin: int) -> int:
		counter = 0
		# Discharge capacitor
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.1)
		GPIO.setup(pin, GPIO.IN)
		# Count loops until voltage across capacitor reads high on GPIO
		while GPIO.input(pin) == GPIO.LOW:
			counter += 1
		return counter


class RandomDetector(NoiseDetector):
	"""
	An implementation for random value (for testing purpose only)
	"""
	__doc__ = NoiseDetector.__doc__

	def detect(self) -> float:
		return random.random()


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
