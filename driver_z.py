import sys
import argparse
import time
import resource
from Queue import PriorityQueue
from math import sqrt

# the goal format of the game
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
board_size = 0

class Game:

    nodes_expanded = 0
    max_search_depth = 0

    def __init__(self, board, parent, move, search_depth):
        self.board = board
        self.parent = parent
        self.move = move
        self.search_depth = search_depth
        if Game.max_search_depth < search_depth:
            Game.max_search_depth = search_depth

    def to_string(self):
        return ', '.join(str(x) for x in self.board)

# moving the blank tile up
def up(board):
    blank = board.index(0)
    if blank < board_size:
        return None
    else:
        result = list(board)
        target = blank - board_size
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile down
def down(board):
    blank = board.index(0)
    if blank > board_size * (board_size - 1) - 1:
        return None
    else:
        result = list(board)
        target = blank + board_size
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile left
def left(board):
    blank = board.index(0)
    if blank % board_size == 0:
        return None
    else:
        result = list(board)
        target = blank - 1
        result[blank], result[target] = result[target], result[blank]
        return result

# moving the blank tile right
def right(board):
    blank = board.index(0)
    if blank % board_size == board_size - 1:
        return None
    else:
        result = list(board)
        target = blank + 1;
        result[blank], result[target] = result[target], result[blank]
        return result

def apply_moves_test(board, moves, fringe):
    for move in moves:
        fringe.append(board)
        board = move_set[move](board)


# apply moves to current game
def apply_moves(game, moves):
    Game.nodes_expanded += 1
    result = list()
    for move in moves:
        new_state = move_set[move](game.board)
        if new_state:
            new_stage = Game(new_state, game, move, game.search_depth + 1)
            result.append(new_stage)
    return result

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
    root = Game(board, None, None, 0)
    fringe = [root]
    visited = set()
    while fringe:
        current_stage = fringe.pop(0)
        visited.add(current_stage.to_string())
        if current_stage.board == goal:
            return current_stage

        moves = apply_moves(current_stage, moves_bfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.append(move)

    # running_time = time.time() - start_time
    # max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000

# dfs for the game
def dfs(board):
    root = Game(board, None, None, 0)
    fringe = [root]
    visited = set()
    while fringe:
        current_stage = fringe.pop()
        visited.add(current_stage.to_string())
        if current_stage.board == goal:
            return current_stage

        moves = apply_moves(current_stage, moves_dfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.append(move)

# a* search for the game
def ast(board):
    root = Game(board, None, None, 0)
    fringe = PriorityQueue()
    fringe.put((manhattan(root.board), root))
    visited = set()
    while fringe:
        current_stage = fringe.get()[1]
        visited.add(current_stage.to_string())
        if current_stage.board == goal:
            return current_stage

        moves = apply_moves(current_stage, moves_dfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.put((manhattan(move.board), move))

# moveset
move_set = {"Up" : up, "Down" : down, "Left" : left, "Right" : right}
moves_bfs = ["Up", "Down", "Left", "Right"]
moves_dfs = list(moves_bfs)
moves_dfs.reverse()

# methods
methods = {"bfs": bfs, "dfs": dfs, "ast": ast}

# reconstruct path_to_goal
def construct_path(end_game):
    path = list()
    while end_game:
        if end_game.move:
            path.append(end_game.move)
        end_game = end_game.parent
    path.reverse()
    return path

def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True

# process the Argument
def process_args(args):
    global board_size
    if args.method not in methods:
        return (-1, None, None)

    board = [int(x) for x in args.board.split(',')]
    if not board or not is_square(len(board)) or len(board) != len(set(board)):
        return (-2, None, None)
    board_size = int(sqrt(len(board)))
    return (1, args.method, board)


# output format
# path_to_goal: ['Up', 'Left', 'Left']
# cost_of_path: 3
# nodes_expanded: 181437
# search_depth: 3
# max_search_depth: 66125
# running_time: 5.01608433
# max_ram_usage: 4.23940217

def main():
    start_time = time.time()
    par = argparse.ArgumentParser()
    par.add_argument("method")
    par.add_argument("board")
    args = process_args(par.parse_args())

    # input contains wrong method
    if args[0] == -1:
        print "method does not exist"

    # input contans wrong board
    elif args[0] == -2:
        print "invalid puzzle board"

    board = args[2]
    result = methods[args[1]](board)
    path = construct_path(result)
    running_time = time.time() - start_time
    max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000

    print "path_to_goal: " + str(path)
    print "cost_of_path: " + str(len(path))
    print "nodes_expanded: " + str(Game.nodes_expanded)
    print "search_depth: " + str(result.search_depth)
    print "max_search_depth: " + str(Game.max_search_depth)
    print "running_time: " + str(running_time)
    print "max_ram_usage: " + str(max_ram_usage)

# if called from the terminal, excute main
if __name__ == '__main__':
    main()
