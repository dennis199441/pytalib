from .base import MomentumIndicator, AbstractIndicator
from .trend import SimpleMovingAverage

class RateOfChange(MomentumIndicator):

	def __init__(self, prices=[], period=9):
		self.roc = []
		super().__init__(prices, period)

	def reset(self, prices, period=9):
		self.prices = prices
		self.period = period
		self.roc = []
	
	def calculate(self):
		if len(self.roc) != 0:
			return self.roc

		self.validate()

		for i in range(len(self.prices)):
			if i < self.period:
				self.roc.append(0.00)
			else:
				self.roc.append(round((self.prices[i] - self.prices[i - self.period]) / self.prices[i - self.period], 2))

		return self.roc

class RelativeStrengthIndex(MomentumIndicator):

	def __init__(self, prices=[], period=14):
		self.rsi = []
		self.rs = []
		self.gain = []
		self.loss = []
		self.avg_gain = []
		self.avg_loss = []
		super().__init__(prices, period)

	def reset(self, prices, period=14):
		self.prices = prices
		self.period = period
		self.rsi = []
		self.rs = []
		self.gain = []
		self.loss = []
		self.avg_gain = []
		self.avg_loss = []
	
	def get_gain_loss(self):
		if len(self.gain) != 0 and len(self.loss) != 0:
			return (self.gain, self.loss)

		for i in range(len(self.prices)):
			if i == 0:
				self.gain.append(0.00)
				self.loss.append(0.00)
				continue
			
			if self.prices[i] > self.prices[i - 1]:
				self.gain.append(round(self.prices[i] - self.prices[i - 1], 2))
				self.loss.append(0.00)
			elif self.prices[i] < self.prices[i - 1]:
				self.loss.append(round(self.prices[i - 1] - self.prices[i], 2))
				self.gain.append(0.00)
			else:
				self.gain.append(0.00)
				self.loss.append(0.00)

		return (self.gain, self.loss)

	def get_avg_gain_loss(self):
		if len(self.avg_gain) != 0 and len(self.avg_loss) != 0:
			return (self.avg_gain, self.avg_loss)

		gain, loss = self.get_gain_loss()
		for i in range(len(self.gain)):
			if i < self.period:
				self.avg_gain.append(0.00)
				self.avg_loss.append(0.00)
				continue

			self.avg_gain.append(round(sum(gain[i - self.period + 1 : i + 1]) / self.period, 2))
			self.avg_loss.append(round(sum(loss[i - self.period + 1 : i + 1]) / self.period, 2))

		return (self.avg_gain, self.avg_loss)


	def get_rs(self):
		if len(self.rs) != 0:
			return self.rs

		avg_gain, avg_loss = self.get_avg_gain_loss()
		for i in range(len(avg_gain)):
			if i < self.period:
				self.rs.append(0.00)
			else:
				self.rs.append(round(avg_gain[i] / avg_loss[i], 2))

		return self.rs

	def calculate(self):
		if len(self.rsi) != 0:
			return self.rsi

		self.validate()

		rs = self.get_rs()
		for i in range(len(rs)):
			if i < self.period:
				self.rsi.append(0.00)
			else:
				self.rsi.append(round((100 - 100 / (1 + rs[i])), 2))

		return self.rsi

