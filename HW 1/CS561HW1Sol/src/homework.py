#! ../bin/python

from Queue import *
import heapq

class Node():
	def __init__(self, state, parent, children, depth, path_cost, path):
		self.state = state
		self.parent = parent
		self.children = children
		self.depth = depth
		self.path_cost = path_cost
		self.path = path
	def __eq__(self, other):
		return self.state == other.state

class State():
	def __init__(self, name, cost):
		self.name = name
		self.cost = cost

	def __eq__(self, other):
		return self.name == other.name

	def __repr__(self):
		return "<State name:%s cost:%s" % (self.name, self.cost)

class Problem():
	def __init__(self, start, goal, graph):
		self.start = start
		self.goal = goal
		self.graph = graph

	def satisfies_goal_test(self, node):
		if node.state == self.goal:
			return True
		else:
			return False

	def expand(self, node):
		state_name = node.state
		if state_name in self.graph:
			children = self.graph[state_name]
			children_nodes = []
			for child in children:
				child_node = Node(child.name, node, None, node.depth + 1, node.path_cost + int(child.cost), node.path + [child.name])
				children_nodes.append(child_node)
			return children_nodes
		else:
			return None

class CustomPriorityQueue():
	def __init__(self):
		self.queue = []
		self.counter = 0

	def put(self, item, priority):
		heapq.heappush(self.queue, (priority, self.counter, item))
		self.counter += 1

	def get(self):
		return heapq.heappop(self.queue)[-1]

	def pop(self, state):
		index, _ = get_node(map(lambda x: x[-1], self.queue), state)
		self.queue.pop(index)

	def empty(self):
		return len(self.queue) == 0
		

def breadth_first_search(input_problem):
	initial_state = input_problem.start
	node = Node(initial_state, None, None, 0, 0, [initial_state])
	nodes = Queue()
	nodes.put(node)
	while True:
		if nodes.empty():
			return None
		else:
			node = nodes.get()
			if input_problem.satisfies_goal_test(node):
				return node
			else:
				expanded_nodes = input_problem.expand(node)
				node.children = expanded_nodes
				if expanded_nodes is not None:
					map(lambda x: nodes.put(x), expanded_nodes)

def uniform_cost_search(input_problem):
	initial_state = input_problem.start
	node = Node(initial_state, None, None, 0, 0, [initial_state])
	open_set = []
	nodes = CustomPriorityQueue()
	nodes.put(node, node.path_cost)
	open_set.append(node)
	closed_set = []
	while True:
		if nodes.empty():
			return None
		else:
			curnode = nodes.get()
			open_set.remove(curnode)
			if input_problem.satisfies_goal_test(curnode):
				return curnode
			else:
				children = input_problem.expand(curnode)
				while children:
					child = children.pop(0)
					if contains_node(open_set, child.state):
						index, node = get_node(open_set, child.state)
						if node.path_cost > child.path_cost:
							open_set.pop(index)
							nodes.pop(node.state)
							open_set.append(child)
							nodes.put(child, child.path_cost)
					elif contains_node(closed_set, child.state):
						index, node = get_node(closed_set, child.state)
						if node.path_cost > child.path_cost:
							closed_set.pop(index)
							open_set.append(child)
							nodes.put(child, child.path_cost)
					else:
						open_set.append(child)
						nodes.put(child, child.path_cost)
				closed_set.append(curnode)

def astar_search(input_problem):
	initial_state = input_problem.start
	node = Node(initial_state, None, None, 0, 0, [initial_state])
	open_set = []
	nodes = CustomPriorityQueue()
	nodes.put(node, node.path_cost + heuristic[node.state])
	open_set.append(node)
	closed_set = []
	while True:
		if nodes.empty():
			return None
		else:
			curnode = nodes.get()
			open_set.remove(curnode)
			if input_problem.satisfies_goal_test(curnode):
				return curnode
			else:
				children = input_problem.expand(curnode)
				while children:
					child = children.pop(0)
					if contains_node(open_set, child.state):
						index, node = get_node(open_set, child.state)
						if node.path_cost > child.path_cost:
							open_set.pop(index)
							nodes.pop(node.state)
							open_set.append(child)
							nodes.put(child, child.path_cost + heuristic[child.state])
					elif contains_node(closed_set, child.state):
						index, node = get_node(closed_set, child.state)
						if node.path_cost > child.path_cost:
							closed_set.pop(index)
							open_set.append(child)
							nodes.put(child, child.path_cost + heuristic[child.state])
					else:
						open_set.append(child)
						nodes.put(child, child.path_cost + heuristic[child.state])
			closed_set.append(curnode)

