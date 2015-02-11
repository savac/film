"""
Search parameter using log seach
"""
import sys
import math
import subprocess
from call_vw import call_vw
import math

phi = (1. + math.sqrt(5.)) / 2.;
resphi = 2. - phi;
best = float('inf')
f_best = float('inf')

def goldenSectionSearch(command, a, b, c, tau):
	global best
	global f_best
	if (c - b > b - a):
		x = b + resphi * (c - b)
	else:
		x = b - resphi * (b - a)
	  
	if (abs(c - a) < tau * (abs(b) + abs(x))):
		return math.pow(10, (c + a) / 2)
	
	print('Trying %f...' % math.pow(10, x), end='')
	f_x = call_vw(command, math.pow(10, x))
	if f_x < f_best:
		best = x
		f_best = f_x
	print('%f %s'%(f_x, '(best)' if best == x else ''))
	
	print('Trying %f...' % math.pow(10, b), end='')
	f_b = call_vw(command, math.pow(10, b))
	if f_b < f_best:
		best = b
		f_best = f_b
	print('%f %s'%(f_b, '(best)' if best == b else ''))
	
	if (f_x < f_b):
		if (c - b > b - a):
			return goldenSectionSearch(command, b, x, c, tau)
		else:
			return goldenSectionSearch(command, a, x, b, tau)
	else:
		if (c - b > b - a):
			return goldenSectionSearch(command, a, b, x, tau)
		else:
			return goldenSectionSearch(command, x, b, c, tau)
	
def score(command, min, guess, max, tau=1e-4):
	a = math.log10(min)
	b = math.log10(guess)
	c = math.log10(max)
	#b = a + resphi * (c - a)
	return goldenSectionSearch(command, a, b, c, tau)

if __name__ == '__main__':
	min = sys.argv[1]
	max = sys.argv[2]
	specified_tol = sys.argv[3].isnumeric()
	tolerance = sys.argv[3] if specified_tol else 1e-4

	vw_command = sys.argv[specified_tol + 3]
	
	if len(sys.argv) >= 3:
		vw_command = sys.argv[3]

	score(command, min, max, tolerance)