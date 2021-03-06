#!/usr/bin/env python3

import sys
import ipdb
breakP = ipdb.set_trace

# This is the main script for Homework #5
def main():
	args = sys.argv

	# 1st argument is the text document containing the map
	txtMap = args[1]

	# 2nd argument is the acceptable error level
	e = float(args[2])

	# First, create an integer version of the map
	rMap = readMap(txtMap)
	#print rMap
	
	# Now, convert the integer version into a list of nodes
	Map = makeMap(rMap)
	
	# Establish all the nodes neighbors
	findNeighbors(Map)
	
	# Include Snake Effect
	# lookSnake(Map)

	# Restablish wall reward
	reWall(Map)
	
	# NOW PERFORM MDP ALGORITHM
	# GIVEN: DISCOUNT FACTOR OF LIFE
	gam = 0.9
	setUtilities(Map)
	#checkMap(Map)
	#print 
	error = e*(1.0-gam)/gam
	delta = 10000.0
	
	while delta > error:
		# Reset the parent pointer to keep the most relevant move
		resetParent(Map)

		# Store the current value of utility
		prev_ut(Map)
		
		# Iterate on the utilities of the map
		Map = iterUtilities(Map,gam)

		# Restablish the zero values of the walls and snakes
		reWall(Map)
		
		# Restablish DELTA from prev and new utilities
		delta = reError(Map)
		
		# Display the current map progress
		#checkMap(Map)
		#print

		
	(util_vals,move) = val_results(Map)
	
	for k in range(0,len(util_vals)):
		print move[k], util_vals[k],
		(y1,x1) = move[k]
		if k != len(util_vals)-1:
			(y2,x2) = move[k+1]
		if x1 + 1 == x2:
			print 'RIGHT',
		if y1 - 1 == y2:
			print 'UP',
		if util_vals[k] == 50:
			print 'YUMMY APPLE'
		print

	#print(util_vals)
	#print(move)
	
	
# CONVERT THE GIVEN TEXT VERSION INTO MORE READABLE VERSION
def readMap(worldname):
	array = []
	filename = open(worldname,'r')
	
   	for lines in filename.read().split('\n'):
		array.append(lines.split(' '))
		
	
	return array[:-2]

# CLASS FOR THE NODES OF THE MAP
class mapNode:
	def __init__(self,x_loc,y_loc,map_type,neighbors):
		
		# This is the location of the node
		self.x = x_loc
		self.y = y_loc
		
		# This is the integer value of the map location
		self.t = map_type
		
		# Is this a wall
		if (self.t == 2) | (self.t == 50):
			self.walkable = False
		else:
			self.walkable = True

		# DESIGNATE REWARD BASED ON MAP TYPE
		if (self.t == 1):
			# MOUNTAIN
			self.reward = -1
		if (self.t == 4):
			# BARN
			self.reward = 1
		if (self.t == 50):
			# APPLE
			self.reward = 50
		if (self.t == 0):
			# ANY WALKABLE 
			self.reward = 0	
		if (self.t == 2):
			# ANY WALL
			self.reward = 0
		if (self.t == 3):
			# ANY SNAKE HAS NEGATIVE REWARD
			self.reward = -2 

		# Establish all nodes at 0 utility	
		self.utility = 0
		
		# Keep the previous value of the map
		self.putility = 0

		# Establish a neighbors array
		self.n = []

		# Establish a parent array
		self.p = []

# MAKE THE MAP FROM THE INTEGER REPRESENTATION
def makeMap(readMap):
	for j in range(len(readMap)):
		for i in range(len(readMap[j])):
			readMap[j][i] = mapNode(i,j,int(readMap[j][i]),None)
	return readMap

# RESET PARENT POINTERS FOR LAST RUN
def resetParent(Map):
	for j in range(len(Map)):
		for i in range(len(Map[j])):
			Map[j][i].p = []

