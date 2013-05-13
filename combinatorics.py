def make_next_permutation(p):
	""" The algorithm works as follows: first, we find the longest
	decreasing suffix of the permutation. If the entire permutation
	is decreasing, then it is the last one. Otherwise, we take the
	element just before the suffix, say A, and find in the suffix the
	smallest element that is greater than A. We swap these two elements
	and reverse the suffix. """
	for before_tail in reversed(xrange(len(p) - 1)):
		if p[before_tail] < p[before_tail + 1]: # found tail
			# now we have to traverse the tail again
			# binary search is probably better in terms of performance
			# but it is more difficult to implement properly
			# and the module 'bisect' is unavailable in Pascal
			# besides, we're dealing with like 10-element arrays here
			for to_swap in reversed(xrange(len(p))):
				if p[before_tail] < p[to_swap]:
					# the following two lines make me love Python
					p[before_tail], p[to_swap] = p[to_swap], p[before_tail]
					p[before_tail+1:] = reversed(p[before_tail+1:])
					return True # I lied, it's three
			else:
				raise RuntimeError("This should never happen")
	return False

def print_permutations_nonrecursive(n):
	p = range(1, n + 1)
	print p
	while make_next_permutation(p):
		print p

def print_permutations_recursive(n):
	""" I was staring at this algorithm for a couple of hours before
	the realization of what's going on started to dawn upon me. It's
	probably best to clarify a few assumptions which make the whole
	thing work. First, the tail which the function 'step' receives
	is always sorted in ascending order. Second, step(k) does two things:
	- prints all permutations of the tail with the first k elements fixed
	- reverses the tail
	So, to print all permutations of the (k-1)th tail one has to do
	the following:
	- supply step(k) with all possible selections of elements
	  in the (k-1)th tail, each being sorted, of course
	- after each call, undo the reversing
	To fulfill the first task, one may just remove each element from the tail,
	one after another, and replace them with the (k-1)th element. That is
	effectively done by putting all elements from the tail into the (k-1)th
	position, one by one. """
	def step(tail_start):
		# if the tail has just one element, print what we've got
		if tail_start == n - 1:
			print p
			return
		# try all possible selections of n elements from a total of (n+1)
		for to_swap in xrange(tail_start + 1, n):
			step(tail_start + 1) # now the tail is reversed
			p[tail_start+1:] = reversed(p[tail_start+1:]) # undoing that
			p[to_swap], p[tail_start] = p[tail_start], p[to_swap]
		step(tail_start + 1) # not reversing after the last time
	p = range(1, n + 1)
	step(0)

def print_subsets_lexicographically(n):
	""" A very simple algorithm for generating all subsets of a set
	with n elements. The representation of a subset is a bitmask of
	the elements it includes, that is, it contains a 0 at the n-th
	position if the element is not in the subset, and a 1 otherwise.
	We start with the empty subset. Its representation contains n
	zeros. Now, this sequence of zeros may be interpreted as a binary
	number. Moreover, every subset has a corresponding binary number
	in the range between 0 and (2^(n+1) - 1). So to print all possible
	subsets, or, which is the same, all numbers in that range, we may
	just keep adding 1 to the current number until we reach 2^(n+1). The
	algorithm below does exactly that. Only it stores the number in
	the reverse order. It's more convenient to do calculations that way. """
	s = [0] * (n + 1) # start off with zero
	while s[n] == 0: # check if 2^(n+1) is reached
		print ''.join(str(v) for v in s[:n])
		# The only tricky part: to add 1 to a binary number we may look at the
		# pencil-and-paper algorithm and see what's going on.
		# What is essentially happening is the following:
		# - if the number ends in 0, that 0 is going to be changed to 1
		# - otherwise, the ending of the number looks like 011...11
		#   in that case, we flip all 1's to 0's
		#   and that lonely zero changes to one
		pos = 0
		while s[pos] == 1:
			s[pos] = 0
			pos += 1
		s[pos] = 1


def test():
	n = 3
	print_permutations_nonrecursive(n)
	print '-' * 16
	print_permutations_recursive(n)
	print '-' * 16
	print_subsets_lexicographically(n)

if __name__ == '__main__':
	test()
