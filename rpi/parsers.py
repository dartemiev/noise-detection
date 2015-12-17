class ArgumentsParser(object):
	"""
	Base class for all application arguments parsing
	"""
	def __init__(self, delimiter: str):
		self.__delimiter = delimiter
		self.__arguments = {}

	def parse(self, arguments: list):
		"""
		Entry point for parsing arguments needed for application
		List aof argument has to be like above

			application.py --path=<path> --output=<output>

		:param arguments: List of params to be parsed (usually it's system params from command line)
		:return: configuration object with all expected arguments
		"""
		assert isinstance(arguments, list)

		for argument in arguments:
			assert isinstance(argument, str) and len(argument) is not 0

			setting = argument.split(self.__delimiter)
			argument_name = setting[0].strip()
			argument_value = setting[1].strip()
			self.__arguments[argument_name] = argument_value

	def get_argument(self, name: str) -> str:
		"""
		Returns argument by given name.
		:param name: THe name of argument, e.g. --path
		:return: The argument by given name
		"""
		return self.__arguments[name]


class AppArgumentsParser(ArgumentsParser):
	def __init__(self):
		super().__init__("=")

	def parse(self, arguments: list):
		super().parse(arguments)
		self.__validate()

	@property
	def storage_url(self) -> str:
		return self.get_argument("--url")

	def __validate(self):
		assert self.storage_url is not None and len(self.storage_url) is not 0
