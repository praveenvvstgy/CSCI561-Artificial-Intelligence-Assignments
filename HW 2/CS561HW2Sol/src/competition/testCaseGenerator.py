import random

board_numbers = [random.randrange(1,101,1) for _ in range (800)]
for i in xrange(4,27):
	for j in xrange(3,4):
		output_file = open("input{0}-{1}.txt".format(i, j), "w")
		output_file.write(str(i) + "\n")
		output_file.write("COMPETITION\n")
		output_file.write("X\n")
		output_file.write(str(j) + "\n")
		board_pos = 0
		for k in xrange(0,i):
			for l in xrange(0,i):
				output_file.write(str(board_numbers[board_pos]) + " ")
				board_pos += 1
			output_file.write("\n")
		for k in xrange(0,i):
			for l in xrange(0,i):
				output_file.write(".")
			output_file.write("\n")
		output_file.close()