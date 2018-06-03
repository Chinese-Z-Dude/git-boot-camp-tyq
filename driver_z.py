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
# moveset
move_set = {"Up" : up, "Down" : down, "Left" : left, "Right" : right}
moves_bfs = ["Up", "Down", "Left", "Right"]
moves_dfs = moves_bfs.reverse()

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

# apply moves to current game
def apply_moves(game, moves, fringe):
    for move in moves:
        new_state = move_set[move](game.board)
        if new_state:
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

# bfs for the game
def bfs(board):
    root = Game(board, [], 0)
    fringe = list(root)
    visited = set()
    while fringe:
        current_stage = fringe.pop()
        if current_stage.board == goal:
            return current_stage
        else if current_stage.board in visited:
            continue

        visited.add(current_stage.board)
        apply_moves(current_stage, moves, current_stage.search_depth + 1)


    # running_time = time.time() - start_time
    # max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000

# dfs for the game
def dfs(board):
    fringe = list()
    visited = set()
# a* search for the game
def ast(board):
    fringe = Queue.PriorityQueue()
    visited = set()

def main():
    
