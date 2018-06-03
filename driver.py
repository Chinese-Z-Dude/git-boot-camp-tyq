import argparse
import time
import resource
class Game:
    def _init_(self, array, path_to_goal, search_depth):
        self.array = array
        self.path_to_goal = path_to_goal
        self.search_depth = search_depth

goal = [0,1,2,3,4,5,6,7,8]
move_set = {"Up" : up, "Down" : down, "Left" : left, "Right" : right}
moves_bfs = ["Up", "Down", "Left", "Right"]
moves_dfs = ["Right","Left", "Down","Up"]

def Up (array) :
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank < dim :
        return None
    else :
        newB = list(array)
        temp = blank - dim
        newB[blank],newB[temp] = newB[temp],newB[blank]
        return newB

def Down (array) :
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank > [dim * (dim -1) -1]:
        return None
    else :
        newB = list(array)
        temp = blank + dim
        newB[blank],newB[temp] = newB[temp],newB[blank]
        return newB

def Left (array) :
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank % dim == 0:
        return None
    else :
        newB = list(array)
        temp = blank - 1
        newB[blank],newB[temp] = newB[temp],newB[blank]
        return newB

def Right (array) :
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank % dim == (dim -1):
        return None
    else :
        newB = list(array)
        temp = blank + 1
        newB[blank],newB[temp] = newB[temp],newB[blank]
        return newB

def apply_moves(game, moves, Fringe) :
    for move in moves:
        new_state = move_set[move](game.array)
        if new_state:
            new_path = list(game.path_to_goal).append(move)
            new_stage = Game(new_state, new_path, game.search_depth + 1)
            fringe.append(new_stage)

def manhattan (array) :
    count = 0
    for i in range(0,len(array)) :
        if array[i] != 0 :
            x = i % dim
            y = i / dim
            x1 = array[i] % dim
            y1 = array[i] / dim
            count += abs(x -x1) +abs(y-y1)
    return count

def bfs (array) :
    root = Game(array,[],0)
    fringe = list(root)
    visited = set()
    while fringe:
        current_stage = fringe.pop(0)
        if current_stage == goal :
            return current_stage
        else :
            current_stage.array in visited
            continue

        visited.add (current_stage.array)
        apply_moves(current_stage, moves_bfs, fringe)

def dfs (array) :
    root = Game(array,[],0)
    fringe = list(root)
    visited = set()
    while fringe:
        current_stage = fringe.pop()
        if current_stage == goal :
            return current_stage
        else :
            current_stage.array in visited
            continue

        visited.add (current_stage.array)
        apply_moves(current_stage, moves_dfs, fringe)

def ats
