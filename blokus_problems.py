from board import Board
from search import SearchProblem, ucs
import util, math


class BlokusFillProblem(SearchProblem):
	"""
	A one-player Blokus game as a search problem.
	This problem is implemented for you. You should NOT change it!
	"""

	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)
		self.expanded = 0

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board

	def is_goal_state(self, state):
		"""
		state: Search state
		Returns True if and only if the state is a valid goal state
		"""
		return not any(state.pieces[0])

	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, 1) for move in
		        state.get_legal_moves(0)]

	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
		self.expanded = 0
		"*** YOUR CODE HERE ***"
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board

	def is_goal_state(self, state):
		if state.state[0][0] == -1 or state.state[self.board.board_h - 1][
			0] == -1 or state.state[0][self.board.board_w - 1] == -1 or \
				state.state[self.board.board_h - 1][
					self.board.board_w - 1] == -1:
			return False
		return True

	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
		        move in state.get_legal_moves(0)]

	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		"*** YOUR CODE HERE ***"
		tot_cost = 0
		for action in actions:
			tot_cost += action.piece.get_num_tiles()
		return tot_cost


def pitaguras_dist(xy1, xy2):
	a = (xy2[0] - xy1[0])
	b = (xy2[1] - xy1[1])
	c = math.floor(((a ** 2) + (b ** 2)) ** 0.5)
	return c


def blokus_corners_heuristic(state, problem):
	"""
	Your heuristic for the BlokusCornersProblem goes here.

	This heuristic must be consistent to ensure correctness.  First, try to come up
	with an admissible heuristic; almost all admissible heuristics will be consistent
	as well.

	If using A* ever finds a solution that is worse uniform cost search finds,
	your heuristic is *not* consistent, and probably not admissible!  On the other hand,
	inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
	"""
	"*** YOUR CODE HERE ***"
	cost = 0
	corners = [(0, 0), (state.board_w - 1, 0), (0, state.board_h - 1),
	           (state.board_w - 1, state.board_h - 1)]
	max_board = state.board_w + state.board_h

	corners_distance = {corners[0]: max_board, corners[1]: max_board,
	                    corners[2]: max_board, corners[3]: max_board}
	for y, y_val in enumerate(state.state):
		for x, x_val in enumerate(state.state[y]):
			if state.state[y][x] == 0:
				for i, corner in enumerate(corners):
					min_d = min(corners_distance[corner],
					            pitaguras_dist(
						            (x, y),
						            (corner[0], corner[1])))
					corners_distance[corner] = min_d

	for val in corners_distance.values():
		cost += max(val, 0)

	return cost


class BlokusCoverProblem(SearchProblem):
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
	             targets=[(0, 0)]):
		self.targets = targets.copy()
		self.expanded = 0
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board

	def is_goal_state(self, state):
		"*** YOUR CODE HERE ***"

		for target in self.targets:
			if state.state[target[0], target[1]] == -1:
				return False
		return True

	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
		        move in state.get_legal_moves(0)]

	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		tot_cost = 0
		for action in actions:
			tot_cost += action.piece.get_num_tiles()
		return tot_cost


def blokus_cover_heuristic(state, problem):
	"*** YOUR CODE HERE ***"
	cost = 0
	max_board = state.board_w + state.board_h

	target_distance = {target: max_board for target in problem.targets}
	for y, y_val in enumerate(state.state):
		for x, x_val in enumerate(state.state[y]):
			if state.state[y][x] == 0:
				for i, target in enumerate(problem.targets):
					min_d = min(target_distance[target],
					            pitaguras_dist(
						            (x, y),
						            (target[0], target[1])))
					target_distance[target] = min_d

	for val in target_distance.values():
		cost += max(val, 0)

	return cost // len(problem.targets)


class ClosestLocationSearch:
	"""
	In this problem you have to cover all given positions on the board,
	but the objective is speed, not optimality.
	"""

	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
	             targets=(0, 0)):
		self.expanded = 0
		self.targets = targets.copy()
		"*** YOUR CODE HERE ***"

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board

	def solve(self):
		"""
		This method should return a sequence of actions that covers all target locations on the board.
		This time we trade optimality for speed.
		Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
		You may define helpful functions as you wish.

		Probably a good way to start, would be something like this --

		current_state = self.board.__copy__()
		backtrace = []

		while ....

			actions = set of actions that covers the closets uncovered target location
			add actions to backtrace

		return backtrace
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()


class MiniContestSearch:
	"""
	Implement your contest entry here
	"""

	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
	             targets=(0, 0)):
		self.targets = targets.copy()
		"*** YOUR CODE HERE ***"

	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board

	def solve(self):
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()
