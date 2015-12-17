import logging
import sys
import time

import requests
from requests import codes, RequestException

from detector import NoiseDetector
from logger import init_logging
from parsers import AppArgumentsParser

init_logging()
logger = logging.getLogger()

if __name__ == "__main__":
	logger.info("Application runs...")

	config = AppArgumentsParser()
	config.parse(sys.argv[1:])
	logger.info(config.storage_url)

	detector = NoiseDetector()
	while True:
		try:
			response = requests.post(config.storage_url + "/noise/register", data={"level": detector.detect()})
			if response.status_code != codes.ok:
				logger.info(response.text)

			# response = requests.get(config.storage_url + "/noise/all")
			# items = json.loads(response.text)
			# for item in items:
			# 	logger.warn(item)
		except RequestException as error:
			logger.fatal("Server {0} is down!".format(config.storage_url))
			logger.fatal(error)

		time.sleep(5)