# STORE THE CURRENT VALUE OF THE UTILITIES BEFORE ITERATION
def prev_ut(Map):
	for j in range(len(Map)):
		for i in range(len(Map[j])):
			Map[j][i].putility = Map[j][i].utility


# NEIGHBOR FINDING FUNCTION TO BE APPLIED TO THE ENTIRE MAP
def findNeighbors(Map):
	for j in range(0,len(Map)):
		for i in range(0,len(Map[j])):
			# IF IN THE TOP ROW OF THE MAP
			if (j == 0):
				# IF LEFT CORNER
				if (i == 0):
					#breakP()
					Map[j][i].n.append(Map[j][i+1])
					Map[j][i].n.append(Map[j+1][i])
				# IF RIGHT CORNER
				elif (i == len(Map[j])-1):
					Map[j][i].n.append(Map[j][i-1])
					Map[j][i].n.append(Map[j+1][i])
				# NOT CORNERS => MUST BE CENTER
				else:
					Map[j][i].n.append(Map[j][i-1])
					Map[j][i].n.append(Map[j+1][i])
					Map[j][i].n.append(Map[j][i+1])
			# ELSE IF LAST ROW
			elif (j == len(Map)-1):
				# IF BOTTOM LEFT CORNER
				if (i == 0):
					Map[j][i].n.append(Map[j-1][i])
					Map[j][i].n.append(Map[j][i+1])
				# IF BOTTOM RIGHT CORNER
				elif (i == len(Map[j])-1):
					Map[j][i].n.append(Map[j-1][i])
					Map[j][i].n.append(Map[j][i-1])
				# NOT CORNERS => MUST BE CENTER
				else:
                                        Map[j][i].n.append(Map[j][i-1])
                                        Map[j][i].n.append(Map[j-1][i])
                                        Map[j][i].n.append(Map[j][i+1])
			# IF IT IS NOT THE TOP OR BOTTOM ROW
			# IF IT IS LEFT SIDE
			elif (i == 0):
				if (j != 0) or (j != len(Map)-1):
					#breakP()
					Map[j][i].n.append(Map[j-1][i])
					Map[j][i].n.append(Map[j][i+1])
					Map[j][i].n.append(Map[j+1][i])
			# IF IT IS RIGHT SIDE
			elif (i == len(Map[j])-1):
				Map[j][i].n.append(Map[j-1][i])
				Map[j][i].n.append(Map[j][i-1])
				Map[j][i].n.append(Map[j+1][i])
			# ELSE IT IS IN THE CENTER OF THE MAP
			else:
				#breakP()
				Map[j][i].n.append(Map[j-1][i])
				Map[j][i].n.append(Map[j][i-1])
				Map[j][i].n.append(Map[j][i+1])
				Map[j][i].n.append(Map[j+1][i])
			#print len(Map[j][i].n),
		#print
	
# USED TO CHECK THE MAP FOR ANY NEW IMPLEMENTATIONS
def checkMap(Map):
	for j in range(0,len(Map)):
		for i in range(0,len(Map[j])):
			print round(Map[j][i].utility,1),
		print

# USED TO ESTABLISH THE SNAKE IMPACTED TILES
#def lookSnake(Map):
#	for j in range(0,len(Map)):
#		for i in range(0,len(Map[j])):
#			# SEARCH NODE NEIGHBORS FOR SNAKES	
#			for m in range(0, len(Map[j][i].n)):
#				if Map[j][i].n[m].t == 3:
#					Map[j][i].reward = Map[j][i].reward - 2

# RESTABLISH WALL REWARDS
def reWall(Map):
	for j in range(0,len(Map)):
		for i in range(0,len(Map[j])):
			# SEARCH FOR WALL NODES AND SET TO 0	
			if Map[j][i].t == 2:
				Map[j][i].reward = 0
				Map[j][i].utility = 0 
