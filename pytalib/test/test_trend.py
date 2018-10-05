from unittest import TestCase
from ..indicators.trend import *

class MovingAverageConvergenceDivergenceTest(TestCase):

	def setUp(self):
		self.indicator = MovingAverageConvergenceDivergence()

	def test_validate_none_price(self):
		self.indicator.prices = None
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_empty_price(self):
		self.indicator.prices = []
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_none_f_ema_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = None
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_none_s_ema_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = None
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_none_signal_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = None
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_zero_f_ema_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 0
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_zero_s_ema_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 0
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_zero_signal_period(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 26
		self.indicator.signal_period = 0
		self.assertRaises(Exception, self.indicator.validate)

	def test_validate_invalid_period_pair(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 12
		self.indicator.s_ema_period = 2
		self.indicator.signal_period = 9
		self.assertRaises(Exception, self.indicator.validate)	

	def test_get_macd(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 2
		self.indicator.s_ema_period = 3
		self.indicator.signal_period = 3
		expected = [0, 0.17, 0.31, 0.40, 0.45, 0.47, 0.48, 0.49, 0.5, 0.5]
		
		self.assertEqual(expected, self.indicator.get_macd())

	def test_get_macd_signal_line(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 2
		self.indicator.s_ema_period = 3
		self.indicator.signal_period = 3
		expected = [0, 0.09, 0.2, 0.3, 0.38, 0.42, 0.45, 0.47, 0.48, 0.49]

		self.assertEqual(expected, self.indicator.get_macd_signal_line())

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.f_ema_period = 2
		self.indicator.s_ema_period = 3
		self.indicator.signal_period = 3
		macd = [0, 0.17, 0.31, 0.40, 0.45, 0.47, 0.48, 0.49, 0.5, 0.5]
		signal = [0, 0.09, 0.2, 0.3, 0.38, 0.42, 0.45, 0.47, 0.48, 0.49]
		expected = (macd, signal)

		self.assertEqual(expected, self.indicator.calculate())

class SimpleMovingAverageTest(TestCase):

	def setUp(self):
		self.indicator = SimpleMovingAverage()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 3

		expected = [0,0,2,3,4,5,6,7,8,9]

		self.assertEqual(expected, self.indicator.calculate())

	def test_calculate_2(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 4
		expected = [0,0,0,2.5,3.5,4.5,5.5,6.5,7.5,8.5]

		self.assertEqual(expected, self.indicator.calculate())
	
class WeightedMovingAverageTest(TestCase):

	def setUp(self):
		self.indicator = WeightedMovingAverage()

	def test_calculate(self):
		self.indicator.prices = [25000,9000,7000,8000,6000,12000,9000,4000,7000,3000,5000,8000,7800,5000]
		self.indicator.period = 2
		expected = [0.00, 14333.33,7666.67,7666.67,6666.67,10000,10000,5666.67,6000,4333.33,4333.33,7000,7866.67,5933.33]

		self.assertEqual(expected, self.indicator.calculate())

class ExponentialMovingAverageTest(TestCase):

	def setUp(self):
		self.indicator = ExponentialMovingAverage()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 3
		expected = [1, 1.5, 2.25, 3.12, 4.06, 5.03,6.02,7.01,8.00,9.00]

		self.assertEqual(expected, self.indicator.calculate())

	def test_calculate_2(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 2
		expected = [1, 1.67, 2.56, 3.52, 4.51, 5.5, 6.5, 7.5, 8.5, 9.5]

		self.assertEqual(expected, self.indicator.calculate())

class TrixTest(TestCase):

	def setUp(self):
		self.indicator = Trix()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 3
		expected = [0, 0.12, 0.2857, 0.3472, 0.3351, 0.2973, 0.256, 0.2156, 0.1832, 0.1598]

		self.assertEqual(expected, self.indicator.calculate())

class AverageDirectionalIndexTest(TestCase):

	def setUp(self):
		self.indicator = AverageDirectionalIndex()

	def test_reset(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.high = [2,3,4,5,6,7,8,9,10,11]
		self.indicator.low = [0,1,2,3,4,5,6,7,8,9]
		self.indicator.period = 1
		self.indicator.adx = [1,2,3,4,5,6,7,8,9,10]

		new_prices = [10,9,8,7,6,5,4,3,2,1]
		new_high = [11,10,9,8,7,6,5,4,3,2]
		new_low = [9,8,7,6,5,4,3,2,1,0]
		self.indicator.reset(new_prices, new_high, new_low, 1)

		self.assertEqual([], self.indicator.adx)
		self.assertEqual(new_prices, self.indicator.prices)
		self.assertEqual(new_high, self.indicator.high)
		self.assertEqual(new_low, self.indicator.low)

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.high = [2,3,4,5,6,7,8,9,10,11]
		self.indicator.low = [0,1,2,3,4,5,6,7,8,9]
		self.indicator.period = 3
		expected = [0, 0, 0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
		self.assertEqual(expected, self.indicator.calculate())
	
	def test_calculate_2(self):
		self.indicator.prices = [10,9,8,7,6,5,4,3,2,1]
		self.indicator.high = [11,10,9,8,7,6,5,4,3,2]
		self.indicator.low = [9,8,7,6,5,4,3,2,1,0]
		self.indicator.period = 3
		expected = [0, 0, 0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
		self.assertEqual(expected, self.indicator.calculate())

	def test_calculate_3(self):
		self.indicator.prices = [5,4,3,2,1,3,4,5,6,7]
		self.indicator.high = [5,7,4,2,2,3,5,7,7,7]
		self.indicator.low =  [4,3,3,2,1,1,3,5,5,6]
		self.indicator.period = 3
		expected = [0, 0, 0, 33.36, 4.0, 16.35, 44.57, 64.49, 70.78, 73.75]
		self.assertEqual(expected, self.indicator.calculate())

class CommodityChannelIndexTest(TestCase):

	def setUp(self):
		self.indicator = CommodityChannelIndex()

	def test_calculate(self):
		self.indicator.high = [24.20,24.07,24.04,23.87,23.67,23.59,23.80,23.80,24.30,24.15,24.05,24.06,23.88,25.14,25.20,25.07,25.22,25.37,25.36,25.26,24.82,24.44,24.65,24.84,24.75,24.51,24.68,24.67,23.84,24.30]
		self.indicator.low = [23.85,23.72,23.64,23.37,23.46,23.18,23.40,23.57,24.05,23.77,23.60,23.84,23.64,23.94,24.74,24.77,24.90,24.93,24.96,24.93,24.21,24.21,24.43,24.44,24.20,24.25,24.21,24.15,23.63,23.76]
		self.indicator.prices = [23.89,23.95,23.67,23.78,23.50,23.32,23.75,23.79,24.14,23.81,23.78,23.86,23.70,24.96,24.88,24.96,25.18,25.07,25.27,25.00,24.46,24.28,24.62,24.58,24.53,24.35,24.34,24.23,23.76,24.20]
		self.indicator.period = 20
		expected = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,101.19,30.41,6.06,33.94,35.22,13.61,-10.61,-11.67,-29.63,-131.58,-73.87]
		
		self.assertEqual(expected, self.indicator.calculate())

class DetrendedPriceOscillatorTest(TestCase):

	def setUp(self):
		self.indicator = DetrendedPriceOscillator()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 4

		expected = [0,0,0,0,0,0,4.5,4.5,4.5,4.5]

		self.assertEqual(expected, self.indicator.calculate())

class MassIndexTest(TestCase):

	def setUp(self):
		self.indicator = MassIndex()

	def test_calculate(self):
		self.indicator.prices = [5,4,3,2,1,3,4,5,6,7]
		self.indicator.high = [5,7,4,2,2,3,5,7,7,7]
		self.indicator.low =  [4,3,3,2,1,1,3,5,5,6]
		self.indicator.mi_period = 3
		self.indicator.ema_period = 3
		expected = [0.0, 0.0, 3.43, 3.1, 2.51, 2.65, 3.13, 3.39, 3.32, 3.06]
		self.assertEqual(expected, self.indicator.calculate())

class VortexIndicatorTest(TestCase):

	def setUp(self):
		self.indicator = VortexIndicator()

	def test_calculate(self):
		self.indicator.prices = [5,4,3,2,1,3,4,5,6,7]
		self.indicator.high = [5,7,4,2,2,3,5,7,7,7]
		self.indicator.low =  [4,3,3,2,1,1,3,5,5,6]
		self.indicator.period = 3
		pos_vi = [0.0, 0.0, 0.8, 0.83, 0.67, 0.75, 1.2, 1.43, 1.43, 1.33]
		neg_vi = [0.0, 0.0, 1.2, 1.33, 2.33, 1.0, 0.4, 0.14, 0.29, 0.5]
		
		self.assertEqual((pos_vi, neg_vi), self.indicator.calculate())

