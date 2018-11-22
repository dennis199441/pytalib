from itertools import combinations

def _concordance(x, y):
	if len(x) != len(y):
		raise Exception("vector x and vector y should have same length!")

	concordant = 0
	discordant = 0
	tied = 0
	for (i, j) in combinations(range(len(x)), 2):
		if (x[i] < x[j] and y[i] < y[j]) or (x[i] > x[j] and y[i] > y[j]):
			concordant += 1
		else:
			discordant += 1

	return (concordant, discordant)

def goodman_kruskal_gamma(x, y):
	concordant, discordant = _concordance(x, y)
	return (concordant - discordant) / (concordant + discordant)
