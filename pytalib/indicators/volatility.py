from .base import VolatilityIndicator, AbstractIndicator
from .trend import SimpleMovingAverage, WeightedMovingAverage, ExponentialMovingAverage
import statistics

class AverageTrueRange(VolatilityIndicator):

	def __init__(self, prices, period, ma_type='SMA'):
		self.tr = []
		self.atr = []
		self.ma_type = ma_type
		super().__init__(prices, period)

	def reset(self, prices, period):
		self.prices = prices
		self.period = period
		self.tr = []
		self.atr = []
		self.ma_type

	def get_tr(self):
		if len(self.tr) != 0:
			return self.tr

		for i in range(len(self.prices)):
			if i == 0:
				self.tr.append(0.00)
			else:
				self.tr.append(round(max(abs(self.high[i] - self.low[i]), abs(self.low[i] - self.low[i - 1]), abs(self.high[i] - self.prices[i - 1])), 2))
						
		return self.tr

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def calculate(self):
		if len(self.atr) != 0:
			return self.atr

		self.validate()

		self.atr = self.get_ma(self.tr, self.period, self.ma_type).calculate()

		return self.atr

class BollingerBands(AbstractIndicator):

	def __init__(self, prices=[], period=3, ma_type='SMA', num_std=2):
		self.period = period
		self.num_std = num_std
		self.ma_type = ma_type
		self.bb_up = []
		self.bb_down = []
		self.ma = []
		super().__init__(prices)

	def reset(self, prices, period=3, ma_type='SMA', num_std=2):
		self.prices = prices
		self.period = period
		self.num_std = num_std
		self.ma_type = ma_type
		self.bb_up = []
		self.bb_down = []
		self.ma = []

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def validate(self):
		self._validate()

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if self.period > len(self.prices):
			self.messages.append("`period` cannot be greater than length of `prices`.")

		if self.num_std is None or self.num_std <= 0:
			self.messages.append("`num_std` cannot be None.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.bb_up) != 0 and len(self.ma) != 0 and len(self.bb_down) != 0:
			return (self.bb_up, self.ma, self.bb_down)

		self.validate()

		self.ma = self.get_ma(self.prices, self.period, self.ma_type).calculate()
		std = StandardDeviation(self.prices, self.period)

		for i in range(len(self.prices)):
			self.bb_up.append(round(self.prices[i] + self.num_std * std[i], 2))
			self.bb_down.append(round(self.prices[i] - self.num_std * std[i], 2))

		return (self.bb_up, self.ma, self.bb_down)

class DonchianChannel(AbstractIndicator):

	def __init__(self, prices, high, low, period):
		self.high = high
		self.low = low
		self.period = period
		self.dc_up = []
		self.dc_mid = []
		self.dc_down = []
		super().__init__(prices)

	def reset(self, prices, high, low, period):
		self.prices = prices
		self.high = high
		self.low = low
		self.period = period
		self.dc_up = []
		self.dc_mid = []
		self.dc_down = []

	def validate(self):
		self._validate()

		if self.high is None or len(self.high) == 0:
			self.messages.append("`high` cannot be None or empty.")

		if self.low is None or len(self.low) == 0:
			self.messages.append("`low` cannot be None or empty.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if len(self.prices) != len(self.high) or len(self.high) != len(self.low):
			self.messages.append("`prices`, `high`, `low` must have the same length.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low):
			self.messages.append("`period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.dc_up) != 0 and len(self.dc_down) != 0 and len(self.dc_mid) != 0:
			return (self.dc_up, self.dc_mid, self.dc_down)
		
		self.validate()

		for i in range(len(self.prices)):
			start = i
			if i < self.period - 1:
				start = 0

			self.dc_up.append(max(self.high[start : i + 1]))
			self.dc_down.append(min(self.low[start : i + 1]))
			self.dc_mid.append((self.dc_up[i] + self.dc_down[i]) / 2)

		return (self.dc_up, self.dc_mid, self.dc_down)

class KeltnerChannel(AbstractIndicator):

	def __init__(self, prices, ma_type='EMA', ma_period=20, atr_period=10, num_atr=2, atr_ma_type='SMA'):
		self.ma_type = ma_type
		self.ma_period = ma_period
		self.atr_period = atr_period
		self.num_atr = num_atr
		self.atr_ma_type = atr_ma_type
		self.kc_up = []
		self.ma = []
		self.kc_down = []
		super().__init__(prices)

	def reset(self, prices, ma_type='EMA', ma_period=20, atr_period=10, num_atr=2, atr_ma_type='SMA'):
		self.prices = prices
		self.ma_type = ma_type
		self.ma_period = ma_period
		self.atr_period = atr_period
		self.num_atr = num_atr
		self.atr_ma_type = atr_ma_type
		self.kc_up = []
		self.ma = []
		self.kc_down = []

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def validate(self):
		self._validate()

		if self.ma_period is None or self.ma_period <= 0:
			self.messages.append("`ma_period` cannot be None.")

		if self.ma_period > len(self.prices):
			self.messages.append("`ma_period` cannot be greater than length of `prices`.")

		if self.atr_period is None or self.atr_period <= 0:
			self.messages.append("`atr_period` cannot be None.")

		if self.atr_period > len(self.prices):
			self.messages.append("`atr_period` cannot be greater than length of `prices`.")

		if self.num_atr is None or self.num_atr <= 0:
			self.messages.append("`num_atr` cannot be None.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.kc_up) != 0 and len(self.ma) != 0 and len(self.kc_down) != 0:
			return (self.kc_up, self.ma, self.kc_down)

		self.ma = self.get_ma(self.prices, self.ma_period, self.ma_type).calculate()
		atr = AverageTrueRange(self.prices, self.atr_period, self.atr_ma_type, self.atr_ma_type).calculate()

		for i in range(len(self.prices)):
			self.kc_up.append(round(self.ma[i] + self.num_atr * atr[i]  , 2))
			self.kc_up.append(round(self.ma[i] - self.num_atr * atr[i]  , 2))

		return (self.kc_up, self.ma, self.kc_down)

class StandardDeviation(VolatilityIndicator):

	def __init__(self, prices, period):
		self.std = []
		super().__init__(prices, period)

	def reset(self, prices, period):
		self.prices = prices
		self.period = period
		self.std = []

	def calculate(self):
		if len(self.std) != 0:
			return self.std

		self.validate()

		for i in range(len(self.prices)):
			if i < self.period - 1:
				self.std.append(0.00)
			else:
				std = statistics.stdev(self.prices[i - self.period + 1 : i + 1])
				self.std.append(round(std, 2))

		return self.std


