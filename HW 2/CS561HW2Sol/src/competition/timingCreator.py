from shutil import copyfile
from subprocess import call
import timeit
import numpy as np
import pickle

timeTaken = dict()

for i in xrange(4,27):
	timeTaken[i] = dict()
	for j in xrange(3, 4):
		copyfile("input{0}-{1}.txt".format(i, j), "input.txt")
		start_time = timeit.default_timer()
		call("./backup")
		timeTaken[i][j] = timeit.default_timer() - start_time
	with open("timeTaken", 'wb') as f:
 		pickle.dump(timeTaken, f)

