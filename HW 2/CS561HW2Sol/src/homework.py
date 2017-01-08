#! ../bin/python
import sys

def deepcopy(org):
    return [row[:] for row in org]

class Game():
	def __init__(self, n, maxdepth, scores, vacant_positions, x_positions, o_positions, youplay, to_play, depth):
		self.n = n
		self.maxdepth = maxdepth
		self.scores = scores
		self.vacant_positions = vacant_positions
		self.x_positions = x_positions
		self.o_positions = o_positions
		
		self.youplay = youplay
		self.to_play = to_play
		self.depth = depth

	def actions(self):
		actions = []
		actions += map(lambda x: (x, "stake"), self.vacant_positions)
		if self.to_play == "X":
			for (x, y) in self.x_positions:
				if (x-1, y) in self.vacant_positions:
					actions.append(((x-1, y), "raid"))
				if (x+1, y) in self.vacant_positions:
					actions.append(((x+1, y), "raid"))
				if (x, y-1) in self.vacant_positions:
					actions.append(((x, y-1), "raid"))
				if (x, y+1) in self.vacant_positions:
					actions.append(((x, y+1), "raid"))
		else:
			for (x, y) in self.o_positions:
				if (x-1, y) in self.vacant_positions:
					actions.append(((x-1, y), "raid"))
				if (x+1, y) in self.vacant_positions:
					actions.append(((x+1, y), "raid"))
				if (x, y-1) in self.vacant_positions:
					actions.append(((x, y-1), "raid"))
				if (x, y+1) in self.vacant_positions:
					actions.append(((x, y+1), "raid"))
				
		## print "Available Actions for " + self.to_play + " are "
		## print actions
		## print "*"*50
		return actions

	def terminal_test(self):
		return ((self.n*self.n) == (len(self.x_positions) + len(self.o_positions))) or (self.depth == self.maxdepth)

	def result(self, move):
		(x, y) = move[0]
		if move[1] == "stake":
			## print "Considering a Stake Move for " + self.to_play + " at position (" + str(x) + ", " + str(y) + ")"
			if self.to_play == "X":
				tmp_vacant_positions = deepcopy(self.vacant_positions)
				tmp_x_positions = deepcopy(self.x_positions)
				tmp_o_positions = deepcopy(self.o_positions)
				tmp_vacant_positions.remove((x, y))
				tmp_x_positions.append((x, y))
				## print "*"*50
				return Game(n, self.maxdepth, self.scores, tmp_vacant_positions, tmp_x_positions, tmp_o_positions, self.youplay, "O", self.depth + 1)
			else:
				tmp_vacant_positions = deepcopy(self.vacant_positions)
				tmp_x_positions = deepcopy(self.x_positions)
				tmp_o_positions = deepcopy(self.o_positions)
				tmp_vacant_positions.remove((x, y))
				tmp_o_positions.append((x, y)) 
				## print "*"*50
				return Game(n, self.maxdepth, self.scores, tmp_vacant_positions, tmp_x_positions, tmp_o_positions, self.youplay, "X", self.depth + 1)
		else:
			## print "Considering a raid Move for " + self.to_play + " at position (" + str(x) + ", " + str(y) + ")"
			if self.to_play == "X":
				tmp_vacant_positions = deepcopy(self.vacant_positions)
				tmp_x_positions = deepcopy(self.x_positions)
				tmp_o_positions = deepcopy(self.o_positions)
				tmp_vacant_positions.remove((x, y))
				tmp_x_positions.append((x, y))
				if y > 0:
					if (x, y-1) in self.o_positions:
						## print "X will raid O at (" + str(x) + ", " + str(y-1) + ")"
						tmp_o_positions.remove((x, y - 1))
						tmp_x_positions.append((x, y - 1))
				if y < n-1:
					if (x, y+1) in self.o_positions:
						## print "X will raid O at (" + str(x) + ", " + str(y+1) + ")"
						tmp_o_positions.remove((x, y + 1))
						tmp_x_positions.append((x, y + 1))
				if x > 0:
					if(x-1, y) in self.o_positions:
						## print "X will raid O at (" + str(x-1) + ", " + str(y) + ")"
						tmp_o_positions.remove((x - 1, y))
						tmp_x_positions.append((x - 1, y))
				if x < n-1:
					if(x+1, y) in self.o_positions:
						## print "X will raid O at (" + str(x+1) + ", " + str(y) + ")"
						tmp_o_positions.remove((x + 1, y))
						tmp_x_positions.append((x + 1, y))
				## print "*"*50
				return Game(n, self.maxdepth, self.scores, tmp_vacant_positions, tmp_x_positions, tmp_o_positions, self.youplay, "O", self.depth + 1)
			else:
				tmp_vacant_positions = deepcopy(self.vacant_positions)
				tmp_x_positions = deepcopy(self.x_positions)
				tmp_o_positions = deepcopy(self.o_positions)
				tmp_vacant_positions.remove((x, y))
				tmp_o_positions.append((x, y))
				if y > 0:
					if (x, y-1) in self.x_positions:
						## print "O will raid X at (" + str(x) + ", " + str(y-1) + ")"
						tmp_x_positions.remove((x, y - 1))
						tmp_o_positions.append((x, y - 1))
				if y < n-1:
					if (x, y+1) in self.x_positions:
						## print "O will raid X at (" + str(x) + ", " + str(y+1) + ")"
						tmp_x_positions.remove((x, y + 1))
						tmp_o_positions.append((x, y + 1))
				if x > 0:
					if(x-1, y) in self.x_positions:
						## print "O will raid X at (" + str(x-1) + ", " + str(y) + ")"
						tmp_x_positions.remove((x - 1, y))
						tmp_o_positions.append((x - 1, y))
				if x < n-1:
					if(x+1, y) in self.x_positions:
						## print "O will raid X at (" + str(x+1) + ", " + str(y) + ")"
						tmp_x_positions.remove((x + 1, y))
						tmp_o_positions.append((x + 1, y))
				## print "*"*50
				return Game(n, self.maxdepth, self.scores, tmp_vacant_positions, tmp_x_positions, tmp_o_positions, self.youplay, "X", self.depth + 1)

	def utility(self):
		just_played = "X" if self.to_play == "O" else "O"
		## print "="*25
		## print "Result when " + just_played + " makes a move"
		## for x in xrange(0,n):
		## 	for y in xrange(0,n):
		## 		if (x, y) in self.x_positions:
		## 			sys.stdout.write(" X ")
		## 		elif (x, y) in self.o_positions:
		## 			sys.stdout.write(" O ")
		## 		else:
		## 			sys.stdout.write(" . ")
			## print
		x_score = 0
		for (x,y) in self.x_positions:
			x_score += self.scores[x][y]
		o_score = 0
		for (x, y) in self.o_positions:
			o_score += self.scores[x][y]
		## print "x_score = " + str(x_score)
		## print "o_score = " + str(o_score)
		if self.youplay == "X":
			## print "score = " + str(x_score - o_score)
			## print "="*25
			return x_score - o_score
		else:
			## print "score = " + str(o_score - x_score)
			## print "="*25
			return o_score - x_score

