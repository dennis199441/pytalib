import networkx as nx

def ts2hvg(series):
	pass
	
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
