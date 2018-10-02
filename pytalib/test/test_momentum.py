from unittest import TestCase
from ..indicators.momentum import *

class RateOfChangeTest(TestCase):

	def setUp(self):
		self.indicator = RateOfChange()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 3
		expected = [0,0,0,3,1.5,1,0.75,0.6,0.5,0.43]
		self.assertEqual(expected, self.indicator.calculate())

class RelativeStrengthIndexTest(TestCase):

	def setUp(self):
		self.indicator = RelativeStrengthIndex()

	def test_calculate(self):
		self.indicator.prices = [44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13]
		self.indicator.period = 14
		expected = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,70.59,70.59,70.59,81.24,72.38,60.00,62.55,60.00,48.45,52.83,48.72,43.50,37.11,32.43,32.43,37.11,31.51,25.93,30.56]
		
		self.assertEqual(expected, self.indicator.calculate())

'''
class StochasticOscillatorTest(TestCase):

	def setUp(self):
		self.indicator = StochasticOscillator()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())

class MoneyFlowIndexTest(TestCase):

	def setUp(self):
		self.indicator = MoneyFlowIndex()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())

class TrueStrengthIndexTest(TestCase):

	def setUp(self):
		self.indicator = TrueStrengthIndex()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())

class UltimateOscillatorTest(TestCase):

	def setUp(self):
		self.indicator = UltimateOscillator()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())

class WilliamsTest(TestCase):

	def setUp(self):
		self.indicator = Williams()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())

class KnowSureThingOscillatorTest(TestCase):

	def setUp(self):
		self.indicator = KnowSureThingOscillator()

	def test_calculate(self):
		self.indicator.prices = [1,2,3,4,5,6,7,8,9,10]
		self.indicator.period = 1
		self.assertEqual(0, self.indicator.calculate())
'''