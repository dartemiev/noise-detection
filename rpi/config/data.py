import math


class Pins(object):
	"""
	Data structure for defining pins used for ADC setup to read data and convert to digital
	representation which understandable for analyzer.
	"""

	def __init__(self, clk: int, cs: int, mosi: int, miso: int) -> None:
		"""
		:param
			clk:  Raspberry Pi pin for Serial Clock (output from master)
			cs:   Raspberry Pi pin for Chip select (active low, output from master)
			mosi: Raspberry Pi pin for output from master (Master Output, Slave Input)
			miso: Raspberry Pi pin for output from slave (Master Input, Slave Output)
		"""
		self.__miso = miso
		self.__mosi = mosi
		self.__clk = clk
		self.__cs = cs
		self.__validate()

	@property
	def miso(self) -> int:
		"""
		Raspberry Pi pin for output from slave (Master Input, Slave Output)
		"""
		return self.__miso

	@property
	def mosi(self) -> int:
		"""
		Raspberry Pi pin for output from master (Master Output, Slave Input)
		"""
		return self.__mosi

	@property
	def clk(self) -> int:
		"""
		Raspberry Pi pin for Serial Clock (output from master)
		"""
		return self.__clk

	@property
	def cs(self) -> int:
		"""
		Raspberry Pi pin for Chip select (active low, output from master)
		"""

		return self.__cs

	def __validate(self) -> None:
		"""
		Validates if all properties are set and have values
		"""
		assert isinstance(self.miso, int) and math.isnan(self.miso) == False
		assert isinstance(self.mosi, int) and math.isnan(self.mosi) == False
		assert isinstance(self.clk, int) and math.isnan(self.clk) == False
		assert isinstance(self.cs, int) and math.isnan(self.cs) == False


class ADCConfig(object):
	"""
	Data structure for defining configuration of ADC.
	"""

	def __init__(self, channel: int, pins: Pins) -> None:
		"""
		:param
			channel: The number of channel used to read data from sensor. Has to be in range [0..7]
			pins:    Pins setup for ADC to read data from sensor
		"""
		self.__channel = channel
		self.__pins = pins
		self.__validate()

	@property
	def channel(self) -> int:
		"""
		The number of channel used to read data from sensor. Has to be in range [0..7]
		"""
		return self.__channel

	@property
	def pins(self) -> Pins:
		"""
		Pins setup for ADC to read data from sensor
		"""
		return self.__pins

	def __validate(self):
		"""
		Validates if all properties are set and have values
		"""
		assert isinstance(self.channel, int) and math.isnan(self.channel) == False
		assert isinstance(self.pins, Pins) and self.pins is not None
