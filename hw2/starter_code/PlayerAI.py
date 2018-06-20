from random import randint
from BaseAI import BaseAI
from math import log
import math
import time

Depth = 3
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
inf = float('inf')

#[UP, DOWN, LEFT, RIGHT]
class PlayerAI(BaseAI):
    def __init__(self):
        pass

    def getMove(self, grid):
        return self.iterativeDepth(grid)

    # def getMove(self, grid):
    #     moves = grid.getAvailableMoves()
    #     return moves[randint(0, len(moves) - 1)]

    def max(self, grid, depth, alpha, beta, start):
        if depth == 0 or not grid.canMove():
            # print self.heuristic(grid)
            return None, self.evaluation2(grid)

        moves = grid.getAvailableMoves()
        if not moves:
            return None, inf

        bestMove = None;
        bestScore = alpha;
        for m in moves:
            temp_grid = grid.clone()
            temp_grid.move(m)
            score = self.expect(temp_grid, depth - 1, bestScore, beta, start)
            if score > bestScore:
                bestScore = score
                bestMove = m
            # print str(depth) + "bestMoveMax: " + str(bestMove) + "bestScoreMax: " + str(bestScore)
            if bestScore > beta or time.time() - start >= 0.195:
                return bestMove, bestScore
        return bestMove, bestScore

    def expect(self, grid, depth, alpha, beta, start):
        if depth == 0 or not grid.canMove():
            # print self.heuristic(grid)
            return self.evaluation2(grid)

        cells = grid.getAvailableCells()
        if not cells:
            return -inf

        bestScore2 = beta
        bestScore4 = beta
        for c in cells:
            temp_grid = grid.clone()
            temp_grid.insertTile(c, 2)
            score = self.max(temp_grid, depth - 1, alpha, bestScore2, start)[1]
            if score < bestScore2:
                bestScore2 = score
            # print str(depth) + "bestScoreMin: " + str(bestScore)
            if bestScore2 < alpha or time.time() - start >= 0.195:
                break
        for c in cells:
            temp_grid = grid.clone()
            temp_grid.insertTile(c, 4)
            score = self.max(temp_grid, depth - 1, alpha, bestScore4, start)[1]
            if score < bestScore4:
                bestScore4 = score
            # print str(depth) + "bestScoreMin: " + str(bestScore)
            if bestScore4 < alpha or time.time() - start >= 0.195:
                break

        return 0.9 * bestScore2 + 0.1 * bestScore4

    # calculate the score of current gird
    def evaluation2(self, grid):
        smoothWeight = 0.2
        monoWeight  = 1.5
        emptyWeight  = 3.0
        maxWeight    = 1.0
        empty = len(grid.getAvailableCells())
        smoothness = self.smoothness(grid)
        mono = self.monocticity(grid)
        max = math.log(grid.getMaxTile(), 2)
        return (smoothWeight * smoothness +
                monoWeight * mono +
                emptyWeight * empty +
                maxWeight * max)

    # check if a position is valid
    def isValid(self, grid, pos):
        return (pos[0] >= 0 and pos[0] < grid.size and
                pos[1] >= 0 and pos[1] < grid.size)

    # find the nearest cell which is not 0 on a direction
    def findCell(self, grid, pos, v):
        tmp = pos
        result = tmp
        while self.isValid(grid, tmp) and grid.canInsert(tmp):
            result = tmp
            tmp = (tmp[0] + v[0], tmp[1] + v[1])

        return result

    # calculate the smoothness of a grid
    def smoothness(self, grid):
        result = 0;
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                pos = (x, y)
                if not grid.canInsert(pos):
                    value = math.log(grid.getCellValue(pos), 2)
                    for v in directionVectors:
                        target = self.findCell(grid, (pos), v)
                        if target != pos and not grid.canInsert(target):
                            targetValue = math.log(grid.getCellValue(target), 2)
                            result -= abs(value - targetValue)
        return result

    # calculate the monoticity of a grid
    def monocticity(self, grid):
        totals = [0, 0, 0, 0]

        # vertical direction
        for i in xrange(grid.size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.canInsert((i, next)):
                    next += 1
                if next >= 4:
                    next -= 1
                currentValue = 0
                currentCell = grid.getCellValue((i, current))
                if currentCell:
                    currentValue = math.log(currentCell, 2)
                nextValue = 0
                nextCell = grid.getCellValue((i, next))
                if nextCell:
                    nextValue = math.log(nextCell, 2)
                if currentValue > nextValue:
                    totals[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] += currentValue - nextValue
                current = next
                next += 1

        # horizontal direction
        for j in xrange(grid.size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.canInsert((next, j)):
                    next += 1
                if next >= 4:
                    next -= 1
                currentValue = 0
                currentCell = grid.getCellValue((current, j))
                if currentCell:
                    currentValue = math.log(currentCell, 2)
                nextValue = 0
                nextCell = grid.getCellValue((next, j))
                if nextCell:
                    nextValue = math.log(nextCell, 2)
                if currentValue > nextValue:
                    totals[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[3] += currentValue - nextValue
                current = next
                next += 1
        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def evaluation(self, grid):
        weight_1 = 18.992
        weight_2 = 13.959
        weight_3 = 7.05
        weight_4 = 0.967
        weight_5 = -0.682

        max_cell = log(grid.getMaxTile(), 2)

        free_tiles = 0.0
        adjacent_sum = 1.0
        adjacent_cells = 0.0
        edges_sum = 0.0
        # diff_adjacent_cells = 0.0
        sum_tiles = 0.0

        for x in xrange(grid.size):
            for y in xrange(grid.size):
                pos = (x, y)
                if grid.canInsert(pos):
                    free_tiles += 1.0
                else:
                    pos_value = grid.getCellValue(pos)
                    # print pos_value
                    sum_tiles += pos_value
                    left_pos = (x - 1, y)
                    right_pos = (x + 1, y)
                    up_pos = (x, y - 1)
                    down_pos = (x, y + 1)
                    left_value = grid.getCellValue(left_pos)
                    right_value = grid.getCellValue(right_pos)
                    up_value = grid.getCellValue(up_pos)
                    down_value = grid.getCellValue(down_pos)
                    if x > 0 and left_value:
                        adjacent_sum += abs(log(pos_value, 2) - log(left_value, 2))
                        if pos_value == left_value:
                            adjacent_cells += 1.0
                    elif x == 0:
                        edges_sum += log(pos_value, 2)
                    if x < 3 and right_value:
                        adjacent_sum += abs(log(pos_value, 2) - log(right_value, 2))
                        if pos_value == right_value:
                            adjacent_cells += 1.0
                    elif x == 3:
                        edges_sum += log(pos_value, 2)
                    if y > 0 and up_value:
                        adjacent_sum += abs(log(pos_value, 2) - log(up_value, 2))
                        if pos_value == up_value:
                            adjacent_cells += 1.0
                    elif y == 0:
                        edges_sum += log(pos_value, 2)
                    if y < 3 and down_value:
                        adjacent_sum += abs(log(pos_value, 2) - log(down_value, 2))
                        if pos_value == down_value:
                            adjacent_cells += 1.0
                    elif y == 3:
                        edges_sum += log(pos_value, 2)
        return (max_cell * weight_1) + \
               (free_tiles * weight_2) + \
               (adjacent_cells * weight_3) + \
               (edges_sum * weight_4) + \
               (adjacent_sum * weight_5)

    def evaluation3(self, grid):
        mask = [[6, 5, 4, 3],
                [5, 4, 3, 2],
                [4, 3, 2, 1],
                [3, 2, 1, 0]]
        score = 0
        penalty = 0
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                score += grid.getCellValue((x, y)) * mask[x][y]

                pos_value = grid.getCellValue((x, y))
                left_pos = (x - 1, y)
                right_pos = (x + 1, y)
                up_pos = (x, y - 1)
                down_pos = (x, y + 1)
                left_value = grid.getCellValue(left_pos)
                right_value = grid.getCellValue(right_pos)
                up_value = grid.getCellValue(up_pos)
                down_value = grid.getCellValue(down_pos)
                if x > 0 and left_value:
                    penalty += abs(pos_value - left_value)
                if x < 3 and right_value:
                    penalty += abs(pos_value - right_value)
                if y > 0 and up_value:
                    penalty += abs(pos_value - up_value)
                if y < 3 and down_value:
                    penalty += abs(pos_value - down_value)
        return score - penalty

    def iterativeDepth(self, grid):
        start = time.time()
        bestMove = None
        bestScore = -inf
        depth = 1
        while True:
            move, score = self.max(grid, depth, -inf, inf, start)
            if score > bestScore:
                bestScore = score
                bestMove = move
            depth += 1
            # print (time.time() - start) * 10
            if ((time.time() - start) >= 0.2):
                break
        return bestMove
