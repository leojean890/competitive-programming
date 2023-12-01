import random
import sys
import heapq
from typing import Tuple, List
from time import process_time


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


start_time = process_time()
v = False
M = 150
T = 120

A,B,C = 9,7,1

while process_time() - start_time < T:
    knights = {0: {(3, j) for j in [0, 1, 2, 5, 6, 7]}, 1: {(4, j) for j in [0, 1, 2, 5, 6, 7]}}
    knightsOut = {1: {(3, j) for j in [0, 1, 2, 5, 6, 7]}, 0: {(4, j) for j in [0, 1, 2, 5, 6, 7]}}

    for i in range(3):
        knights[0] |= {(i, j) for j in range(8)}
        knights[1] |= {(7 - i, j) for j in range(8)}
        knightsOut[1] |= {(i, j) for j in range(8)}
        knightsOut[0] |= {(7 - i, j) for j in range(8)}

    q = PriorityQueue()
    q.put((0, 0, 0, knights, []), 0)
    visited = {tuple(sorted(knights[0])) + tuple(sorted(knights[1]))}
    while not q.empty() and process_time() - start_time < T:
        (depth, score, randMove, knights, moves) = q.get()

        if knights == knightsOut:
            print(len(moves), M, file=sys.stderr)

            if process_time() - start_time > T: 
                break
            if len(moves) < M:
                M = len(moves)
                print(len(moves))
                for move in moves:
                    print(*move)
                v = True

            break
        for team in range(2):
            for (y,x) in knights[team]:
                for (a,b) in ((y+2,x+1),(y-2,x-1),(y-2,x+1),(y+2,x-1),(y+1,x+2),(y-1,x-2),(y-1,x+2),(y+1,x-2)):
                    if 0 <= a < 8 and 0 <= b < 8 and (a,b) not in knights[0] and (a,b) not in knights[1]:
                        newKnights = {0: knights[0].copy(), 1: knights[1].copy()}
                        newKnights[team].remove((y,x))
                        newKnights[team].add((a,b))

                        hash = tuple(sorted(newKnights[0])) + tuple(sorted(newKnights[1]))

                        if hash not in visited:
                            visited.add(hash)
                            newScore = A*(depth+1)+sum([B*i + (0 if (i,j) in knightsOut[1] else C) for (i,j) in newKnights[1]])+sum([B*(7-i) + (0 if (i,j) in knightsOut[0] else C) for (i,j) in newKnights[0]])
                            q.put((depth+1, newScore, random.randint(0,1000000000), newKnights, moves+[(y,x,a,b)]), newScore)