def min_value(state):
	if state.terminal_test():
		## print "="*20
		## print "Terminal Test Passed in Min Value"
		## print "="*20
		return state.utility()
	else:
		## print "="*20
		## print "Terminal Test Passed in Max Value"
		## print "="*20
		v = float("inf")
		for a in state.actions():
			v = min(v, max_value(state.result(a)))
		return v

def max_value(state):
	if state.terminal_test():
		return state.utility()
	else:
		v = -float("inf")
		for a in state.actions():
			v = max(v, min_value(state.result(a)))
		return v

def minimax_decision(state):
	## print "="*50
	## print "GAMEPLAYING BEGINS"
	## print "="*50
	return max(state.actions(), key = lambda a: min_value(state.result(a)))

# Alpha Beta Search
def ab_max_value(state, alpha, beta):
	if state.terminal_test():
		return state.utility()
	else:
		v = -float('inf')
		for a in state.actions():
			v = max(v, ab_min_value(state.result(a), alpha, beta))
			if v >= beta:
				return v
			alpha = max(alpha, v)
		return v

def ab_min_value(state, alpha, beta):
	if state.terminal_test():
		return state.utility()
	v = float('inf')
	for a in state.actions():
		v = min(v, ab_max_value(state.result(a), alpha, beta))
		if v <= alpha:
			return v
		beta = min(beta, v)
	return v

def alpha_beta_search(state):
	alpha, beta = -float('inf'), float('inf')
	selected_action = None
	for action in state.actions():
		v = ab_min_value(state.result(action), alpha, beta)
		if v > alpha:
			alpha = v
			selected_action = action
	return selected_action

input_file = open("input.txt", "r")

n = int(input_file.readline().strip())
## print "n is " + str(n)

mode = input_file.readline().strip()
## print "mode is " + mode

youplay = input_file.readline().strip()
## print "youplay is " + youplay

depth = int(input_file.readline().strip())
## print "depth is " + str(depth)

scores = []
for i in xrange(0,n):
	row = map(int, input_file.readline().strip().split())
	scores.append(row)

## print "Scores Grid is"
## print scores

board_state = []
for i in xrange(0,n):
	row = list(input_file.readline().strip())
	board_state.append(row)

vacant_positions = []
x_positions = []
o_positions = []
for x in xrange(0, n):
	for y in xrange(0, n):
		if board_state[x][y] != '.':
			if board_state[x][y] == "X":
				x_positions.append((x, y))
			else:
				o_positions.append((x, y))
		else:
			vacant_positions.append((x, y))
		

## print "Board State is "
## print board_state
		
game_state = Game(n, depth, scores, vacant_positions, x_positions, o_positions, youplay, youplay, 0)
if mode == "MINIMAX":
	((x, y), move) = minimax_decision(game_state)
	print chr(97 + y) + str(x + 1) + " " + move
	output_file = open("output.txt", "w")
	output_file.write((chr(97 + y).upper() + str(x + 1) + " " + move.title()) + "\n")
	output_state = game_state.result(((x, y), move))
	for x in xrange(0,n):
		for y in xrange(0,n):
			if (x, y) in output_state.x_positions:
				output_file.write("X")
			elif (x, y) in output_state.o_positions:
				output_file.write("O")
			else:
				output_file.write(".")
		if not x == n - 1:
			output_file.write("\n")
	output_file.close()
else:
	((x, y), move) = alpha_beta_search(game_state)
	print chr(97 + y) + str(x + 1) + " " + move
	output_file = open("output.txt", "w")
	output_file.write((chr(97 + y).upper() + str(x + 1) + " " + move.title()) + "\n")
	output_state = game_state.result(((x, y), move))
	for x in xrange(0,n):
		for y in xrange(0,n):
			if (x, y) in output_state.x_positions:
				output_file.write("X")
			elif (x, y) in output_state.o_positions:
				output_file.write("O")
			else:
				output_file.write(".")
		if not x == n - 1:
			output_file.write("\n")
	output_file.close()