class StochasticOscillator(AbstractIndicator):
	
	def __init__(self, prices=[], high=[], low=[], k_period=5, d_period=3):
		self.high = high
		self.low = low
		self.k_period = k_period
		self.d_period = d_period
		self.stc = []
		self.stc_sma = []
		super().__init__(prices)

	def reset(self, prices=[], high=[], low=[], k_period=5, d_period=3):
		self.prices = prices
		self.high = high
		self.low = low
		self.k_period = k_period
		self.d_period = d_period
		self.stc = []
		self.stc_sma = []
		
	def validate(self):
		self._validate()

		if self.high is None or len(self.high) == 0:
			self.messages.append("`high` cannot be None or empty.")

		if self.low is None or len(self.low) == 0:
			self.messages.append("`low` cannot be None or empty.")

		if self.k_period is None or self.k_period <= 0:
			self.messages.append("`k_period` cannot be None.")

		if self.d_period is None or self.d_period <= 0:
			self.messages.append("`d_period` cannot be None.")

		if self.k_period > len(self.prices) or self.k_period > len(self.high) or self.k_period > len(self.low):
			self.messages.append("`k_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.d_period > len(self.prices) or self.d_period > len(self.high) or self.d_period > len(self.low):
			self.messages.append("`d_period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_stc(self):
		if len(self.stc) != 0:
			return self.stc

		for i in range(len(self.prices)):
			if i < self.period:
				self.stc.append(0.00)
			else:
				period_low = min(self.low[i - self.k_period + 1 : i + 1])
				period_high = max(self.high[i - self.k_period + 1 : i + 1])
				self.append(round( 100 * (self.prices[i] - period_low) / (period_high - period_low), 2))

		return self.stc

	def get_stc_sma(self):
		if len(self.stc_sma) != 0:
			return self.stc_sma

		stc = self.get_stc()
		sma = SimpleMovingAverage(stc, self.d_period)
		self.stc_sma = sma.calculate()

		return self.stc_sma

	def calculate(self):
		if len(self.stc_sma) != 0 and len(self.stc) != 0:
			return (self.stc, self.stc_sma)

		self.validate()

		return (self.get_stc(), self.get_stc_sma())

class MoneyFlowIndex(AbstractIndicator):
	
	def __init__(self, prices=[], high=[], low=[], volume=[], period=14):
		self.high = high
		self.low = low
		self.volume = volume
		self.period = period
		self.d_period = d_period
		self.mfi = []
		self.tp = []
		self.raw_mf = []
		self.pos_mf = []
		self.neg_mf = []
		self.period_pos_mf = []
		self.period_neg_mf = []
		super().__init__(prices)

	def reset(self, prices=[], high=[], low=[], volume=[], period=14):
		self.prices = prices
		self.high = high
		self.low = low
		self.volume = volume
		self.period = period
		self.d_period = d_period
		self.mfi = []
		self.tp = []
		self.raw_mf = []
		self.pos_mf = []
		self.neg_mf = []
		self.period_pos_mf = []
		self.period_neg_mf = []

	
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

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low):
			self.messages.append("`period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_tp(self):
		if len(self.tp) != 0:
			return self.tp

		for i in range(len(self.prices)):
			self.tp.append(round((self.high[i] + self.low[i] + self.prices[i]) / 3, 2))

		return self.tp

	def get_raw_mf(self):
		if len(self.raw_mf) != 0:
			return self.raw_mf

		for i in range(len(self.get_tp())):
			self.raw_mf.append(round(self.get_tp()[i] * self.volume[i], 2))

		return self.raw_mf

	def get_pos_neg_mf(self):
		if len(self.pos_mf) != 0 and len(self.neg_mf) != 0:
			return (self.pos_mf, self.neg_mf)

		raw_mf = self.get_raw_mf()
		for i in range(self.prices):
			if i == 0 or self.prices[i] == self.prices[i - 1]:
				self.pos_mf.append(0.00)
				self.neg_mf.append(0.00)
				continue

			if self.prices[i] > self.prices[i - 1]:
				self.pos_mf.append(raw_mf[i])
				self.neg_mf.append(0.00)
			else:
				self.pos_mf.append(0.00)
				self.neg_mf.append(raw_mf[i])

		return (self.pos_mf, self.neg_mf)

	def get_period_pos_mf(self):
		if len(self.period_pos_mf) != 0:
			return self.period_pos_mf

		pos_mf, neg_mf = self.get_pos_neg_mf()
		for i in range(self.prices):
			if i < self.period + 1:
				self.period_pos_mf.append(0.00)
			else:
				self.period_pos_mf.append(round(sum(pos_mf[i - self.period + 1: i + 1]), 2))

		return self.period_pos_mf

	def get_period_neg_mf(self):
		if len(self.period_neg_mf) != 0:
			return self.period_neg_mf

		pos_mf, neg_mf = self.get_pos_neg_mf()
		for i in range(self.prices):
			if i < self.period + 1:
				self.period_neg_mf.append(0.00)
			else:
				self.period_neg_mf.append(round(sum(neg_mf[i - self.period + 1: i + 1]), 2))

		return self.period_neg_mf

	def calculate(self):
		if len(self.mfi) != 0:
			return self.mfi

		period_pos_mf = self.get_period_pos_mf()
		period_neg_mf = self.get_period_neg_mf()
		for i in range(self.prices):
			if i < self.period + 1:
				self.mfi.append(0.00)
			else:
				ratio = period_pos_mf[i] / period_neg_mf[i]
				self.mfi.append(round(100 - 100 / (1 + ratio), 2))

		return self.mfi

class TrueStrengthIndex(MomentumIndicator):
	
	def reset(self, prices):
		pass
	
	def calculate(self):
		
		return 0

class UltimateOscillator(MomentumIndicator):
	
	def reset(self, prices):
		pass
	
	def calculate(self):
		
		return 0

class Williams(MomentumIndicator):
	
	def reset(self, prices):
		pass
	
	def calculate(self):
		
		return 0

class KnowSureThingOscillator(MomentumIndicator):
	
	def reset(self, prices):
		pass

	def calculate(self):
		self.validate()
		
		return 0
