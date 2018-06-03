import argparse
import time
import resource
class Game:
    nodes_expanded = 0
    max_search_depth = 0

    def _init_(self, array, parent, move, search_depth):
        self.array = array
        self.parent= parent
        self.move = move
        self.search_depth = search_depth

    def to_string(self):
        return ', '.join(str(x) for x in self.array)

goal = [0,1,2,3,4,5,6,7,8]
move_set = {"Up" : Up, "Down" : Down, "Left" : Left, "Right" : Right}
moves_bfs = ["Up", "Down", "Left", "Right"]
moves_dfs = ["Right","Left", "Down","Up"]

def Up (array):
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank < dim:
        return None
    else:
        newB = list(array)
        temp = blank - dim
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Down (array):
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank > [dim * (dim -1) -1]:
        return None
    else:
        newB = list(array)
        temp = blank + dim
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Left (array):
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank % dim == 0:
        return None
    else:
        newB = list(array)
        temp = blank - 1
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

def Right (array) :
    blank = array.index(0)
    dim = sqrt(len(array))
    if blank % dim == (dim -1):
        return None
    else :
        newB = list(array)
        temp = blank + 1
        newB[blank], newB[temp] = newB[temp], newB[blank]
        return newB

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
    for i in range(0,len(array)):
        if array[i] != 0:
            x = i % dim
            y = i / dim
            x1 = array[i] % dim
            y1 = array[i] / dim
            count += abs(x -x1) +abs(y-y1)
    return count

def bfs (array):
    root = Game(array,[],[],0)
    fringe = list(root)
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
    root = Game(array,[],[],0)
    fringe = list(root)
    visited = set()
    while fringe:
        current_stage = fringe.pop()
        visited.add(current_stage.to_string())
        if current_stage.array == goal:
            return current_stage
        moves = apply_moves(current_stage, moves_dfs)
        for move in moves:
            if move.to_string() not in visited:
                visited.add(move.to_string())
                fringe.append(move)



def ast (array):
    root = Game(array,[],[],0)
    fringe = PriorityQueue()
    fringe.put(manhattan(root.array),root)
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
                fringe.put(manhattan(move.array),move)

def construct_path(Game):
    path = list()
    while Game:
        if Game.move:
            path.append(Game.move)
            Game = Game.parent
    path.reverse()
    return path


def main():
    test = [1,2,5,3,4,0,6,7,8]
    result =bfs(test)
    path = construct_path(result)


main()
