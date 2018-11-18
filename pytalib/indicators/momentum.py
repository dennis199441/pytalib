from .base import MomentumIndicator, AbstractPriceIndicator, AbstractHighLowPriceIndicator
from .trend import SimpleMovingAverage, ExponentialMovingAverage

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
				try:
					self.roc.append(round((self.prices[i] - self.prices[i - self.period]) / self.prices[i - self.period], 2))
				except:
					self.roc.append(0.00)
					
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

class StochasticOscillator(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], k_period=14, d_period=3):
		self.k_period = k_period
		self.d_period = d_period
		self.stc = []
		self.stc_sma = []
		super().__init__(prices, high, low)

	def reset(self, prices=[], high=[], low=[], k_period=14, d_period=3):
		self.prices = prices
		self.high = high
		self.low = low
		self.k_period = k_period
		self.d_period = d_period
		self.stc = []
		self.stc_sma = []
		
	def validate(self):
		self._validate()

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
			if i < self.k_period:
				self.stc.append(0.00)
			else:
				period_low = min(self.low[i - self.k_period + 1 : i + 1])
				period_high = max(self.high[i - self.k_period + 1 : i + 1])
				self.stc.append(round( 100 * (self.prices[i] - period_low) / (period_high - period_low), 2))

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

class MoneyFlowIndex(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], volume=[], period=14):
		self.volume = volume
		self.period = period
		self.mfi = []
		self.tp = []
		self.raw_mf = []
		self.pos_mf = []
		self.neg_mf = []
		self.period_pos_mf = []
		self.period_neg_mf = []
		super().__init__(prices, high, low)

	def reset(self, prices=[], high=[], low=[], volume=[], period=14):
		self.prices = prices
		self.high = high
		self.low = low
		self.volume = volume
		self.period = period
		self.mfi = []
		self.tp = []
		self.raw_mf = []
		self.pos_mf = []
		self.neg_mf = []
		self.period_pos_mf = []
		self.period_neg_mf = []

	
	def validate(self):
		self._validate()

		if self.volume is None or len(self.volume) == 0:
			self.messages.append("`volume` cannot be None or empty.")

		if len(self.prices) != len(self.volume):
			self.messages.append("`prices`, `high`, `low`, `volume` must have the same length.")

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low) or self.period > len(self.volume):
			self.messages.append("`period` cannot be greater than length of `prices`, `high`, `low` and `volume`.")

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
		for i in range(len(self.prices)):
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
		for i in range(len(self.prices)):
			if i < self.period + 1:
				self.period_pos_mf.append(0.00)
			else:
				self.period_pos_mf.append(round(sum(pos_mf[i - self.period + 1: i + 1]), 2))

		return self.period_pos_mf

	def get_period_neg_mf(self):
		if len(self.period_neg_mf) != 0:
			return self.period_neg_mf

		pos_mf, neg_mf = self.get_pos_neg_mf()
		for i in range(len(self.prices)):
			if i < self.period + 1:
				self.period_neg_mf.append(0.00)
			else:
				self.period_neg_mf.append(round(max(sum(neg_mf[i - self.period + 1: i + 1]), 1), 2))

		return self.period_neg_mf

	def calculate(self):
		if len(self.mfi) != 0:
			return self.mfi

		period_pos_mf = self.get_period_pos_mf()
		period_neg_mf = self.get_period_neg_mf()
		for i in range(len(self.prices)):
			if i < self.period + 1:
				self.mfi.append(0.00)
			else:
				ratio = period_pos_mf[i] / period_neg_mf[i]
				self.mfi.append(round(100 - 100 / (1 + ratio), 2))

		return self.mfi

