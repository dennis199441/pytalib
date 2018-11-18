from .base import AbstractPriceIndicator, AbstractMovingAverages, AbstractHighLowPriceIndicator

class MovingAverageConvergenceDivergence(AbstractPriceIndicator):

	def __init__(self, prices=[], f_ema_period=12, s_ema_period=26, signal_period=9):
		self.f_ema_period = f_ema_period
		self.s_ema_period = s_ema_period
		self.signal_period = signal_period
		self.macd = []
		self.macd_signal_line = []
		super().__init__(prices)

	def reset(self, prices, f_ema_period=12, s_ema_period=26, signal_period=9):
		self.prices = prices
		self.f_ema_period = f_ema_period
		self.s_ema_period = s_ema_period
		self.signal_period = signal_period
		self.macd = []
		self.macd_signal_line = []

	def validate(self):
		self._validate()

		if self.f_ema_period is None or self.f_ema_period <= 0:
			self.messages.append("`f_ema_period` cannot be None.")

		if self.s_ema_period is None or self.s_ema_period <= 0:
			self.messages.append("`s_ema_period` cannot be None.")

		if self.signal_period is None or self.signal_period <= 0:
			self.messages.append("`signal_period` cannot be None.")

		if self.f_ema_period is not None and self.f_ema_period is not None and self.f_ema_period >= self.s_ema_period:
			self.messages.append("`f_ema_period` must be greater than `s_ema_period`")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_macd(self):
		if len(self.macd) != 0:
			return self.macd

		self.validate()
		f_ema = ExponentialMovingAverage(self.prices, self.f_ema_period).calculate()
		s_ema = ExponentialMovingAverage(self.prices, self.s_ema_period).calculate()

		if len(f_ema) != len(s_ema):
			raise Exception("Different len(f_ema) and len(s_ema)!")

		for i in range(len(f_ema)):
			self.macd.append(round(f_ema[i] - s_ema[i], 2))

		return self.macd

	def get_macd_signal_line(self):
		if len(self.macd_signal_line) != 0:
			return self.macd_signal_line

		self.macd_signal_line = ExponentialMovingAverage(self.get_macd(), self.signal_period).calculate()

		return self.macd_signal_line

	def calculate(self):
		return (self.get_macd(), self.get_macd_signal_line())

class SimpleMovingAverage(AbstractMovingAverages):
	
	def __init__(self, prices=[], period=20):
		self.sma = []
		super().__init__(prices, period)

	def reset(self, prices, period=20):
		self.prices = prices
		self.period = period
		self.sma = []

	def calculate(self):
		if len(self.sma) != 0:
			return self.sma

		self.validate()

		for i in range(len(self.prices)):
			if i < self.period - 1:
				self.sma.append(0)
			else:
				self.sma.append(round(sum(self.prices[i + 1 - self.period : i + 1]) / self.period, 2))

		return self.sma

class WeightedMovingAverage(AbstractMovingAverages):

	def __init__(self, prices=[], period=20):
		self.wma = []
		super().__init__(prices, period)

	def reset(self, prices, period=20):
		self.prices = prices
		self.period = period
		self.wma = []

	def calculate(self):
		if len(self.wma) != 0:
			return self.wma

		self.validate()

		multiplier = []
		denominator = 0
		for i in range(1, self.period + 1):
			multiplier.append(i)
			denominator += i

		total_price = 0
		numerator = 0
		for i in range(len(self.prices)):
			if i < self.period - 1:
				self.wma.append(0.00)
			elif i == self.period - 1:
				total_price = sum(self.prices[i - self.period + 1 : i + 1])
				numerator = 0
				for j in range(self.period):
					numerator += multiplier[j] * self.prices[j]
				self.wma.append(round(numerator / denominator, 2))
			else:
				numerator = numerator + self.period * self.prices[i] - total_price
				total_price = total_price + self.prices[i] - self.prices[i - self.period]
				self.wma.append(round(numerator / denominator, 2))

		return self.wma

class ExponentialMovingAverage(AbstractMovingAverages):

	def __init__(self, prices=[], period=20):
		self.ema = []
		super().__init__(prices, period)

	def reset(self, prices, period=20):
		self.prices = prices
		self.period = period
		self.ema = []

	def calculate(self):
		if len(self.ema) != 0:
			return self.ema

		self.validate()
		multiplier = 2 / (self.period + 1)

		for i in range(len(self.prices)):
			if i == 0:
				self.ema.append(self.prices[i])
			else:
				self.ema.append(round((self.prices[i] - self.ema[i - 1]) * multiplier + self.ema[i - 1], 2))

		return self.ema