def depth_first_search(input_problem):
	initial_state = input_problem.start
	node = Node(initial_state, None, None, 0, 0, [initial_state])
	nodes = []
	nodes.append(node)
	explored_set = []
	while True:
		if len(nodes) == 0:
			return None
		else:
			node = nodes.pop()
			if input_problem.satisfies_goal_test(node):
				return node
			else:
				explored_set.append(node)
				expanded_nodes = input_problem.expand(node)
				if expanded_nodes:
					expanded_nodes.reverse()
					for child in expanded_nodes:
						if child not in explored_set and child not in nodes:
							nodes.append(child)

def contains_node(list, state):
	return any(x.state == state for x in list)

def get_node(list, state):
	for (index, node) in enumerate(list):
		if node.state == state:
			return (index, node)

input_file  = open("input.txt", "r")
algorithm = input_file.readline().strip()
print "Algorithm is " + algorithm
start = input_file.readline().strip()
print "Start state is " + start
goal = input_file.readline().strip()
print "Goal state is " + goal
liveCount = input_file.readline().strip()
print "There are " + liveCount + " live traffic lines"
liveCount = int(liveCount)

graph = {}
heuristic = {}

for i in xrange(0,liveCount):
	(state1, state2, traveltime) = input_file.readline().split()
	print "State 1: " + state1 + ", State 2: " + state2 + ", Travel Time: " + traveltime

	if state1 not in graph:
		graph[state1] = []
	graph[state1].append(State(state2, traveltime))

print "\n Graph is"
print graph
print

sundayCount = input_file.readline().strip()
print "There are " + sundayCount + " sunday traffic lines"
sundayCount = int(sundayCount)

for i in xrange(0,sundayCount):
	(state, timetogoal) = input_file.readline().split()
	print "State: " + state + ", Time to Goal: " + timetogoal

	heuristic[state] = int(timetogoal)

print

input_problem  = Problem(start, goal, graph)

if algorithm == "BFS":
	soln_node = breadth_first_search(input_problem)
	print soln_node.path
	output_file = open("output.txt", "w")
	index = 0
	for i in soln_node.path:
		output_file.write(i + " " + str(index) + "\n")
		index += 1
	output_file.close()
elif algorithm == "DFS":
	soln_node = depth_first_search(input_problem)
	print soln_node.path
	output_file = open("output.txt", "w")
	index = 0
	for i in soln_node.path:
		output_file.write(i + " " + str(index) + "\n")
		index += 1
	output_file.close()
elif algorithm == "UCS":
	soln_node = uniform_cost_search(input_problem)
	print soln_node.path
	output_file = open("output.txt", "w")
	path = []
	while soln_node.parent:
		path.append((soln_node.state, soln_node.path_cost))
		soln_node = soln_node.parent
	path.append((soln_node.state, soln_node.path_cost))
	path.reverse()
	for state,cost in path:
		output_file.write(state + " " + str(cost) + "\n")
	output_file.close()
elif algorithm == "A*":
	soln_node = astar_search(input_problem)
	print soln_node.path
	output_file = open("output.txt", "w")
	path = []
	while soln_node.parent:
		path.append((soln_node.state, soln_node.path_cost))
		soln_node = soln_node.parent
	path.append((soln_node.state, soln_node.path_cost))
	path.reverse()
	for state,cost in path:
		output_file.write(state + " " + str(cost) + "\n")
	output_file.close()

input_file.close()