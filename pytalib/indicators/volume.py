from .base import VolumeIndicator, AbstractIndicator
from .trend import SimpleMovingAverage, WeightedMovingAverage, ExponentialMovingAverage
from .momentum import RateOfChange

class AccumulationDistributionLine(AbstractIndicator):

	def __init__(self, prices, high, low, volume, period):
		self.high = high
		self.low = low
		self.volume = volume
		self.period
		self.mf_multiplier = []
		self.mf_volume = []
		self.adl = []
		super().__init__(prices)

	def reset(self, prices, high, low, volume, period):
		self.prices = prices
		self.high = high
		self.low = low
		self.volume = volume
		self.period
		self.mf_multiplier = []
		self.mf_volume = []
		self.adl = []

	def validate(self):
		self._validate()

		if self.high is None or len(self.high) == 0:
			self.messages.append("`high` cannot be None or empty.")

		if self.low is None or len(self.low) == 0:
			self.messages.append("`low` cannot be None or empty.")

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if len(self.prices) != len(self.high) or len(self.high) != len(self.low) or len(self.low) != len(self.volume):
			self.messages.append("`prices`, `high`, `low`, `volume` must have the same length.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low) or self.period > len(self.volume):
			self.messages.append("`period` cannot be greater than length of `prices`, `high`, `low` and `volume`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_mf_multiplier(self):
		if len(self.mf_multiplier) != 0:
			return self.mf_multiplier

		for i in range(len(self.prices)):
			self.mf_multiplier.append(round(((self.prices[i] - self.low[i]) - (self.high[i] - self.prices[i])) / (self.high[i] - self.low[i]), 2))

		return self.mf_multiplier

	def get_mf_volume(self):
		if len(self.mf_volume) != 0:
			return self.mf_volume

		mf_multiplier = self.get_mf_multiplier()
		for i in range(len(self.prices)):
			self.mf_volume.append(round(mf_multiplier[i] * self.volume[i], 2))

		return self.mf_volume

	def calculate(self):
		if len(self.adl) != 0:
			return self.adl
		
		self.validate()

		mf_volume = self.get_mf_volume()
		for i in range(len(self.prices)):
			if i == 0:
				self.append(mf_volume[i])
			else:
				self.append(self.adl[i - 1] + mf_volume[i])

		return self.adl

class EaseOfMovement(AbstractIndicator):

	def __init__(self, prices, high, low, volume, period, ma_type='SMA'):
		self.high = high
		self.low = low
		self.volume = volume
		self.period = period
		self.ma_type = ma_type
		self.distance = []
		self.box_ratio = []
		self.emv = []
		self.period_emv = []
		super().__init__(prices)

	def reset(self, prices, high, low, volume, period, ma_type='SMA'):
		self.prices = prices
		self.high = high
		self.low = low
		self.volume = volume
		self.period = period
		self.ma_type = ma_type
		self.distance = []
		self.box_ratio = []
		self.emv = []
		self.period_emv = []

	def validate(self):
		self._validate()

		if self.high is None or len(self.high) == 0:
			self.messages.append("`high` cannot be None or empty.")

		if self.low is None or len(self.low) == 0:
			self.messages.append("`low` cannot be None or empty.")

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if len(self.prices) != len(self.high) or len(self.high) != len(self.low) or len(self.low) != len(self.volume):
			self.messages.append("`prices`, `high`, `low`, `volume` must have the same length.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low) or self.period > len(self.volume):
			self.messages.append("`period` cannot be greater than length of `prices`, `high`, `low` and `volume`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def get_distance(self):
		if len(self.distance) != 0:
			return self.distance

		for i in range(len(self.prices)):
			if i == 0:
				self.distance.append(0.00)
			else:
				self.distance.append(round((self.high[i] + self.low[i]) / 2 - (self.high[i - 1] + self.low[i - 1]) / 2, 2))

		return self.distance

	def get_box_ratio(self):
		if len(self.box_ratio) != 0:
			return self.box_ratio

		for i in range(len(self.prices)):
			self.box_ratio.append(round((self.volume[i] / 100000000) / (self.high[i] - self.low[i]) , 2))

		return self.box_ratio

	def get_emv(self):
		if len(self.emv) != 0:
			return self.emv

		distance = self.get_distance()
		box_ratio = self.get_box_ratio()
		for i in range(len(self.prices)):
			self.emv.append(round(distance[i] / box_ratio[i], 2))

		return self.emv

	def calculate(self):
		if len(self.period_emv) != 0:
			return self.period_emv

		self.validate()

		emv = self.get_emv()
		self.period_emv = self.getma(emv, self.period, self.ma_type).calculate()

		return self.period_emv

class ForceIndex(AbstractIndicator):

	def __init__(self, prices, volume, period, ma_type='EMA'):
		self.volume = volume
		self.period = period
		self.ma_type = ma_type
		self.fi = []
		self.period_fi = []
		super().__init__(prices)

	def reset(self, prices, volume, period, ma_type='EMA'):
		self.prices = prices
		self.volume = volume
		self.period = period
		self.ma_type = ma_type
		self.fi = []
		self.period_fi = []
	
	def validate(self):
		self._validate()

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if len(self.prices) != len(self.volume):
			self.messages.append("`prices` and `volume` must have the same length.")

		if self.period > len(self.prices) or self.period > len(self.volume):
			self.messages.append("`period` cannot be greater than length of `prices` and `volume`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def get_fi(self):
		if len(self.fi) != 0:
			return self.fi

		for i in range(len(self.prices)):
			if i == 0:
				self.fi.append(0.00)
			else:
				self.fi.append(round((self.prices[i] - self.prices[i - 1]) * self.volume[i], 2))

		return self.fi

	def calculate(self):
		if len(self.period_fi) != 0:
			return self.period_fi

		self.validate()

		fi = self.get_fi()
		self.period_fi = self.get_ma(fi, self.period, self.ma_type).calculate()

		return self.period_fi

class NegativeVolumeIndex(AbstractIndicator):

	def __init__(self, prices, volume, period, ma_type='EMA'):
		self.volume = volume
		self.period = period
		self.nvi = []
		self.signal = []
		super().__init__(prices)

	def reset(self, prices, volume, period, ma_type='EMA'):
		self.prices = prices
		self.volume = volume
		self.period = period
		self.nvi = []
		self.signal = []

	def validate(self):
		self._validate()

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if len(self.prices) != len(self.volume):
			self.messages.append("`prices` and `volume` must have the same length.")

		if self.period > len(self.prices) or self.period > len(self.volume):
			self.messages.append("`period` cannot be greater than length of `prices` and `volume`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_ma(self, series, period, ma_type='SMA'):
		if ma_type == 'EMA':
			return ExponentialMovingAverage(series, period)
		elif ma_type = 'WMA':
			return WeightedMovingAverage(series, period)

		return  SimpleMovingAverage(series, period)

	def get_nvi(self):
		if len(self.nvi) != 0:
			return self.nvi

		roc = RateOfChange(self.prices, 1)
		roc_price = roc.calculate()
		roc.reset(self.volume, 1)
		roc_volume = roc.calculate()

		for i in range(len(self.prices)):
			if i == 0:
				self.nvi.append(1000.00)
				continue

			if roc_volume[i] >= 0:
				self.nvi.append(self.nvi[i - 1])
			else:
				self.nvi.append(self.nvi[i - 1] + roc_price[i])

		return self.nvi

	def get_signal(self):
		if len(self.signal) != 0:
			return self.signal

		nvi = self.get_nvi()
		self.signal = self.get_ma(nvi, self.period, self.ma_type).calculate()

		return self.signal

	def calculate(self):
		if len(self.nvi) != 0 and len(self.signal) != 0:
			return (self.nvi, self.signal)

		self.validate()

		return (self.get_nvi(), self.get_signal())

class OnBalanceVolume(AbstractIndicator):

	def __init__(self, prices, volume):
		self.volume = volume
		self.period = period
		self.obv = []
		super().__init__(prices)

	def reset(self, prices, volume):
		self.prices = prices
		self.volume = volume
		self.obv = []

	def validate(self):
		self._validate()

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if len(self.prices) != len(self.volume):
			self.messages.append("`prices` and `volume` must have the same length.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))
	
	def calculate(self):
		if len(self.obv) != 0:
			return self.obv

		self.validate()

		for i in range(len(self.prices)):
			if i == 0:
				self.obv.append(0.00)
				continue

			if self.prices[i] > self.prices[i - 1]:
				self.obv.append(round(self.obv[i - 1] + self.volume[i] , 2))
			elif self.prices[i] < self.prices[i - 1]:
				self.obv.append(round(self.obv[i - 1] - self.volume[i] , 2))
			else:
				self.obv.append(round(self.obv[i - 1], 2))

		return self.obv

class PutCallRatio(AbstractIndicator):

	def __init__(self, prices, put_volume, call_volume):
		self.put_volume = put_volume
		self.call_volume = call_volume
		self.pc_ratio = []
		super().__init__(prices)

	def reset(self, prices, put_volume, call_volume):
		self.prices = prices
		self.put_volume = put_volume
		self.call_volume = call_volume
		self.pc_ratio = []
	
	def validate(self):
		self._validate()

		if self.put_volume is None or len(self.put_volume) == 0:
			self.messages.append("`put_volume` cannot be None or empty.")

		if self.call_volume is None or len(self.call_volume) == 0:
			self.messages.append("`call_volume` cannot be None or empty.")

		if len(self.prices) != len(self.put_volume) or len(self.put_volume) != len(self.call_volume):
			self.messages.append("`prices`, `put_volume` and `call_volume` must have the same length.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.pc_ratio) != 0:
			return self.pc_ratio

		self.validate()

		for i in range(len(self.prices)):
			self.pc_ratio.append(round(self.put_volume[i] / self.call_volume[i] , 2))

		return self.pc_ratio


class VolumePriceTrend(VolumeIndicator):

	def reset(self, prices):
		pass
	
	def calculate(self):
		return 0



