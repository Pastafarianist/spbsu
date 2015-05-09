from __future__ import division
from math import sqrt
import sys


def solve_iterations(func, initial, eps, distfunc, maxiter):
	curr = initial
	for k in xrange(maxiter):
		sys.stdout.write("%2d: %.15f -> " % (k + 1, curr))
		next = func(curr)
		sys.stdout.write("%.15f" % (next))
		sys.stdout.write(", diff=%.15f, %.1f%% of eps\n" % \
		 (abs(curr - next), abs(curr - next)/eps))
		if distfunc(curr, next) < eps:
			return next
		curr = next
	raise RuntimeError("Iterations diverge!")

def solve_newton(func, dfunc, initial, eps, maxiter):
	curr = initial
	for k in xrange(maxiter):
		sys.stdout.write("%2d: %.15f -> " % (k + 1, curr))
		next = curr - func(curr)/dfunc(curr)
		sys.stdout.write("%.15f" % (next))
		sys.stdout.write(", diff=%.15f, %.1f%% of eps\n" % \
		 (abs(curr - next), abs(curr - next)/eps))
		if abs(curr - next) < eps:
			return next
		curr = next
	raise RuntimeError("Newton diverges!")

f = lambda x: sqrt(5-x**2) - 5/(x**2+5)
df = lambda x: -x / sqrt(-x**2 + 5) + 10 * x / (x**2 + 5)**2
F = lambda x: x - f(x) / df(2.2)
initial = 2.15
distfunc = lambda x, y: abs(x - y)
eps = 1e-12
maxiter = 30

ans = solve_iterations(F, initial, eps, distfunc, maxiter)
print "f(%.15f) = %.15f" % (ans, f(ans))

print

ans = solve_newton(f, df, initial, eps, maxiter)
print "f(%.15f) = %.15f" % (ans, f(ans))