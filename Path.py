# Ryan Cox
# 5-1-14
# CSE415 HW2

# This is a python program that allows an agent to compute
# the shortest path from an start point to a goal point
# that goes around rectangular obstacles. Each rectangular obstacle
# has four corners and the robot is only allowed to move from one corner
# to another. We call each corner a "State". A legal move is one from one
# corner to another without going through a rectangle obstacle.
# However, going along the outside is fine and common.

# This is a class for storing problem states.
# pos is the 2D coordinate position of the robot as a tuple
# g_val is the cost so far for A* search
# h_val is the heuristic function value for A* search
# f_val is the sum of g_val and h_val
# parent is the parent of the node
	
from PathGraphics import PathGraphics

class State(object):

	def __init__(self, pos = (0,0), g_val = 0, h_val = 0, f_val = 0, parent = None):
		self.pos = pos
		self.g_val = g_val
		self.h_val = h_val
		self.f_val = f_val
		self.parent = parent

obstacles = []	
		
# 'astar' is a function that gives us the path and cost from start to goal state
# Input: Input file describing the problem instance.
# Output: Solution path and cost for that path.
def astar(input_file):

	# Opening the input file
	f = open(input_file)

	# Retrieving start location from the first line of the file
	s = f.readline().split()[0:2]
	start = (int(s[0]),int(s[1]))

	# Retrieving goal location from the second line of the file
	s = f.readline().split()[0:2]
	goal = (int(s[0]),int(s[1]))

	# Retrieving number of obstacles.
	n_obstacles = f.readline()

	# Creating a list to store the obstacle corners.
	# They are stored in clockwise order as described in the course web-page
	#obstacles = []
	for line in f:
		ln = line.split()

		# Each corner is a tuple of (x,y) location
		top_left = (int(ln[0]),int(ln[1]))
		top_right = (int(ln[2]),int(ln[3]))
		bottom_right = (int(ln[4]),int(ln[5]))
		bottom_left = (int(ln[6]),int(ln[7]))

		#'obstacles' is a list of tuples where each tuple contains four corner points
		global obstacles
		obstacles += [(top_left,top_right,bottom_right,bottom_left)]

	# Closing the file. We don't need it anymore
	f.close()

	# Now we will create nodes and lines from all the obstacles.
	# remember the agent is only allowed to stay at one of these nodes
	# 'nodes' is a list of (x,y) tuples containing the x,y position of all nodes
	# 'lines' is a list of tuples where each tuple contains two nodes
	nodes = [] 
	lines = []
	for obstacle in obstacles:
		nodes += [obstacle[0],obstacle[1],obstacle[2],obstacle[3]]
		lines += [(obstacle[0],obstacle[1])]
		lines += [(obstacle[1],obstacle[2])]
		lines += [(obstacle[2],obstacle[3])]
		lines += [(obstacle[3],obstacle[0])]

	startH = straightLineDistance(start, goal)
	startState = State(start, 0, startH, startH)
	startState.succ = [startState]
	q = startState
	
	openList = [startState]
	closedList = []
	
	while (len(openList) != 0):
		# finds the state in open with the lowest f_val
		q = openList[0]
		for node in openList:  
			if (node.f_val < q.f_val):
				q = node
		 
		openList.remove(q) # pop q off open list
		children = find_valid_children(q, nodes, lines, obstacles, goal)

		for child in children: # children, list of states	
			# Reached the goal
			if (child.pos == goal):
				kid = child
				successors = [kid]
				while (kid.parent != None):
					successors.append(kid.parent)
					kid = kid.parent
				return successors
		
			skipNode1 = False
			skipNode2 = False
			for node in openList:
				if (node.pos == child.pos and node.f_val <= child.f_val):
					# do not add to openList
					skipNode1 = True
			for node in closedList:
				if (node.pos == child.pos and node.f_val <= child.f_val):
					# do not add to openList
					skipNode2 = True
			if (skipNode1 != True and skipNode2 != True): 
				openList.append(child)
		
		closedList.append(q)

# Computes the length of the direct path from the input coordinates to the goal coordinates
def straightLineDistance(node, goal):
	return (((goal[0] - node[0]) ** 2) + (goal[1] - node[1]) ** 2) ** 0.5

