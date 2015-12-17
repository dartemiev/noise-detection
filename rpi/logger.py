import logging
import sys
from os import path


def init_logging():
	"""
	Setup logging system to display user-friendly output of execution of the script
	It may help easy find issues which can happens by executing script
	"""
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

	console = logging.StreamHandler(sys.stdout)
	console.setFormatter(formatter)

	file = logging.FileHandler(path.join(path.dirname(__file__), "all_logs.log"))
	file.setFormatter(formatter)

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	logger.addHandler(console)
	logger.addHandler(file)
