from itertools import combinations
import math

def _concordance(x, y):
	if len(x) != len(y):
		raise Exception("vector x and vector y should have same length!")

	concordant = 0
	discordant = 0
	tied = 0
	for (i, j) in combinations(range(len(x)), 2):
		if (x[i] < x[j] and y[i] < y[j]) or (x[i] > x[j] and y[i] > y[j]) or (x[i] == x[j] and y[i] == y[j]):
			concordant += 1
		else:
			discordant += 1

	return (concordant, discordant)

def goodman_kruskal_gamma(x, y):
	concordant, discordant = _concordance(x, y)
	return (concordant - discordant) / (concordant + discordant)

def coarse_grain_series(series, s):
	if not series:
		raise Exception("coarse_grain_series error: `series` cannot be None!")
	if len(series) < s:
		raise Exception("coarse_grain_series error: `s` cannot be greater than the length of `series`!")

	result_series = []
	i = 0
	while i < len(series):
		if i + s >= len(series):
			result = sum(series[i:]) / (len(series) - i)
		else:
			result = sum(series[i: i + s]) / s
		result_series.append(result)
		i += s

	return result_series

def test_statistics(n, r):
	numerator = r * math.sqrt((n - 2))
	denominator = math.sqrt((1 - r ** 2))
	return (numerator / denominator)

def pearson_correlation(x, y):
	if len(x) != len(y):
		raise Exception("vector x and vector y should have same length!")

	xsquares = sum([i ** 2 for i in x])
	ysquares = sum([i ** 2 for i in y])

	product_sum = 0
	for i in range(len(x)):
		product_sum += x[i] * y[i]

	numerator = product_sum - ((sum(x) * sum(y))/len(x))
	denominator = math.sqrt((xsquares - (sum(x) * sum(x)) / len(x)) * (ysquares - (sum(y) * sum(y)) / len(x)))

	if denominator == 0:
		return 0

	return numerator / denominator
	
def euclidean_distance(x, y):
	if len(x) != len(y):
		raise Exception("vector x and vector y should have same length!")
	
	sqrted_sum = 0
	for i in range(len(x)):
		sqrted_sum += (x[i] - y[i]) ** 2

	return math.sqrt(sqrted_sum)

def cosine_similarity(x, y):
	if len(x) != len(y):
		raise Exception("vector x and vector y should have same length!")
	
	dp = 0
	xnorm = 0
	ynorm = 0
	for i in range(len(x)):
		dp += x[i] * y[i]
		xnorm += x[i] ** 2
		ynorm += y[i] ** 2

	return (dp / (math.sqrt(xnorm) * math.sqrt(ynorm)))