import logging
import time

from requests import RequestException

from detectors import get_detector, Detectors
from logger import init_logging
from parsers import AppConfigParser

init_logging()
logger = logging.getLogger()

if __name__ == "__main__":
	logger.info("Application runs...")

	config = AppConfigParser()
	config.parse()

	# detector = get_detector(Detectors.SENSOR, config)
	detector = get_detector(Detectors.RANDOM, config)
	while True:
		try:
			print(detector.detect())
			# response = requests.post(config.storage_url + "/noise/register", data={"level": detector.detect()})
			# if response.status_code != codes.ok:
			# 	logger.info(response.text)

			# response = requests.get(config.storage_url + "/noise/all")
			# items = json.loads(response.text)
			# for item in items:
			# 	logger.warn(item)
		except RequestException as error:
			logger.fatal("Server {0} is down!".format(config.storage_url))
			logger.fatal(error)

		time.sleep(1)
