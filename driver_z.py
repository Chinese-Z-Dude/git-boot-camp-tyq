import argparse

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
moves = {"Up" : up, "Down" : down, "Left" : left, "Right" : right}

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
def bfs(root):
    fringe = list()
    visited = set()

# recursive method for bfs
def bfs_r(board, fringe, visited):


# dfs for the game
def dfs(root):
    fringe = list()
    visited = set()
# a* search for the game
def ast(root):
    fringe = Queue.PriorityQueue()
    visited = set()

def main():
