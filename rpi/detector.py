import logging
import random

logger = logging.getLogger()


class NoiseDetector(object):
	def detect(self) -> float:
		return random.random()
