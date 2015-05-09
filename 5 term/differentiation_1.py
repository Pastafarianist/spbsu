from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt


ys = [-0.20136, 0.0, 0.20136, 0.41152, 0.64350]
ys = np.asarray(ys)
x1 = -0.2
h = 0.2
xs = np.linspace(x1, x1 + h * (len(ys) - 1), len(ys))
print(xs)
print(ys)

x0k = 2 # x0 = 0.2

def left_d(xs, ys, k):
	return (ys[k] - ys[k-1]) / (xs[k] - xs[k-1])

def right_d(xs, ys, k):
	return (ys[k] - ys[k+1]) / (xs[k] - xs[k+1])

def center_d(xs, ys, k):
	return (ys[k+1] - ys[k-1]) / (xs[k+1] - xs[k-1])

def second_d(xs, ys, k):
	return (ys[k+1] - 2*ys[k] + ys[k-1]) / ((xs[k+1]-xs[k]) * (xs[k] - xs[k-1]))

print(left_d(xs, ys, x0k))
print(right_d(xs, ys, x0k))
print(center_d(xs, ys, x0k))
print(second_d(xs, ys, x0k))

plt.plot(xs, ys, 'ro')
plt.xlim([-0.3, 0.7])
plt.ylim([-1, 1])
plt.show()
