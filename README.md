# pytalib
Pytalib is a python technical analysis library developed CMSC5720 project group which support various types of technical indicators. Pytalib adapts object oriented paradigm that each indicator is represented as an object. Unlike function-based library, using objects allow us to store some intermediate variables, for example Average gain/loss in RSI. This improves flexibility if we want to do further analysis on indicators.

## Python version
Python 3.6.4

## Dependencies
Networkx

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

## Visibility Graph Algorithm
Implementations the following time series-to-graph algorithm which takes the time series as parameter and returns a networkx undirected graph.

1. ts2vg_basic
  
Reference: "From time series to complex networks: The visibility graph" by L. Lacasa, B. Luque, F. Ballesteros, J. Luque, and J. C. Nuno

2. ts2vg_fast
  
Reference: "Fast transformation from time series to visibility graphs" by Xin Lan, Hongming Mo, Shiyu Chen, Qi Liu, and Yong Deng

3. ts2hvg

Reference: "Horizontal visibility graphs: exact results for random time series" by B. Luque , L. Lacasa, F. Ballesteros and J. Luque

## How to install
Pytalib has not been published on Python Package Index (PyPi) yet. I will update this in the future.
But basically the procedure is same as follows:
```
pip install pytalib
```

## Example Code
#### Calculate indicators
```
from pytalib.indicators.trend import SimpleMovingAverage

prices = [1,2,3,4,5,6,7,8,9,10]
sma = SimpleMovingAverage(prices=prices, period=3)
result = sma.calculate()

# reuse sma object
prices2 = [10,9,8,7,6,5,4,3,2,1]
sma.reset(prices=prices2, period=3)
result2 = sma.calculate()
```

#### Time series-to-Graph transformation
```
import networkx as nx
from pytalib.graph import visibility_graph as vg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

prices = [1,3,2,4,5,6,9,8,9,10]
G = vg.ts2vg_fast(prices)
nx.draw_networkx(G, with_labels=True, font_weight='bold')
plt.title('visibility graph of prices')
plt.show()
```

<img src="https://github.com/dennis199441/pytalib/blob/master/example/vg.png" width="50%" height="50%">

```
import networkx as nx
from pytalib.graph import visibility_graph as vg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

prices = [1,3,2,4,5,6,9,8,9,10]
G = vg.ts2hvg(prices)
nx.draw_networkx(G, with_labels=True, font_weight='bold')
plt.title('horizontal visibility graph of prices')
plt.show()
```

<img src="https://github.com/dennis199441/pytalib/blob/master/example/hvg.png" width="50%" height="50%">

