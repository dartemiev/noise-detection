import logging
import random

from RPi import GPIO

logger = logging.getLogger()


class NoiseDetector(object):
	def __init__(self, active_pin: int):
		super().__init__()
		self.__active_pin = active_pin

		logger.info("RPi listens pin {0} from sensor".format(active_pin))
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(active_pin, GPIO.IN)

	def detect(self) -> float:
		# return GPIO.input(self.__active_pin)
		return random.random()
