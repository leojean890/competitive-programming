import heapq
import random
from time import process_time
import sys
from typing import List, Tuple

sys.setrecursionlimit(1000000)


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


boundary1 = 65  # int(boundary1)
boundary2 = 5  # int(boundary2)
boundary3 = 160  # int(boundary3)

N = int(input())
start_time = process_time()
horizontal_bars = [input() for _ in range(N - 1)]
vertical_bars = [input() for _ in range(N)]

entrance = (0, 0)
(i2, j2) = (0, 0)
dirt_quantity_delta = []
avgDirtDelta = 0
for i in range(N):
    lst = [int(j) for j in input().split()]
    dirt_quantity_delta.append(lst)
    for j in range(N):
        avgDirtDelta += lst[j]
avgDirtDelta /= N * N

dij = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir = "RDLU"
ll = list(range(4))
dijPerDir = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}
best = None
bestScore = sys.maxsize
nbIt = 0
time_new_it = process_time()
it_duration = 0
while process_time() - start_time + it_duration < 1.9:
    nbIt += 1
    nbVisited = N * N
    counterReshit = 0

    visited = []

    for y in range(N):
        for x in range(N):
            visited.append((y, x))

    turnsPerSpot = []
    for j in range(N):
        turnsPerSpot.append([(0,) for i in range(N)])

    (i, j, depth) = (0, 0, 0)

    currentPath = ""

    factor1 = random.randint(1, boundary1)
    factor2 = random.randint(1, boundary2)
    factor3 = random.randint(1, boundary3)

    while (i, j) != entrance or nbVisited > 0:  # ou depth > 2000
        toGo = entrance
        if nbVisited > 0:
            toGo = None
            if (i, j) in visited:
                visited.remove((i, j))
                nbVisited -= 1

        q = PriorityQueue()
        initDepth = depth
        q.put((i, j, [], depth), 0)
        visited1 = {(i, j)}
        v = False

        while q:
            (y, x, path, depth) = q.get()

            scores = {}

            for d in ll:
                di, dj = dij[d]
                i2 = y + di
                j2 = x + dj

                if 0 <= i2 < N and 0 <= j2 < N and (i2, j2) not in visited1:  # and not visited[i2][j2]:
                    if di == 0 and vertical_bars[y][min(x, j2)] == '0' or dj == 0 and horizontal_bars[min(y, i2)][
                        x] == '0':
                        score = factor1 * len([(a, b) in visited or N in (a, b) or -1 in (a, b) for (a, b) in
                                               ((i2, j2 + 1), (i2 - 1, j2), (i2 + 1, j2), (i2, j2 - 1))])
                        score += factor2 * (depth - turnsPerSpot[i2][j2][-1])
                        scores[(i2, j2, d)] = score

            for ((i2, j2, d), score) in list(
                {a: b for a, b in sorted(scores.items(), key=lambda x: x[1], reverse=True)}.items()):

                if (i2, j2) == toGo or (not toGo and (i2, j2) in visited):
                    v = True
                    break
                if not toGo and counterReshit < 50 and ((initDepth + depth - turnsPerSpot[i2][j2][-1] > N * N // 2 and
                                                         dirt_quantity_delta[i2][j2] > avgDirtDelta) or (
                                                            initDepth + depth - turnsPerSpot[i2][j2][
                                                            -1] > N * N // 3 and dirt_quantity_delta[i2][
                                                                j2] > 10 * avgDirtDelta)):
                    v = True
                    counterReshit += 1
                    break

                q.put((i2, j2, path + [(i2, j2, dir[d])], depth + 1), factor3 * (depth - initDepth) - score)
                visited1.add((i2, j2))
            if v:
                path += [(i2, j2, dir[d])]
                pathSet = {(a, b) for (a, b, c) in path}
                break

        for index in range(len(path)):
            (a, b, dd) = path[index]
            turnsPerSpot[a][b] += (depth - index,)  # ou initDepth+index

            if (a, b) in visited:
                nbVisited -= 1
                visited.remove((a, b))
            currentPath += dd

        (i, j) = (i2, j2)
    score = 0
    (i, j, depth) = (0, 0, 0)

    for y in range(N):
        for x in range(N):

            infirstCycle = 0
            inglobalCycle = 0

            for i in range(len(turnsPerSpot[y][x]) - 1):
                i1, i2 = turnsPerSpot[y][x][i], turnsPerSpot[y][x][i + 1]
                n = (i2 - i1)

                infirstCycle += (n * (n + 1))
                inglobalCycle += (n * (n + 1))

            n = len(currentPath) - turnsPerSpot[y][x][-1]
            infirstCycle += (n * (n + 1))

            n = len(currentPath) + turnsPerSpot[y][x][1] - turnsPerSpot[y][x][-1]
            inglobalCycle += (n * (n + 1))

            for i in range(1, len(turnsPerSpot[y][x]) - 1):
                i1, i2 = turnsPerSpot[y][x][i], turnsPerSpot[y][x][i + 1]
                n = (i2 - i1)

                inglobalCycle += (n * (n + 1))

            n = len(currentPath) - turnsPerSpot[y][x][-1]
            inglobalCycle += (n * (n + 1))

            score += (inglobalCycle - infirstCycle) * dirt_quantity_delta[y][x] / 2

    score /= len(currentPath)

    if score < bestScore:
        best = currentPath
        bestScore = score

    time_fin_it = process_time()
    it_duration = max(time_fin_it - time_new_it, it_duration)
    time_new_it = time_fin_it

print(best)
