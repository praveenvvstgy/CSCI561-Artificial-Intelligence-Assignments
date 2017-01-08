import timeit
import subprocess
import random


x_folder = "p1"
o_folder = "p2"

p = subprocess.Popen(["make", "agent"], cwd=x_folder)
p.wait()
p = subprocess.Popen(["make", "agent"], cwd=o_folder)
p.wait()
p = subprocess.Popen(["make", "calibrate"], cwd=x_folder)
p.wait()
p = subprocess.Popen(["make", "calibrate"], cwd=o_folder)
p.wait()

x_positions = []
o_positions = []

x_time = 200
o_time = 200

next_to_play = "X"

board_size = 4

scores = []

board_numbers = [random.randrange(1,101,1) for _ in range (800)]
def create_input_file(x_positions, o_positions, i, player, time_remaining):
	output_file = open("input.txt", "w")
	output_file.write(str(i) + "\n")
	output_file.write("COMPETITION\n")
	output_file.write(player + "\n")
	output_file.write(str(time_remaining) + "\n")
	board_pos = 0
	for k in xrange(0,i):
		scores.append([])
		for l in xrange(0,i):
			scores[k].append(board_numbers[board_pos])
			output_file.write(str(board_numbers[board_pos]) + " ")
			board_pos += 1
		output_file.write("\n")
	for k in xrange(0,i):
		for l in xrange(0,i):
			if (k, l) in x_positions:
				output_file.write("X")
			elif (k, l) in o_positions:
				output_file.write("O")
			else:
				output_file.write(".")
		output_file.write("\n")
	output_file.close()

def terminal_test(vacant_positions, x_positions, o_positions):
	return (len(vacant_positions) == 0) or (x_time <= 0) or (o_time <= 0)

create_input_file(x_positions, o_positions, board_size, "X", 200)
vacant_positions = []
for k in xrange(0,board_size):
		for l in xrange(0,board_size):
			vacant_positions.append((k ,l))

def run_program(folder):
	# print "Copying input file to ", folder
	p = subprocess.Popen(["cp", "../input.txt", "."], cwd=folder)
	p.wait()
	# print "Running Program"
	start_time = timeit.default_timer()
	p = subprocess.Popen(["make", "run"], cwd=folder)
	p.wait()
	time_taken = timeit.default_timer() - start_time
	print "Copying output file from", folder, " to main folder"
	p = subprocess.Popen(["cp", "output.txt", "../"], cwd=folder)
	p.wait()
	print "Time taken is ", str(time_taken), " seconds"
	return time_taken

while not terminal_test(vacant_positions, x_positions, o_positions):
	if next_to_play == "X":
		print "*" * 30
		print "X is playing"
		time_taken = run_program(x_folder)
		x_time -= time_taken
		next_to_play = "O"
	else:
		print "*" * 30
		print "O is playing"
		time_taken = run_program(o_folder)
		o_time -= time_taken
		next_to_play = "X"
	output_lines = []
	with open('output.txt', 'r') as output_file:
		for i, line in enumerate(output_file):
			if i > 0:
				output_lines.append(line)
	with open("input.txt", 'r') as input_file:
		input_data = input_file.readlines()
	linecount = 0
	for i, line in enumerate(output_lines):
		input_data[i + 4 + board_size] = line
	input_data[2] = next_to_play + "\n"
	if next_to_play == "X":
		input_data[3] = str(x_time) + "\n"
	else:
		input_data[3] = str(o_time) + "\n"
	with open('input.txt', 'w') as input_file:
		input_file.writelines(input_data)
	with open("output.txt", 'r') as fin:
		print fin.read()
	vacant_positions = []
	x_positions = []
	o_positions = []
	output_lines = []
	print "<<>>>"
	with open('output.txt', 'r') as output_file:
		for i, line in enumerate(output_file):
			if i > 0:
				output_lines.append(list(line))
	for k in xrange(0,board_size):
		for l in xrange(0,board_size):
			if output_lines[k][l] == "X":
				x_positions.append((k, l))
			elif output_lines[k][l] == "O":
				o_positions.append((k, l))
			else:
				vacant_positions.append((k, l))

if x_time == 0:
	print "O is the winner, X timedout"
elif o_time == 0:
	print "X is the winner, O timedout"
else:
	x_score = 0
	o_score = 0
	for k in xrange(0,board_size):
		for l in xrange(0,board_size):
			if output_lines[k][l] == "X":
				x_score += scores[k][l]
			elif output_lines[k][l] == "O":
				o_score += scores[k][l]
	if x_score > o_score:
		print "X is the winner"
	else:
		print "O is the winner"

p = subprocess.Popen(["make", "newgame"], cwd=x_folder)
p.wait()
p = subprocess.Popen(["make", "newgame"], cwd=o_folder)
p.wait()




