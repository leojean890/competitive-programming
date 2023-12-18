
import heapq
import sys
from typing import List, Tuple


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
inv = {RIGHT:LEFT, LEFT:RIGHT, UP:DOWN, DOWN:UP}

N = 141
lines = []
for ind in range(N):
    lines.append([int(i) for i in input()])
q = PriorityQueue()
q.put((0, 0, -1, -1, 0), 0)
dd = {}

M = sys.maxsize

while not q.empty():
    (y, x, dir, nbCasesPerDir, currentTotalCost) = q.get()

    if y == N-1 and x == N-1:
        if currentTotalCost < M:
            M = currentTotalCost
        continue

    state1 = (y, x, dir, nbCasesPerDir)
    if state1 in dd:
        continue
    dd[state1] = currentTotalCost

    for (a,b,d) in ((y+1,x,DOWN), (y,x+1,RIGHT), (y,x-1,LEFT), (y-1,x,UP)):
        if 0 <= a < N and 0 <= b < N and nbCasesPerDir <= 10 and (dir in (-1,d) or nbCasesPerDir >= 4) and dir != inv[d]:
            state = (a, b, d, 1 if d != dir else nbCasesPerDir + 1, currentTotalCost + lines[a][b])
            q.put(state, currentTotalCost + lines[a][b])

print(M) # 788