class TrueStrengthIndex(AbstractPriceIndicator):

	def __init__(self, prices=[], r_period=25, s_period=13):
		self.r_period = r_period
		self.s_period = s_period
		self.momentum = []
		self.abs_momentum = []
		self.tsi = []
		super().__init__(prices)

	def reset(self, prices=[], r_period=25, s_period=13):
		self.prices = prices
		self.r_period = r_period
		self.s_period = s_period
		self.momentum = []
		self.abs_momentum = []
		self.tsi = []

	def validate(self):
		self._validate()

		if self.r_period is None or self.r_period <= 0:
			self.messages.append("`r_period` cannot be None.")

		if self.s_period is None or self.s_period <= 0:
			self.messages.append("`s_period` cannot be None.")

		if self.r_period > len(self.prices):
			self.messages.append("`r_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.s_period > len(self.prices):
			self.messages.append("`s_period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_momentums(self):
		if len(self.momentum) != 0 and len(self.abs_momentum) != 0:
			return (self.momentum, self.abs_momentum)

		for i in range(len(self.prices)):
			if i == 0:
				self.momentum.append(0)
				self.abs_momentum.append(0)
			else:
				self.momentum.append(self.prices[i] - self.prices[i - 1])
				self.abs_momentum.append(abs(self.prices[i] - self.prices[i - 1]))

		return (self.momentum, self.abs_momentum)

	def calculate(self):
		if len(self.tsi) != 0:
			return self.tsi

		momentum, abs_momentum = self.get_momentums()

		ema = ExponentialMovingAverage(momentum, self.r_period)
		momentum_ema = ema.calculate()
		ema.reset(momentum_ema, self.s_period)
		smoothed_momentum_ema = ema.calculate()

		ema.reset(abs_momentum, self.r_period)
		abs_momentum_ema = ema.calculate()
		ema.reset(abs_momentum_ema, self.s_period)
		smoothed_abs_momentum_ema = ema.calculate()

		for i in range(len(smoothed_momentum_ema)):
			if i == 0:
				self.tsi.append(0.00)
			else:
				self.tsi.append(round(100 * (smoothed_momentum_ema[i] / smoothed_abs_momentum_ema[i]), 2))

		return self.tsi

class UltimateOscillator(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], s_period=7, m_period=14, l_period=28, s_weight=4, m_weight=2, l_weight=1):
		self.s_period = s_period
		self.m_period = m_period
		self.l_period = l_period
		self.s_weight = s_weight
		self.m_weight = m_weight
		self.l_weight = l_weight
		self.bp = []
		self.tr = []
		self.uo = []
		super().__init__(prices, high, low)

	def reset(self, prices=[], high=[], low=[], s_period=7, m_period=14, l_period=28, s_weight=4, m_weight=2, l_weight=1):
		self.prices = prices
		self.high = high
		self.low = low
		self.s_period = s_period
		self.m_period = m_period
		self.l_period = l_period
		self.s_weight = s_weight
		self.m_weight = m_weight
		self.l_weight = l_weight
		self.bp = []
		self.tr = []
		self.uo = []

	def validate(self):
		self._validate()

		if self.s_period is None or self.s_period <= 0:
			self.messages.append("`s_period` cannot be None.")

		if self.s_period > len(self.prices) or self.s_period > len(self.high) or self.s_period > len(self.low):
			self.messages.append("`s_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.m_period is None or self.m_period <= 0:
			self.messages.append("`m_period` cannot be None.")

		if self.m_period > len(self.prices) or self.m_period > len(self.high) or self.m_period > len(self.low):
			self.messages.append("`m_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.l_period is None or self.l_period <= 0:
			self.messages.append("`l_period` cannot be None.")

		if self.l_period > len(self.prices) or self.l_period > len(self.high) or self.l_period > len(self.low):
			self.messages.append("`l_period` cannot be greater than length of `prices`, `high` and `low`.")

		if self.s_weight is None or self.s_weight <= 0:
			self.messages.append("`s_weight` cannot be None.")

		if self.m_weight is None or self.m_weight <= 0:
			self.messages.append("`m_weight` cannot be None.")

		if self.l_weight is None or self.l_weight <= 0:
			self.messages.append("`l_weight` cannot be None.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def get_bp(self):
		if len(self.bp) != 0:
			return self.bp

		for i in range(len(self.prices)):
			if i == 0:
				self.bp.append(0.00)
			else:
				self.bp.append(round(self.prices[i] - min(self.low[i], self.prices[i - 1]), 2))
		
		return self.bp

	def get_tr(self):
		if len(self.tr) != 0:
			return self.tr

		for i in range(len(self.prices)):
			if i == 0:
				self.tr.append(0.00)
			else:
				self.tr.append(round(max(self.high[i], self.prices[i - 1]) - min(self.low[i], self.prices[i - 1]), 2))
		
		return self.tr

	def get_period_avg(self, period):
		period_avg = []
		bp = self.get_bp()
		tr = self.get_tr()
		for i in range(len(self.prices)):
			if i < period:
				period_avg.append(0.00)
			else:
				period_avg.append(round(sum(bp[i - period + 1 : i + 1]) / sum(tr[i - period + 1 : i + 1]), 2))
		
		return period_avg

	def calculate(self):
		if len(self.uo) != 0:
			return self.uo

		s_period_avg = self.get_period_avg(self.s_period)
		m_period_avg = self.get_period_avg(self.m_period)
		l_period_avg = self.get_period_avg(self.l_period)

		for i in range(len(self.prices)):
			if i < self.l_period:
				self.uo.append(0.00)
			else:
				self.uo.append(round( 100 * ((self.s_weight * s_period_avg[i]) + (self.m_weight * m_period_avg[i]) + (self.l_weight * l_period_avg[i])) / (self.s_weight + self.m_weight + self.l_weight),2))

		return self.uo

class Williams(AbstractHighLowPriceIndicator):
	
	def __init__(self, prices=[], high=[], low=[], period=14):
		self.period = period
		self.williams = []
		super().__init__(prices, high, low)

	def reset(self, prices=[], high=[], low=[], period=14):
		self.prices = prices
		self.high = high
		self.low = low
		self.period = period
		self.williams = []

	def validate(self):
		self._validate()

		if self.period is None or self.period <= 0:
			self.messages.append("`period` cannot be None.")

		if self.period > len(self.prices) or self.period > len(self.high) or self.period > len(self.low):
			self.messages.append("`period` cannot be greater than length of `prices`, `high` and `low`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.williams) != 0:
			return self.williams

		for i in range(len(self.prices)):
			if i < self.period - 1:
				self.williams.append(0.00)
			else:
				hh = max(self.high[i - self.period + 1 : i + 1])
				ll = min(self.low[i - self.period + 1 : i + 1])
				self.williams.append(round( -100 * ((hh - self.prices[i]) / (hh - ll)),2))
		
		return self.williams

class KnowSureThingOscillator(AbstractPriceIndicator):

	def __init__(self, prices=[], ss_roc_period=10, s_roc_period=15, m_roc_period=20, l_roc_period=30, ss_ma_period=10
			, s_ma_period=10, m_ma_period=10, l_ma_period=15, ss_weight=1, s_weight=2, m_weight=3, l_weight=4, signal_period=9):
		self.ss_roc_period = ss_roc_period
		self.s_roc_period = s_roc_period
		self.m_roc_period = m_roc_period
		self.l_roc_period = l_roc_period
		self.ss_ma_period = ss_ma_period
		self.s_ma_period = s_ma_period
		self.m_ma_period = m_ma_period
		self.l_ma_period = l_ma_period
		self.ss_weight = ss_weight
		self.s_weight = s_weight
		self.m_weight = m_weight
		self.l_weight = l_weight
		self.signal_period = signal_period
		self.kst = []
		self.kst_signal = []
		super().__init__(prices)

	def reset(self, prices=[], ss_roc_period=10, s_roc_period=15, m_roc_period=20, l_roc_period=30, ss_ma_period=10, s_ma_period=10
			, m_ma_period=10, l_ma_period=15, ss_weight=1, s_weight=2, m_weight=3, l_weight=4, signal_period=9):
		self.prices = prices
		self.ss_roc_period = ss_roc_period
		self.s_roc_period = s_roc_period
		self.m_roc_period = m_roc_period
		self.l_roc_period = l_roc_period
		self.ss_ma_period = ss_ma_period
		self.s_ma_period = s_ma_period
		self.m_ma_period = m_ma_period
		self.l_ma_period = l_ma_period
		self.ss_weight = ss_weight
		self.s_weight = s_weight
		self.m_weight = m_weight
		self.l_weight = l_weight
		self.signal_period = signal_period
		self.kst = []
		self.kst_signal = []

	def validate(self):
		self._validate()

		if self.ss_roc_period is None or self.ss_roc_period <= 0:
			self.messages.append("`ss_roc_period` cannot be None.")

		if self.s_roc_period is None or self.s_roc_period <= 0:
			self.messages.append("`s_roc_period` cannot be None.")

		if self.m_roc_period is None or self.m_roc_period <= 0:
			self.messages.append("`m_roc_period` cannot be None.")

		if self.l_roc_period is None or self.l_roc_period <= 0:
			self.messages.append("`l_roc_period` cannot be None.")

		if self.ss_ma_period is None or self.ss_ma_period <= 0:
			self.messages.append("`ss_ma_period` cannot be None.")

		if self.s_ma_period is None or self.s_ma_period <= 0:
			self.messages.append("`s_ma_period` cannot be None.")

		if self.m_ma_period is None or self.m_ma_period <= 0:
			self.messages.append("`m_ma_period` cannot be None.")

		if self.l_ma_period is None or self.l_ma_period <= 0:
			self.messages.append("`l_ma_period` cannot be None.")

		if self.ss_weight is None or self.ss_weight <= 0:
			self.messages.append("`ss_weight` cannot be None.")

		if self.s_weight is None or self.s_weight <= 0:
			self.messages.append("`s_weight` cannot be None.")

		if self.m_weight is None or self.m_weight <= 0:
			self.messages.append("`m_weight` cannot be None.")

		if self.l_weight is None or self.l_weight <= 0:
			self.messages.append("`l_weight` cannot be None.")

		if self.signal_period is None or self.signal_period <= 0:
			self.messages.append("`signal_period` cannot be None.")

		if self.ss_roc_period > self.s_roc_period and self.s_roc_period > self.m_roc_period and self.m_roc_period > self.l_roc_period:
			self.messages.append("Invalid: `ss_roc_period` > `s_roc_period` and `s_roc_period` > `m_roc_period` and `m_roc_period` > `l_roc_period`")

		if self.ss_ma_period > self.s_ma_period and self.s_ma_period > self.m_ma_period and self.m_ma_period > self.l_ma_period:
			self.messages.append("Invalid: `ss_ma_period` > `s_ma_period` and `s_ma_period` > `m_ma_period` and `m_ma_period` > `l_ma_period`")

		if self.ss_roc_period > len(self.prices):
			self.messages.append("`ss_roc_period` cannot be greater than length of `prices`.")

		if self.ss_ma_period > len(self.prices):
			self.messages.append("`ss_ma_period` cannot be greater than length of `prices`.")

		if len(self.messages) > 0:
			raise Exception(", ".join(self.messages))

	def calculate(self):
		if len(self.kst) != 0 and len(self.kst_signal) != 0:
			return (self.kst, self.kst_signal)

		self.validate()

		roc = RateOfChange(self.prices, self.ss_roc_period)
		ss_roc = roc.calculate()
		sma = SimpleMovingAverage(ss_roc, self.ss_ma_period)
		ss_ma = sma.calculate()

		roc.reset(self.prices, self.s_roc_period)
		s_roc = roc.calculate()
		sma.reset(s_roc, self.s_ma_period)
		s_ma = sma.calculate()

		roc.reset(self.prices, self.m_roc_period)
		m_roc = roc.calculate()
		sma.reset(m_roc, self.m_ma_period)
		m_ma = sma.calculate()

		roc.reset(self.prices, self.l_roc_period)
		l_roc = roc.calculate()
		sma.reset(l_roc, self.l_ma_period)
		l_ma = sma.calculate()

		for i in range(len(self.prices)):
			if i < self.l_roc_period + self.l_ma_period - 1:
				self.kst.append(0.00)
			else:
				self.kst.append(round((ss_ma[i] * self.ss_weight) + (s_ma[i] * self.s_weight) + (m_ma[i] * self.m_weight) + (l_ma[i] * self.l_weight), 2))

		sma.reset(self.kst, self.signal_period)
		self.kst_signal = sma.calculate()

		return (self.kst, self.kst_signal)
