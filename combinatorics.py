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

def print_gray_code_recursive(n):
	""" Gray code is a sequence of binary numbers of fixed length
	where every next number differs from the previous one in just
	one digit. Obviously, the two possible Gray codes of length 1
	are (0, 1) and (1, 0). Now, if we know how to make Gray codes
	of length (n), it's easy to make them one digit longer. We could
	take two copies of a sequence of codes of length (n), reverse one
	of them and concatenate. The resulting sequence will still be a
	Gray code with one exception at the boundary between sequences.
	Now, we can append a zero to the first part and a one to the
	second. At any position, say, at the end. Now the sequence contains
	numbers of length (n+1) and it still remains a Gray code.
	The implementation here relies on this:
	- step(pos) prints all Gray codes of length (n-pos) with a fixed prefix,
	  namely everything before (pos)
	- when called twice with on the same suffix, it prints the code
	  first in direct order, then in reverse order """
	def step(pos):
		if pos == n: # recursion end reached
			print ''.join(str(v) for v in s)
			return
		step(pos + 1)
		s[pos] = 1 - s[pos] # makes the second property work
		step(pos + 1)
	s = [0] * n
	step(0)

def print_gray_code_iterative(n):
	""" The idea here is to observe that the position of the changing
	digit in Gray codes is the same as the position of the leftmost changing
	digit in natural binary numbers. """
	s = [0] * n
	index = 0 # of the currently printed code
	flip_at = 0
	temp = 0 # we're doing Pascal here
	# probably one of the few chances for Pascal to have an advantage
	# is the absence of (repeat...until) in Python
	while True:
		print ''.join(str(v) for v in s)
		# now we want to calculate (flip_at) for the next iteration
		# it equals the number of 1's at the end of (index), plus 1
		# which, in turn, equals the number of 0's at the end of (index+1)
		index += 1 # updating now, so there's no need to calculate it twice
		flip_at = 0
		temp = index
		while temp % 2 == 0: # while the last digit is zero
			temp //= 2 # shift one digit to the right
			flip_at += 1 # and update the counter
		# here we go, a replacement
		if flip_at >= n: # we've gone too far
			break
		s[flip_at] = 1 - s[flip_at]



def print_gray_code_iterative_bitmagic(n):
	""" The basic idea is the same, however, there is considerably
	more magic going on. """
	s = 0
	index = 0
	flip_at = -1
	while True:
		print bin(s)[2:].zfill(n)
		index += 1
		flip_at = (index ^ (index - 1)) & index
		if flip_at & (1 << n):
			break
		s ^= flip_at


def test():
	n = 3
	print_permutations_nonrecursive(n)
	print '-' * 16
	print_permutations_recursive(n)
	print '-' * 16
	print_subsets_lexicographically(n)
	print '-' * 16
	print_gray_code_recursive(n)
	print '-' * 16
	print_gray_code_iterative(n)
	print '-' * 16
	print_gray_code_iterative_bitmagic(n)

if __name__ == '__main__':
	test()
