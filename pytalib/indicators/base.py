from abc import ABC, abstractmethod

class AbstractIndicator(ABC):

	def __init__(self):
		self.messages = []
		super().__init__()

	@abstractmethod
	def _validate(self):
		pass

	@abstractmethod
	def validate(self):
		pass

	@abstractmethod
	def reset(self, prices):
		pass

	@abstractmethod
	def calculate(self):
		pass

class AbstractPriceIndicator(AbstractIndicator):

	def __init__(self, prices=[]):
		self.prices = prices
		super().__init__()

	def _validate(self):
		if self.prices is None:
			self.messages.append("`prices` cannot be None.")
		if self.prices is not None and len(self.prices) == 0:
			self.messages.append("`prices` cannot be an empty list.")

	@abstractmethod
	def validate(self):
		pass

	@abstractmethod
	def reset(self, prices):
		pass

	@abstractmethod
	def calculate(self):
		pass

class AbstractHighLowPriceIndicator(AbstractIndicator):
	
	def __init__(self, prices=[], high=[], low=[]):
		self.prices = prices
		self.high = high
		self.low = low
		self.messages = []
		super().__init__()

	def _validate(self):
		if self.prices is None:
			self.messages.append("`prices` cannot be None.")
		if self.prices is not None and len(self.prices) == 0:
			self.messages.append("`prices` cannot be an empty list.")
		if self.high is None or len(self.high) == 0:
			self.messages.append("`high` cannot be None or empty.")
		if self.low is None or len(self.low) == 0:
			self.messages.append("`low` cannot be None or empty.")
		if len(self.prices) != len(self.high) or len(self.high) != len(self.low):
			self.messages.append("`prices`, `high`, `low` must have the same length.")

	@abstractmethod
	def validate(self):
		pass

	@abstractmethod
	def reset(self, prices):
		pass

	@abstractmethod
	def calculate(self):
		pass

class AbstractMovingAverages(AbstractPriceIndicator):

	def __init__(self, prices=[], period=0):
		self.period = period
		super().__init__(prices)

	def validate(self):
		self._validate()

		if self.period is None:
			self.messages.append("`period` cannot be None.")
		else:
			if self.period < 0:
				self.messages.append("`period` must be greater than or equal to 0.")
			if self.prices is not None and len(self.prices) < self.period:
				self.messages.append("`prices` length must be greater than or equal to `period`. length={} period={}".format(len(self.prices), self.period))

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

class MomentumIndicator(AbstractPriceIndicator):

	def __init__(self, prices=[], period=0):
		self.period = period
		super().__init__(prices)

	def validate(self):
		self._validate()

		if self.period is None:
			self.messages.append("`period` cannot be None.")
		else:
			if self.period < 0:
				self.messages.append("`period` must be greater than or equal to 0.")
			if self.prices is not None and len(self.prices) < self.period:
				self.messages.append("`prices` length must be greater than or equal to `period`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

class VolatilityIndicator(AbstractPriceIndicator):

	def __init__(self, prices=[], period=0):
		self.period = period
		super().__init__(prices)

	def validate(self):
		self._validate()

		if self.period is None:
			self.messages.append("`period` cannot be None.")
		else:
			if self.period < 0:
				self.messages.append("`period` must be greater than or equal to 0.")
			if self.prices is not None and len(self.prices) < self.period:
				self.messages.append("`prices` length must be greater than or equal to `period`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

class VolumeIndicator(AbstractPriceIndicator):

	def __init__(self, prices=[], period=0):
		self.period = period
		super().__init__(prices)

	def validate(self):
		self._validate()

		if self.period is None:
			self.messages.append("`period` cannot be None.")
		else:
			if self.period < 0:
				self.messages.append("`period` must be greater than or equal to 0.")
			if self.prices is not None and len(self.prices) < self.period:
				self.messages.append("`prices` length must be greater than or equal to `period`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))





