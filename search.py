"""
In search.py, you will implement generic search algorithms
"""

import util
import numpy as np


class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		util.raiseNotDefined()

	def is_goal_state(self, state):
		"""
		state: Search state

		Returns True if and only if the state is a valid goal state
		"""
		util.raiseNotDefined()

	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		util.raiseNotDefined()

	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		util.raiseNotDefined()


def depth_first_search(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches
	the goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
	print("Is the start a goal?",
	      problem.is_goal_state(problem.get_start_state()))

	print("Start's successors:",
	      problem.get_successors(problem.get_start_state()))

	"""
	# todo: improve performance in blokus (best is 1163 in blokus, ours 1477)
	visited = set()
	v = np.array([problem.get_start_state()])
	e = np.array([])
	fringe = util.Stack()
	fringe.push((problem.get_start_state(), []))

	while not fringe.isEmpty():
		current, move_list = fringe.pop()
		if problem.is_goal_state(current):
			return move_list
		elif current not in visited:
			v_e_new = np.array(problem.get_successors(current))
			if len(v_e_new) == 0:
				continue
			v_new = v_e_new[:, 0]
			e_new = v_e_new[:, 1]
			for vertex_edge in v_e_new:
				fringe.push((vertex_edge[0], move_list + [vertex_edge[1]]))
			v = np.concatenate((v, v_new), axis=None)
			e = np.concatenate((e, e_new), axis=None)
			visited.add(current)

	return []


def breadth_first_search(problem):
	"""
	Search the shallowest nodes in the search tree first.
	"""
	# todo: improve performance in blokus_fill (best is 2114 in blokus, ours 2664)
	# todo: improve performance in blokus_corner (best is 9023 in blokus, ours 9613 )
	visited = set()
	v = np.array([problem.get_start_state()])
	e = np.array([])
	fringe = util.Queue()
	fringe.push((problem.get_start_state(), []))

	while not fringe.isEmpty():
		current, move_list = fringe.pop()
		if problem.is_goal_state(current):
			return move_list
		elif current not in visited:
			v_e_new = np.array(problem.get_successors(current))
			if len(v_e_new) == 0:
				continue
			v_new = v_e_new[:, 0]
			e_new = v_e_new[:, 1]
			for vertex_edge in v_e_new:
				fringe.push((vertex_edge[0], move_list + [vertex_edge[1]]))
			v = np.concatenate((v, v_new), axis=None)
			e = np.concatenate((e, e_new), axis=None)
			visited.add(current)

	return []


def uniform_cost_search(problem):
	"""
	Search the node of least total cost first.
	"""
	"*** YOUR CODE HERE ***"
	visited = set()
	v = np.array([problem.get_start_state()])
	e = np.array([])
	fringe = util.PriorityQueue()
	fringe.push((problem.get_start_state(), []), 0)

	while not fringe.isEmpty():
		current, move_list = fringe.pop()

		if problem.is_goal_state(current):
			return move_list
		elif current not in visited:
			v_e_new = np.array(problem.get_successors(current))
			if len(v_e_new) == 0:
				continue
			v_new = v_e_new[:, 0]
			e_new = v_e_new[:, 1]
			for vertex_edge in v_e_new:
				vertex_edge[0].__class__.__lt__ = lambda x, y: (True)
				vertex_edge[1].__class__.__lt__ = lambda x, y: (True)
				fringe.push((vertex_edge[0], move_list + [vertex_edge[1]]),
				            problem.get_cost_of_actions(move_list) + vertex_edge[2])
			v = np.concatenate((v, v_new), axis=None)
			e = np.concatenate((e, e_new), axis=None)
			visited.add(current)

	return []


def null_heuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0


def a_star_search(problem, heuristic=null_heuristic):
	"""
	Search the node that has the lowest combined cost and heuristic first.
	"""
	"*** YOUR CODE HERE ***"
	visited = set()
	v = np.array([problem.get_start_state()])
	e = np.array([])
	fringe = util.PriorityQueue()
	fringe.push((problem.get_start_state(), [], 0), 0)

	while not fringe.isEmpty():
		current, move_list, move_list_cost = fringe.pop()
		if problem.is_goal_state(current):
			return move_list
		elif current not in visited:
			v_e_new = np.array(problem.get_successors(current))
			if len(v_e_new) == 0:
				continue
			v_new = v_e_new[:, 0]
			e_new = v_e_new[:, 1]
			for vertex_edge in v_e_new:
				vertex_edge[0].__class__.__lt__ = lambda x, y: (True)
				vertex_edge[1].__class__.__lt__ = lambda x, y: (True)
				tot_cost =  move_list_cost + vertex_edge[2]
				fringe.push((vertex_edge[0], move_list + [vertex_edge[1]], tot_cost),
				            tot_cost + heuristic(vertex_edge[0], problem))
			v = np.concatenate((v, v_new), axis=None)
			e = np.concatenate((e, e_new), axis=None)
			visited.add(current)

	return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