# Finds all possible next states
#
# input parameters 
# state: State object
# nodes: list of tuples, all possible states
# lines: list of tuples where each tuple is two nodes
# obstacles: list of tuples where each tuples contains four corner points
# goal: tuple, goal coordinates
#
# output
# returns a list of states representing valid moves from the state input
#
def find_valid_children(state, nodes, lines, obstacles, goal):

	# Empty list of children that needs to be returned by the function
	children = []

	for possibleState in nodes:
		if (find_valid_move(state.pos, possibleState, lines, obstacles)):
			newState = State(possibleState) 
			newState.g_val = state.g_val + straightLineDistance(state.pos, newState.pos)
			newState.h_val = straightLineDistance(newState.pos, goal)
			newState.f_val = newState.g_val + newState.h_val
			newState.succ = state.succ
			if (state not in newState.succ):
				newState.succ.append(state)
			newState.parent = state
			children.append(newState)
				
	return children

# This function determines if the move from p0 to p1 is valid or not.

# Input: - 'p0' and 'p1' are two tuples containing starting and ending co-ordinate, respectively.
#		- 'lines' is a list of tuples where each tuple is two points. See the construction of 'lines'
#		   in the astar function above.
#		- 'obstacles' is a list of tuples where each tuple contains four corner points. See the
#		   construction of 'obstacles' in the astar function above.

# Output: - 'True' if the move is valid (does not intersect any obstacle)
#		 - 'False' if the move is invalid (intersects a rectangle)

# Detail:  You are not required to understand the detail of this function to implement this assignment.
#		  You can just call it directly whenever needed. But you can always dig deeper.
#		  On a high level, this function tests if two lines intersect or not. One line
#		  is the movement line and other is edge of all obstacles stored in the 'lines'
#		  list. As each obstacle is made of four edges (lines), only checking the line
#		  intersection is sufficient.

def find_valid_move(p0,p1,lines,obstacles):

	# Test if (p0,p1) is an edge of any obstacle,
	# which is already valid according to the problem definition.
	for obstacle in obstacles:
		if p0 in obstacle and p1 in obstacle:

			# Finding the indices
			i = obstacle.index(p0)
			j = obstacle.index(p1)

			# Make sure that i is the smaller index. This is very important as
			# the nodes are sorted in clockwise order
			if j < i:
				i,j = j,i

			# Indices are consecutive. So this is an edge
			if 1 == (j - i) or (0 == i and len(obstacle)-1 == j):
				return True
			else:
				return False

	# Now we have to find if the line (p0,p1) intersects any obstacle.
	# Obstacles are made of edges (lines). So just checking
	# if (p0,p1) intersects any line will be sufficient.

	for line in lines:
		# skip if p0 or p1 is an endpoint of this line
		if p0 in line or p1 in line:
			continue

		# We utilized vector math to figure out if any two lines intersects each other
		# The math details can be found here:
		# see http://www.cs.iastate.edu/~cs518/handouts/segment-intersect.ppt (Slide 4)
		r0 = sub(line[0],line[1])
		c0 = cross(sub(p0,line[1]),r0)
		c1 = cross(sub(p1,line[1]),r0)

		r1 = sub(p0,p1)
		c2 = cross(sub(line[0],p1),r1)
		c3 = cross(sub(line[1],p1),r1)

		# If the sign does not match, its an intersection
		if (c0 == 0 or c1 == 0 or sign(c0) != sign(c1)) and (c2 == 0 or c3 == 0 or sign(c2) != sign(c3)):
			return False

	return True


# The following three functions (sign, sub, and cross) are small helper functions used to
# implement find_valid_move function.

# returns the sign of a number as -1,0,1
def sign(x):
	if x == 0:
		return 0
	elif x < 0:
		return -1
	elif x >0:
		return 1
	else:
		return None

# Subtracting one point from another
def sub(a,b):
	return (a[0]-b[0],a[1]-b[1])

# return the vector cross product
# only need 2D case, so returns z component as scalar
# inputs are in form ((x0,y0),(x1,y1))
def cross(a,b):
	return a[0]*b[1]-a[1]*b[0]
	
# Prints the shortest path to the console	
def output(list):
	print("Point\t\t\tCumulative Cost")
	for step in list:
		print(str(step.pos) + "  \t\t" + str(step.g_val))

# Main function
if __name__ == "__main__":
	result = astar('ComplexDataSet.txt')
	result.reverse()
	output(result)
	
	# Create visualization
	app = PathGraphics(obstacles, result)
	app.master.title('Shortest Path')
	app.mainloop()

