import argparse
import time
import resource

# output format
# path_to_goal: ['Up', 'Left', 'Left']
# cost_of_path: 3
# nodes_expanded: 181437
# search_depth: 3
# max_search_depth: 66125
# running_time: 5.01608433
# max_ram_usage: 4.23940217

# the goal format of the game
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

class Game:

    nodes_expanded = 0
    max_search_depth = 0

    def __init__(self, board, path_to_goal, search_depth):
        self.board = board
        self.path_to_goal = path_to_goal
        self.search_depth = search_depth
        Game.nodes += 1
        if Game.max_search_depth < search_depth:
            Game.max_search_depth = search_depth

# moving the blank tile up
def up(board):
    blank = board.index(0)
    if blank < 3:
        return None
    else:
        result = list(board)
        target = blank - 3
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile down
def down(board):
    blank = board.index(0)
    if blank > 5:
        return None
    else:
        result = list(board)
        target = blank + 3
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile left
def left(board):
    blank = board.index(0)
    if blank % 3 == 0:
        return None
    else:
        result = list(board)
        target = blank - 1
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile right
def right(board):
    blank = board.index(0)
    if blank % 3 == 2:
        return None
    else:
        result = list(board)
        target = blank + 1;
        result[blank], result[target] = result[target], result[blank]
        return result

# moveset
move_func = {"Up" : up, "Down" : down, "Left" : left, "Right" : right}
moves = ["Up", "Down", "Left", "Right"]

# apply moves to current game
def apply_moves(game, moves, fringe):
    for move in moves:
        new_state = move_func[move](game.board)
        if new_state not in visited:
            new_path = list(game.path_to_goal).append(move)
            new_stage = Game(new_state, new_path, game.search_depth + 1)
            fringe.append(new_stage)

# compute the manhattan distance
def manhattan(board):
    sum = 0
    for t in board:
        if t == 0:
            continue
        pos = board.index(t);
        if t != pos:
            goal_x = t % 3
            goal_y = t / 3
            sum += abs(pos % 3 - goal_x)
            sum += abs(pos / 3 - goal_y)
    return sum

# return in dictionary format
# result = {
#         "path_to_goal": [],
#         "cost_of_path": -1,
#         "nodes_expanded": 0,
#         "search_depth:": depth,
#         "max_search_depth": max_search_depth,
#         "status": -1    ## -1: no result; 0: duplicate state; 1: goal}
# }

# bfs for the game
def bfs(root):
    fringe = list()
    visited = set()
    start_time = time.time()
    apply_moves(root, moveset, fringe)
    result = bfs_r(fringe, visited, 0, 0)
    running_time = time.time() - start_time
    max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000

# dfs for the game
def dfs(root):
    fringe = list()
    visited = set()
# a* search for the game
def ast(root):
    fringe = Queue.PriorityQueue()
    visited = set()

def main():