class Trix(AbstractMovingAverages):

	def __init__(self, prices=[], period=15):
		self.trix = []
		super().__init__(prices, period)

	def reset(self, prices, period=15):
		self.prices = prices
		self.period = period
		self.trix = []

	def calculate(self):
		if len(self.trix) != 0:
			return self.trix

		self.validate()
		ema = ExponentialMovingAverage(self.prices, self.period)
		for i in range(3):
			self.trix = ema.calculate()
			ema.reset(self.trix, self.period)

		i = len(self.trix) - 1
		while i >= 0:
			if i > 0:
				self.trix[i] = round((self.trix[i] - self.trix[i - 1]) / self.trix[i - 1], 4)
			else:
				self.trix[i] = 0
			i -= 1

		return self.trix

class AverageDirectionalIndex(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], period=14):
		self.period = period
		self.tr = []
		self.period_tr = []
		self.pos_dm = []
		self.pos_period_dm = []
		self.neg_dm = []
		self.neg_period_dm = []
		self.pos_period_di = []
		self.neg_period_di = []
		self.adx = []
		super().__init__(prices, high, low)

	def validate(self):
		self._validate()

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low):
			self.messages.append("`period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def reset(self, prices, high, low, period):
		self.prices = prices
		self.high = high
		self.low = low
		self.period = period
		self.tr = []
		self.period_tr = []
		self.pos_dm = []
		self.pos_period_dm = []
		self.neg_dm = []
		self.neg_period_dm = []
		self.pos_period_di = []
		self.neg_period_di = []
		self.adx = []

	def get_tr(self):
		if len(self.tr) != 0:
			return self.tr

		for i in range(len(self.prices)):
			if i == 0:
				self.tr.append(0.00)
			else:
				self.tr.append(round(max(abs(self.high[i] - self.low[i]), abs(self.low[i] - self.low[i - 1]), abs(self.high[i] - self.prices[i - 1])), 2))
						
		return self.tr

	def get_period_tr(self):
		if len(self.period_tr) != 0:
			return self.period_tr

		tr = self.get_tr()
		for i in range(len(self.tr)):
			if i < self.period:
				self.period_tr.append(0.00)
				continue

			if i == self.period:
				self.period_tr.append(round(sum(tr[i - self.period + 1 : i + 1]), 2))
			else:
				self.period_tr.append(round(self.period_tr[i - 1] - (self.period_tr[i - 1] / self.period) + tr[i], 2))

		return self.period_tr

	def get_pos_dm(self):
		if len(self.pos_dm) != 0:
			return self.pos_dm

		for i in range(len(self.prices)):
			if i == 0:
				self.pos_dm.append(0.00)
				continue

			if self.high[i] - self.high[i - 1] > self.low[i - 1] - self.low[i]:
				if self.high[i] - self.high[i - 1] > 0:
					self.pos_dm.append(round(self.high[i] - self.high[i - 1], 2))
				else:
					self.pos_dm.append(0.00)
			else:
				self.pos_dm.append(0.00)

		return self.pos_dm

	def get_pos_period_dm(self):
		if len(self.pos_period_dm) != 0:
			return self.pos_period_dm

		pos_dm = self.get_pos_dm()
		for i in range(len(pos_dm)):
			if i < self.period:
				self.pos_period_dm.append(0.00)
				continue

			if i == self.period:
				self.pos_period_dm.append(round(sum(pos_dm[i - self.period + 1: i + 1]), 2))
			else:
				self.pos_period_dm.append(round(self.pos_period_dm[i - 1] - (self.pos_period_dm[i - 1] / self.period) + pos_dm[i], 2))

		return self.pos_period_dm

	def get_neg_dm(self):
		if len(self.neg_dm) != 0:
			return self.neg_dm

		for i in range(len(self.prices)):
			if i == 0:
				self.neg_dm.append(0.00)
				continue

			if self.low[i - 1] - self.low[i] > self.high[i] - self.high[i -1]:
				if self.low[i - 1] - self.low[i] > 0:
					self.neg_dm.append(round(self.low[i - 1] - self.low[i], 2))
				else:
					self.neg_dm.append(0.00)
			else:
				self.neg_dm.append(0.00)

		return self.neg_dm

	def get_neg_period_dm(self):
		if len(self.neg_period_dm) != 0:
			return self.neg_period_dm

		neg_dm = self.get_neg_dm()
		for i in range(len(neg_dm)):
			if i < self.period:
				self.neg_period_dm.append(0.00)
				continue

			if i == self.period:
				self.neg_period_dm.append(round(sum(neg_dm[i - self.period + 1: i + 1]), 2))
			else:
				self.neg_period_dm.append(round(self.neg_period_dm[i - 1] - (self.neg_period_dm[i - 1] / self.period) + neg_dm[i], 2))

		return self.neg_period_dm

	def get_pos_period_di(self):
		if len(self.pos_period_di) != 0:
			return self.pos_period_di

		period_tr = self.get_period_tr()
		pos_period_dm = self.get_pos_period_dm()

		self.pos_period_di = ExponentialMovingAverage(pos_period_dm, self.period).calculate()
		for i in range(len(self.pos_period_di)):
			if i < self.period:
				self.pos_period_di[i] = 0.0
			else:
				self.pos_period_di[i] = round((self.pos_period_di[i] / period_tr[i]) * 100, 2)

		return self.pos_period_di

	def get_neg_period_di(self):
		if len(self.neg_period_di) != 0:
			return self.neg_period_di

		period_tr = self.get_period_tr()
		neg_period_dm = self.get_neg_period_dm()

		self.neg_period_di = ExponentialMovingAverage(neg_period_dm, self.period).calculate()
		for i in range(len(self.neg_period_di)):
			if i < self.period:
				self.neg_period_di[i] = 0.0
			else:
				self.neg_period_di[i] = round((self.neg_period_di[i] / period_tr[i]) * 100, 2)

		return self.neg_period_di

	def get_adx(self):
		if len(self.adx) != 0:
			return self.adx

		pos_period_di = self.get_pos_period_di()
		neg_period_di = self.get_neg_period_di()
		for i in range(len(pos_period_di)):
			if i < self.period:
				self.adx.append(0)
			else:
				self.adx.append(round((abs(pos_period_di[i] - neg_period_di[i]) / (pos_period_di[i] + neg_period_di[i])) * 100, 2))
	
		return self.adx

	def calculate(self):
		if len(self.adx) != 0:
			return self.adx

		self.validate()

		return self.get_adx()

class CommodityChannelIndex(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], period=14, cci_constant=0.015):
		self.period = period
		self.cci_constant = cci_constant
		self.mean_sd = []
		self.tp = []
		self.cci = []
		super().__init__(prices, high, low)

	def reset(self, prices, high, low, period=14, cci_constant=0.015):
		self.prices = prices
		self.high = high
		self.low = low
		self.period = period
		self.cci_constant = cci_constant
		self.mean_sd = []
		self.tp = []
		self.cci = []

	def validate(self):
		self._validate()

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

	def get_mean_sd(self):
		if len(self.mean_sd) != 0:
			return self.mean_sd

		for i in range(len(self.prices)):
			if i < self.period - 1:
				self.mean_sd.append(0.00)
				continue
			
			mean = sum(self.get_tp()[i - self.period + 1 : i + 1]) / self.period
			abs_sum = 0
			for j in range(i - self.period + 1, i + 1):
				abs_sum += abs(self.get_tp()[j] - mean)

			self.mean_sd.append(round(abs_sum / self.period, 2))

		return self.mean_sd

	def calculate(self):
		if len(self.cci) != 0:
			return self.cci

		self.validate()
		sma = SimpleMovingAverage(self.get_tp(), self.period).calculate()
		
		for i in range(len(sma)):
			if i < self.period - 1:
				self.cci.append(0.00)
			else:
				self.cci.append(round((self.get_tp()[i] - sma[i]) / (self.cci_constant * self.get_mean_sd()[i]), 2))

		return self.cci

