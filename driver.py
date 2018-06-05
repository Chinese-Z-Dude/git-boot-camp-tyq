import argparse
import time
import resource
from Queue import PriorityQueue
from math import sqrt



class Game:
    nodes_expanded = 0
    max_search_depth = 0

    def __init__(self, array, parent, move, search_depth):
        self.array = array
        self.parent= parent
        self.move = move
        self.search_depth = search_depth
        if Game.max_search_depth < search_depth:
            Game.max_search_depth = search_depth

    def to_string(self):
        return ', '.join(str(x) for x in self.array)

goal = [0,1,2,3,4,5,6,7,8]


def Up (array):
    blank = array.index(0)
    dim = int(sqrt(len(array)))
    if blank < dim:
        return None
    else:
        newB = list(array)
        temp = blank - dim
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Down (array):
    blank = array.index(0)
    dim = int(sqrt(len(array)))
    if blank > dim * (dim -1) -1:
        return None
    else:
        newB = list(array)
        temp = blank + dim
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Left (array):
    blank = array.index(0)
    dim = int(sqrt(len(array)))
    if blank % dim == 0:
        return None
    else:
        newB = list(array)
        temp = blank - 1
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Right (array) :
    blank = array.index(0)
    dim = int(sqrt(len(array)))
    if blank % dim == (dim -1):
        return None
    else :
        newB = list(array)
        temp = blank + 1
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

move_set = {"Up" : Up, "Down" : Down, "Left" : Left, "Right" : Right}
moves_bfs = ["Up", "Down", "Left", "Right"]
moves_dfs = ["Right","Left", "Down","Up"]

def apply_moves(game, moves):
    Game.nodes_expanded += 1
    result = list()
    for move in moves:
        new_state = move_set[move](game.array)
        if new_state:
            new_stage = Game(new_state, game, move, game.search_depth + 1)
            result.append(new_stage)
    return result


def manhattan (array):
    count = 0
    dim = int(sqrt(len(array)))
    for i in range(0,len(array)):
        if array[i] != 0:
            x = i % dim
            y = i / dim
            x1 = array[i] % dim
            y1 = array[i] / dim
            count += abs(x -x1) +abs(y-y1)
    return count

def bfs (array):
    root = Game(array,None,None,0)
    fringe = [root]
    visited = set()
    while fringe:
        current_stage = fringe.pop(0)
        visited.add(current_stage.to_string())
        if current_stage.array == goal:
            return current_stage
        moves = apply_moves(current_stage, moves_bfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.append(move)

def dfs (array):
    root = Game(array,None,None,0)
    fringe = [root]
    visited = set()
    while fringe:
        current_stage = fringe.pop()
        visited.add(current_stage.to_string())
        if current_stage.array == goal:
            Game.max_search_depth -= 1
            return current_stage
        moves = apply_moves(current_stage, moves_dfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.append(move)



def ast (array):
    root = Game(array,None,None,0)
    fringe = PriorityQueue()
    fringe.put((manhattan(root.array),root))
    visited = set()
    while fringe:
        current_stage = fringe.get()[1]
        visited.add(current_stage.to_string())
        if current_stage.array == goal:
            return current_stage
        moves = apply_moves(current_stage, moves_dfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.put((manhattan(move.array),move))

def construct_path(game):
    path = list()
    while game:
        if game.move:
            path.append(game.move)
        game = game.parent
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


def main():
    test = [1,2,5,3,4,0,6,7,8]
    result =ast(test)
    path = construct_path(result)
    print "path_to_goal: " + str(path)
    print "cost_of_path: " + str(len(path))
    print "nodes_expanded: " + str(Game.nodes_expanded)
    print "search_depth: " + str(result.search_depth)
    print "max_search_depth: " + str(Game.max_search_depth)

main()
