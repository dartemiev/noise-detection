import RPi.GPIO as GPIO


class MCP3008(object):
	"""
	The basic features of Microchip MCP3008:
		- capacity - 10-bit
		- channels - 8
		- bus      - SPI
		- supply   - 2.7-5.5V

	The pins of MCP3008
		- CH0-CH7 - channels for connecting analog sensors
		- VDD     - power voltage 2.7-5.5V
		- VREF    - reference voltage
		- AGND    - analog ground
		- DGND    - digital ground
		- CLK, D_OUT, D_IN, CS - SPI bus.

	The Serial Peripheral Interface (SPI) bus is a synchronous serial communication interface specification used for
	short distance communication, primarily in embedded systems. The interface was developed by Motorola and has become
	a de facto standard. Typical applications include Secure Digital cards and liquid crystal displays.

	@see https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus
	"""

	def __init__(self, pin_clk: int, pin_cs: int, pin_mosi: int, pin_miso: int) -> None:
		"""
		Setup for pinout between RPi and MCP3008 to make it work and read data from ADC and send it to RPI for
		further usage.

		:param
			pin_clk: RPi pin for Serial Clock (output from master)
			pin_cs: RPi pin for Chip select (active low, output from master)
			pin_mosi: RPi pin for output from master (Master Output, Slave Input)
			pin_miso: RPi pin for output from slave (Master Input, Slave Output)
		"""
		self.__pin_clk = pin_clk
		self.__pin_cs = pin_cs
		self.__pin_mosi = pin_mosi
		self.__pin_miso = pin_miso

		# Setup GPIO by specification of SPI bus
		GPIO.setup(pin_clk, GPIO.OUT)
		GPIO.setup(pin_cs, GPIO.OUT)
		GPIO.setup(pin_mosi, GPIO.OUT)
		GPIO.setup(pin_miso, GPIO.IN)

	def read(self, channel: int) -> int:
		"""
		Reads data from attached sensor to given channel of ADC.
		:param channel: The number of ADC channel (must be in range [0..7])
		:raise IndexError: if given ADC channel is out of range [0..7]
		:return: 10-bit of data read from channel (sensor)
		"""
		if 7 < channel < 0:
			raise IndexError("MCP3008 has only 8 ADC channels. Channel {0} is not available".format(channel))

		self.__setup_serial_clock()
		self.__setup_adc(channel)
		return self.__read_from_adc()

	def __setup_serial_clock(self) -> None:
		"""
		Setup serial clock to read data from ADC
		"""
		GPIO.output(self.__pin_cs, GPIO.HIGH)  # bring CS high
		GPIO.output(self.__pin_clk, GPIO.LOW)  # start clock low
		GPIO.output(self.__pin_cs, GPIO.LOW)  # bring CS low

	def __setup_adc(self, channel: int) -> None:
		"""
		Setup ADC to be able read data from attach to given channel sensor
		:param channel: Channel for configuring
		"""
		command_out = channel
		command_out |= 0x18  # start bit + single-ended bit
		command_out <<= 3  # we only need to send 5 bits here
		for i in range(5):
			if command_out & 0x80:
				GPIO.output(self.__pin_mosi, GPIO.HIGH)
			else:
				GPIO.output(self.__pin_mosi, GPIO.LOW)
			command_out <<= 1
			GPIO.output(self.__pin_clk, GPIO.HIGH)
			GPIO.output(self.__pin_clk, GPIO.LOW)

	def __read_from_adc(self) -> int:
		"""
		Reads data from channel and returns result as 10-bit value
		"""
		adc_out = 0
		# read in one empty bit, one null bit and 10 ADC bits
		for _ in range(12):
			GPIO.output(self.__pin_clk, GPIO.HIGH)
			GPIO.output(self.__pin_clk, GPIO.LOW)
			adc_out <<= 1
			if GPIO.input(self.__pin_miso):
				adc_out |= 0x1

		GPIO.output(self.__pin_cs, GPIO.HIGH)

		# first bit is"null so drop it
		adc_out >>= 1
		return adc_out
