from collections import deque, defaultdict
from time import process_time
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


N, M = [int(i) for i in input().split()]
start_time = process_time()
si, sj = [int(i) for i in input().split()]

allLetters = set()
letters = []

for j in range(N):
    letters.append(input())
    for l in letters[-1]:
        allLetters.add(l)

nbLetters = len(allLetters)
allBfsDists = defaultdict(dict)

for i in range(N):
    for j in range(N):
        q = deque()
        q.appendleft((i, j, 0))
        visited = {(i, j)}

        while len(allBfsDists[(i,j)].items()) < nbLetters:
            (y, x, depth) = q.pop()
            if letters[y][x] not in allBfsDists[(i,j)]:
                allBfsDists[(i,j)][letters[y][x]] = (y, x, depth)

            for a, b in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= a < N and 0 <= b < N and (a, b) not in visited:
                    visited.add((a, b))
                    q.appendleft((a, b, depth + 1))

words = []

for j in range(M):
    words.append(input())

nwords = words.copy()
ci, cj = si, sj

bestScore = sys.maxsize
bestActions = None
currentDepth = 0

q = PriorityQueue()
q.put((0, 0, si, sj, nwords, []),0)

while not q.empty():
    (score,dpth,ci,cj,nwords,actions) = q.get()

    if currentDepth < dpth:
        nq = PriorityQueue()
        nq.put((score, dpth, ci, cj, nwords, actions), score - 100 * dpth)

        for i in range(11):
            (score, dpth, ci, cj, nwords, actions) = q.get()
            nq.put((score, dpth, ci, cj, nwords, actions), score-100*dpth)

        q = nq
        currentDepth = dpth
        continue

    if not nwords:
        if score < bestScore:
            bestActions = actions
            bestScore = score
        continue


    for i in range(len(nwords)):
        ni, nj = ci, cj
        localScore = 0
        cActions = []

        for letter in nwords[i]:
            (y,x,depth) = allBfsDists[(ni,nj)][letter]

            ni, nj = y, x
            localScore += depth
            cActions.append((y,x))

        nnwords = nwords[:i] + nwords[i+1:]

        nactions = actions.copy()
        for action in cActions:
            nactions.append(action)

        q.put((score+localScore, dpth+1, ni, nj, nnwords,nactions), score+localScore-100*dpth)

for action in bestActions:
    print(*action)


