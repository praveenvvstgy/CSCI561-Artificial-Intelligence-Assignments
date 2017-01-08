import sys
import pickle
import numpy as np
import math

with open("timeTaken", 'rb') as f:
    timeTaken = pickle.load(f)

board_size = int(sys.argv[1])
cputime_remaining = float(sys.argv[2])
vacant_positions = float(sys.argv[3])

if board_size < 4:
	with open('depth', 'w') as f:
		f.write('%d' % board_size)
	exit(0)

# print timeTaken
timeTaken = timeTaken[board_size]
baseTime = timeTaken[3]

if cputime_remaining < baseTime:
	with open('depth', 'w') as f:
		f.write('%d' % 1)
	exit(0)

depth = 0
for i in xrange(4,10):
	ti = baseTime * ((vacant_positions) ** (i - 3))
	print i, "->", ti
	if ti > cputime_remaining:
		depth = i
		break
with open('depth', 'w') as f:
	f.write('{0}'.format(i))