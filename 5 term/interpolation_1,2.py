from __future__ import division
from math import factorial
import numpy as np
import matplotlib.pyplot as plt

ys = [0.1494, 0.2474, 0.3428, 0.4349, 0.5226, 0.6051, 0.6816, 0.7512, 0.8134]
ys = np.asarray(ys)
x1 = 0.15
h = 0.1

def product(lst):
	result = 1
	for v in lst:
		result *= v
	return result

def make_deltas(h, ys):
	n = len(ys)
	deltas = [ys]
	for k in xrange(1, n):
		layer = (deltas[k-1][1:] - deltas[k-1][:-1])# / (h * k)
		deltas.append(layer)
	return deltas

def interpolator_diffscheme(x1, h, ys):
	n = len(ys)
	diffs = [layer[0] for layer in make_deltas(h, ys)]
	# def kterm(k, x):
	# 	prod = product(x - (x1 + j*h) for j in xrange(k))
	# 	return diffs[k] * prod / (h**k * factorial(k))
	def kterm(k, x):
		t = (x - x1) / h
		prod = product(t - j for j in xrange(k))
		return diffs[k] * prod / (factorial(k))
	return lambda x: diffs[0] + sum(kterm(k, x) for k in xrange(1, n))

def print_deltas(h, ys):
	deltas = make_deltas(h, ys)
	for layer in deltas:
		print '\t'.join('%.4f' % v for v in layer)
	print '[' + ', '.join('%.4f' % layer[0] for layer in deltas) + ']'

def plot_interpolation(Pn, x1, h, ys):
	xs = np.linspace(x1, x1 + h * (len(ys) - 1), len(ys))
	vPn = np.vectorize(Pn)
	x = np.linspace(0, 1, 100)

	plt.plot(x, vPn(x), '-')
	plt.plot(xs, ys, 'ro')
	plt.ylim([0, 1])
	plt.show()

print_deltas(h, ys)
Pn = interpolator_diffscheme(x1, h, ys)
print Pn(0.31), Pn(0.79)
plot_interpolation(Pn, x1, h, ys)