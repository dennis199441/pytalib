# pytalib
Pytalib is a python technical analysis library developed CMSC5720 project group which support various types of technical indicators. Pytalib adapts object oriented paradigm that each indicator is represented as an object. Unlike function-based library, using objects allow us to store some intermediate variables, for example Average gain/loss in RSI. This improves flexibility if we want to do further analysis on indicators.

## Python version
python3.6.4

## Types of indicators
#### Trend indicators
  1. Moving Average Convergence Divergence
  2. Simple Moving Average
  3. Weighted Moving Average
  4. Exponential Moving Average
  5. Trix
  6. Average Directional Index
  7. Commodity Channel Index
  8. Detrended Price Oscillator
  9. Mass Index
  10. Vortex Indicator
  
#### Momentum indicators
  1. Rate of Change
  2. Relative Strength Index
  3. Stochastic Oscillator
  4. Money Flow Index
  5. True Strength Index
  6. Ultimate Oscillator
  7. Williams
  8. Know Sure Thing Oscillator
  
#### Volatility indicators
  1. Average True Range
  2. Bollinger Bands
  3. Price Channel
  4. Keltner Channel
  5. Standard Deviation
  
#### Volume indicators
  1. Accumulation Distribution Line
  2. Ease of Movement
  3. Force Index
  4. Negative Volume Index
  5. On Balance Volume
  6. Put Call Ratio

## How to install
Pytalib has not been published on Python Package Index (PyPi) yet. I will update this in the future.
But basically the procedure is same as follows:
```
pip install pytalib
```

## How to use 
```
from pytalib.indicators.trend import SimpleMovingAverage

prices = [1,2,3,4,5,6,7,8,9,10]
sma = SimpleMovingAverage(prices=prices, period=3)
result = sma.calculate()
```
