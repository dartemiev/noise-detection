import logging
import time
from os import path

from requests import RequestException

from config.parser import AppConfigParser
from detectors import get_detector, Detectors
from util.logger import init_logging

init_logging()
logger = logging.getLogger()

if __name__ == "__main__":
	logger.info("Application runs...")

	config = AppConfigParser()
	config.parse(path.join(path.dirname(__file__), "config.ini"))

	detector = get_detector(Detectors.SENSOR, config)
	while True:
		try:
			print("DETECTED DATA = {}".format(detector.detect()))
			# response = requests.post(config.storage_url + "/noise/register", data={"level": detector.detect()})
			# if response.status_code != codes.ok:
			# 	logger.info(response.text)

			# response = requests.get(config.storage_url + "/noise/all")
			# items = json.loads(response.text)
			# for item in items:
			# 	logger.warn(item)
		except RequestException as error:
			logger.fatal("Server {} is down!".format(config.storage_url))
			logger.fatal(error)

		time.sleep(0.5)
