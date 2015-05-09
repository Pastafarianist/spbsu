from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt

k = 5
a = 123 + 0.05*k
h = 0.05
L = 0.5

A = np.matrix([
	[-125, a],
	[a, -123]
])
y0 = np.matrix([[1], [1]])
xs = np.linspace(0, L, L/h + 1)

def matrix_powers(M, y0, n):
	"""Calculates [y0, M*y0, M^2*y0, ..., M^(n-1)*y0]."""
	y = np.empty((len(y0), n))
	y[:, 0:1] = y0
	for i in xrange(n-1):
		y[:, i+1:i+2] = M * y[:, i:i+1]
	return y

def explicit_euler(A, y0, h, L):
	n = int(L/h) + 1
	M = np.eye(2) + h * A
	return matrix_powers(M, y0, n)

def implicit_euler(A, y0, h, L):
	n = int(L/h) + 1
	M = np.linalg.inv(np.eye(2) - h * A)
	return matrix_powers(M, y0, n)

def trapezoidal_euler(A, y0, h, L):
	n = int(L/h) + 1
	M = np.linalg.inv(np.eye(2) - (h/2)*A) * (np.eye(2) + (h/2)*A)
	return matrix_powers(M, y0, n)

# Stability
L = np.linalg.eigvals(A)
print([l for l in L]) # Explicit Euler
print([1/(1-h*l) for l in L]) # Implicit Euler
print([1/(1-(h/2)*l) * (1+(h/2)*l) for l in L]) # InterpAdams2

def solve_quadratic(a, b, c):
	D = b**2 - 4*a*c
	if D > 0:
		x1 = (-b - np.sqrt(D))/(2*a)
		x2 = (-b + np.sqrt(D))/(2*a)
		return x1, x2
	else:
		raise ValueError('2hard2try')

print([solve_quadratic(1, -(1 + 3/2 * h*l), (h*l)/2) for l in L]) # ExtrapAdams2
print([solve_quadratic((1-(h*l)/12), -(1 + 2/3 * h*l), (h*l)/12) for l in L]) # InterpAdams3
exit()

y_exp = explicit_euler(A, y0, h, L)
print(y_exp.T)
y_imp = implicit_euler(A, y0, h, L)
print(y_imp.T)
y_tra = trapezoidal_euler(A, y0, h, L)
print(y_tra.T)

# Computed with Mathematica
y1_exact = np.vectorize(lambda t: 0.00407312*np.exp(-248.*t)*(np.exp(0.745943*t) + 244.512*np.exp(247.254*t)))
y2_exact = np.vectorize(lambda t: -0.0040402*np.exp(-248.*t)*(np.exp(0.745943*t) - 248.512*np.exp(247.254*t)))

plt.plot(y_exp[0, :], y_exp[1, :], 'ro')
plt.plot(y_imp[0, :], y_imp[1, :], 'gs')
plt.plot(y_tra[0, :], y_tra[1, :], 'bd')
plt.plot(y1_exact(xs), y2_exact(xs), 'y^')
plt.plot(y1_exact(xs), y2_exact(xs), 'y--')
plt.xlim([0.65, 1.05])
plt.ylim([0.65, 1.05])
plt.show()