class DetrendedPriceOscillator(AbstractMovingAverages):
	
	def __init__(self, prices=[], period=20):
		self.dpo = []
		super().__init__(prices, period)

	def reset(self, prices, period=20):
		self.prices = prices
		self.period = period
		self.dpo = []

	def calculate(self):
		if len(self.dpo) != 0:
			return self.dpo

		self.validate()
		sma = SimpleMovingAverage(self.prices, self.period).calculate()
		price_index = int(self.period / 2 + 1)


		for i in range(len(sma)):
			if i < self.period + price_index - 1:
				self.dpo.append(0.00)
			else:
				self.dpo.append(self.prices[i] - sma[i - price_index])

		return self.dpo

class MassIndex(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], mi_period=25, ema_period=9):
		self.high = high
		self.low = low
		self.mi_period = mi_period
		self.ema_period = ema_period
		self.mi = []
		super().__init__(prices, high, low)

	def validate(self):
		self._validate()

		if self.mi_period is None or self.mi_period <= 0:
			self.messages.append("`mi_period` cannot be None.")

		if self.ema_period is None or self.ema_period <= 0:
			self.messages.append("`ema_period` cannot be None.")

		if self.mi_period > len(self.prices) or self.mi_period > len(self.high) or self.mi_period > len(self.low):
			self.messages.append("`mi_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.ema_period > len(self.prices) or self.ema_period > len(self.high) or self.ema_period > len(self.low):
			self.messages.append("`ema_period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def reset(self, prices, high, low, mi_period=25, ema_period=9):
		self.prices = prices
		self.high = high
		self.low = low
		self.mi_period = mi_period
		self.ema_period = ema_period
		self.mi = []

	def calculate(self):
		if len(self.mi) != 0:
			return self.mi

		self.validate()

		diff_h_l = [ self.high[i] - self.low[i] for i in range(len(self.high))]

		ema = ExponentialMovingAverage(diff_h_l, self.ema_period)
		single_ema = ema.calculate()
		ema.reset(single_ema, self.ema_period)
		double_ema = ema.calculate()

		ema_ratio = []
		for i in range(len(single_ema)):
			if double_ema[i] == 0:
				ema_ratio.append(0)
			else:
				ema_ratio.append(round(single_ema[i] / double_ema[i], 2))
		
		for i in range(len(ema_ratio)):
			if i < self.mi_period - 1:
				self.mi.append(0.00)
			else:
				self.mi.append(round(sum(ema_ratio[i - self.mi_period + 1 : i + 1]),2))
		
		return self.mi

class VortexIndicator(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], period=21):
		self.period = period
		self.tr = []
		self.pos_vm = []
		self.neg_vm = []
		self.period_tr = []
		self.period_pos_vm = []
		self.period_neg_vm = []
		self.pos_vi = []
		self.neg_vi = []
		super().__init__(prices, high, low)

	def reset(self, prices=[], high=[], low=[], period=21):
		self.high = high
		self.low = low
		self.period = period
		self.tr = []
		self.pos_vm = []
		self.neg_vm = []
		self.period_tr = []
		self.period_pos_vm = []
		self.period_neg_vm = []
		self.pos_vi = []
		self.neg_vi = []

	def validate(self):
		self._validate()

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low):
			self.messages.append("`period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_tr(self):
		if len(self.tr) != 0:
			return self.tr

		for i in range(len(self.prices)):
			if i == 0:
				self.tr.append(0.00)
			else:
				self.tr.append(round(max(abs(self.high[i] - self.low[i]), abs(self.low[i] - self.low[i - 1]), abs(self.high[i] - self.prices[i - 1])), 2))
						
		return self.tr

	def get_pos_vm(self):
		if len(self.pos_vm) != 0:
			return self.pos_vm

		for i in range(len(self.prices)):
			if i == 0:
				self.pos_vm.append(0.00)
			else:
				self.pos_vm.append(round(abs(self.high[i] - self.low[i - 1]), 2))

		return self.pos_vm

	def get_neg_vm(self):
		if len(self.neg_vm) != 0:
			return self.neg_vm

		for i in range(len(self.prices)):
			if i == 0:
				self.neg_vm.append(0.00)
			else:
				self.neg_vm.append(round(abs(self.low[i] - self.high[i - 1]), 2))

		return self.neg_vm

	def get_period_tr(self):
		if len(self.period_tr) != 0:
			return self.period_tr

		tr = self.get_tr()
		self.period_tr.append(0.00)
		for i in range(1, len(tr)):
			if i < self.period - 1:
				self.period_tr.append(0.00)
			else:
				self.period_tr.append(round(sum(tr[i - self.period + 1 : i + 1]), 2))

		return self.period_tr

	def get_period_pos_vm(self):
		if len(self.period_pos_vm) != 0:
			return self.period_pos_vm

		pos_vm = self.get_pos_vm()
		self.period_pos_vm.append(0.00)
		for i in range(1, len(pos_vm)):
			if i < self.period - 1:
				self.period_pos_vm.append(0.00)
			else:
				self.period_pos_vm.append(round(sum(pos_vm[i - self.period + 1 : i + 1]), 2))

		return self.period_pos_vm
		
	def get_period_neg_vm(self):
		if len(self.period_neg_vm) != 0:
			return self.period_neg_vm
		
		neg_vm = self.get_neg_vm()
		self.period_neg_vm.append(0.00)
		for i in range(1, len(neg_vm)):
			if i < self.period - 1:
				self.period_neg_vm.append(0.00)
			else:
				self.period_neg_vm.append(round(sum(neg_vm[i - self.period + 1 : i + 1]), 2))

		return self.period_neg_vm
		
	def calculate(self):
		if len(self.pos_vi) != 0 and len(neg_vi) != 0:
			return (self.pos_vi, self.neg_vi)

		self.validate()
		
		for i in range(len(self.get_period_tr())):
			if i < self.period - 1:
				self.pos_vi.append(0.00)
				self.neg_vi.append(0.00)
			else:
				self.pos_vi.append(round(self.get_period_pos_vm()[i] / self.get_period_tr()[i], 2))
				self.neg_vi.append(round(self.get_period_neg_vm()[i] / self.get_period_tr()[i], 2))

		return (self.pos_vi, self.neg_vi)