# FIRST RUN SET REWARD AS UTILITIES
def setUtilities(Map):
	for j in range(0,len(Map)):
                 for i in range(0,len(Map[j])):
                 	Map[j][i].utility = Map[j][i].reward

def iterUtilities(Map,gamma):
	#g_loc = len(Map[0])-1
	#breakP()
	for j in range(0,len(Map)):
                for i in range(0,len(Map[j])):
			i = len(Map[j])-1-i
			#breakP()
			if Map[j][i].walkable == True:
				# RE-EDITTING UTILITY ITERATION ROUTINE	
				#breakP()
				# START IN TOP RIGHT CORNER
				#if j == 0:
					# DONT EVAL GOAL
				#	x_g = g_loc - i - 1
				#else:
					# EVAL IN GOAL COLUMN
				#	x_g = g_loc - i
				
				# DETERMINE IF ANY MOVE RESULTS IN BOUNCING BACK
				# TOP BOUNCE DOWN
				if (Map[j][i].y - 1 == -1):
					top = Map[j][i]
				else:
					top = Map[j-1][i]
				# BOTTOM BOUNCE UP
				if (Map[j][i].y + 1 == len(Map)):
					bottom = Map[j][i]
				else:				
					bottom = Map[j+1][i]
				# LEFT BOUNCE RIGHT
				if (Map[j][i].x - 1 == -1):
					left = Map[j][i]
				else:
					left = Map[j][i-1];
				# RIGHT BOUNCE LEFT
				if (Map[j][i].x + 1 == len(Map[j])):
					right = Map[j][i]
				else:
					right = Map[j][i+1]	
				# CREATE VARIABLE TO STORE THE BEST MOVE FROM THE NEIGHBORS
				max_actval = -1000	

				# DETERMINED BOUNCES, NOW LOOK AT NEIGHBORS(ACTIONS)
				for m in range(0, len(Map[j][i].n)):
					# MOVE RIGHT TO RIGHT NEIGHBOR
					if (Map[j][i].n[m].x == i + 1):
						act_val = (.8*right.utility + .1*top.utility + .1*bottom.utility)
						act = Map[j][i].n[m]
					# MOVE DOWN TO BOTTOM NEIGHBOR
					elif (Map[j][i].n[m].y == j + 1):
						act_val = (.8*bottom.utility + .1*left.utility +.1*right.utility)	
						act = Map[j][i].n[m]
					# MOVE LEFT TO LEFT NEIGHBOR
					elif (Map[j][i].n[m].x == i - 1):
						act_val = (.8*left.utility + .1*top.utility + .1*bottom.utility)
						act = Map[j][i].n[m]
					# MOVE UP TO TOP NEIGHBOR	
					elif (Map[j][i].n[m].y == j - 1):
						act_val = (.8*top.utility + .1*left.utility + .1*right.utility)
						act = Map[j][i].n[m]
					if (act_val > max_actval):
						max_actval = act_val
						max_act = act
				#breakP()
				Map[j][i].utility = Map[j][i].reward + gamma*max_actval
				Map[j][i].p.append(max_act)
			else:
				pass
	return Map

# Restablish error value
def reError(Map):
	max_error = 0
	for j in range(0,len(Map)):
		for i in range(0,len(Map[j])):
                 	node_error = abs(Map[j][i].utility-Map[j][i].putility)
			if node_error > max_error:
				max_error = node_error
	return max_error

# Prints the utilities result
def val_results(Map):
	values = []
	path = []
	last_row = len(Map) - 1
	node = Map[last_row][0]
	values.append(node.utility)
	path.append((node.y,node.x))
	Go = True
	while(node.t != 50):
		route = node
		best = 0
		for i in range(0,len(node.n)):
			this = node.n[i]
			if this.utility > best:
				best = this.utility
				bpath = (this.y,this.x)
				route = this 
		node = route
		values.append(best)
		path.append(bpath)
	return (values, path)

if __name__ == '__main__':
    sys.exit(main())
