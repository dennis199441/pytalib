import networkx as nx
from .utils import *
from scipy.stats import t
def ts2hvg(series):
	"""
	convert time series to horizontal visibility graph

	Reference:
	B. Luque , L. Lacasa, F. Ballesteros and J. Luque, "Horizontal visibility graphs: exact results for random time series"
	"""
	hvg = nx.Graph()
	hvg.add_nodes_from([i for i in range(len(series))])
	stack = []
	for i in range(len(series)):
		if not stack:
			stack.append((i , series[i]))
		elif stack[-1][1] > series[i]:
			hvg.add_edge(stack[-1][0], i)
			stack.append((i , series[i]))
		else:
			while stack and stack[-1][1] < series[i]:
				hvg.add_edge(i, stack.pop()[0])
			if stack:
				hvg.add_edge(stack[-1][0], i)
			stack.append((i , series[i]))
	
	return hvg

def ts2vg_basic(series):
	"""
	convert time series to visibility graph

	Reference:
	L. Lacasa, B. Luque, F. Ballesteros, J. Luque, and J. C. Nuno, "From time series to complex networks: The visibility graph" Proc. Natl. Acad. Sci. U.S.A. 105, 4972–4975 (2008)
	"""
	vg = nx.Graph()
	vg.add_nodes_from([i for i in range(len(series))])

	for i in range(len(series)):
		y_from = series[i]
		max_slope = None
		for j in range(i + 1, len(series)):
			y_to = series[j]
			slope = (y_to - y_from) / (j - i)
			if max_slope is None or (max_slope is not None and slope > max_slope):
				max_slope = slope
				vg.add_edge(i, j)

	return vg

def ts2vg_fast(series):
	"""
	convert time series to visibility graph using divide and conquer strategy

	Reference:
	Xin Lan, Hongming Mo, Shiyu Chen, Qi Liu, and Yong Deng, "Fast transformation from time series to visibility graphs" American Institute of Physics, Chaos 25, 083105 (2015)
	"""
	vg = nx.Graph()
	vg.add_nodes_from([i for i in range(len(series))])
	ts2vg_fast_helper(vg, series, 0, len(series) - 1)
	return vg

def ts2vg_fast_helper(graph, series, left, right):
	if left < right and len(series[left : right + 1]) > 1:
		k = series[left : right + 1].index(max(series[left : right + 1])) + left
		y_from = series[k]
		min_slope_left = None
		max_slope_right = None

		for i in range(k - 1, left - 1, -1):
			y_to = series[i]
			slope = (y_to - y_from) / (i - k)
			if min_slope_left is None or (min_slope_left is not None and slope < min_slope_left):
				min_slope_left = slope
				graph.add_edge(k, i)

		for i in range(k + 1, right + 1):
			y_to = series[i]
			slope = (y_to - y_from) / (i - k)
			if max_slope_right is None or (max_slope_right is not None and slope > max_slope_right):
				max_slope_right = slope
				graph.add_edge(k, i)

		ts2vg_fast_helper(graph, series, left, k - 1)
		ts2vg_fast_helper(graph, series, k + 1, right)

def mhvgca_method(series_a, series_b, timescale=20):
	"""
	multiscale horizontal-visibility-graph correlation analysis

	Reference:
	Weidong Li and Xiaojun Zhao, "Multiscale horizontal-visibility-graph correlation analysis of stock time series" 2018 EPL 122 40007
	"""
	if len(series_a) != len(series_b):
		raise Exception("`series_a` and `series_b` should have the same length! {} != {}".format(len(series_a), len(series_b)))
	
	degree_distribution_a = {}
	degree_distribution_b = {}
	G_s = []
	P_s = []
	for s in range(1, timescale + 1):
		grained_a = coarse_grain_series(series_a, s)
		grained_b = coarse_grain_series(series_b, s)
		hvg_a = ts2hvg(grained_a)
		hvg_b = ts2hvg(grained_b)
		degree_sequence_a = [d for n, d in hvg_a.degree()]
		degree_sequence_b = [d for n, d in hvg_b.degree()]

		correlation_coefficient = goodman_kruskal_gamma(degree_sequence_a, degree_sequence_b)
		df = len(degree_sequence_a) - 2
		try:
			t_stat = test_statistics(len(degree_sequence_a), correlation_coefficient)
			pvalue = 2 * (1 - t.cdf(abs(t_stat), df))
		except:
			pvalue = 1

		P_s.append(pvalue)
		G_s.append(correlation_coefficient)

	return G_s, P_s
