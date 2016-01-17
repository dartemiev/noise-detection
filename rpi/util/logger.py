import logging
import sys
from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
from os import path


def init_logging():
	"""
	Setup logging system to display user-friendly output of execution of the script
	It may help easy find issues which can happens by executing script.
	By default 2 logger are active - console (for debugging purpose only) and to file
	(for production execution to see potential issues)
	"""
	formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")

	console = StreamHandler(sys.stdout)
	console.setFormatter(formatter)

	file = RotatingFileHandler(path.join(path.dirname(__file__), "all_logs.log"), maxBytes=5242880, backupCount=5)
	file.setFormatter(formatter)

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	logger.addHandler(console)
	logger.addHandler(file)
