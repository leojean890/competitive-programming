import random
import sys
from collections import deque, defaultdict
from time import process_time
import heapq
from typing import List, Tuple

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: int):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]

globalScores = {".":1,"*":3,"B":6}

def isolated(r, c, depth, currGrid):
    q = deque()
    q.appendleft((r,c))
    visited = {(r,c)}
    counter = 6
    if currGrid[r][c] == "T" or depth >= reachedByWater[(r, c)]:
        return 0
    while q:
        (y,x) = q.pop()
        #print(y,x,file=sys.stderr)

        for a, b in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if inGrid(a, b) and waterPasses(currGrid[a][b]) and (a, b) not in visited:
                currVal = currGrid[a][b]
                if currVal == "T" or depth >= reachedByWater[(a, b)]:
                    return 0
                q.appendleft((a, b))
                visited.add((a, b))
                counter += globalScores[currVal]

    return counter


def beam(r,c,grid):
    q = deque()
    q.appendleft((r,c,0,[[grid[y][x] for x in range(W)] for y in range(H)],[], {(r,c)}, 0, 0))
    #visited = {(y,x)}

    best = None
    bestScore = 0
    width = 3500
    currentDepth = 0

    while q:
        (y,x,depth, currGrid, moves, allPos, lastPutDelay, value) = q.pop()
        score = isolated(y,x,depth,currGrid)
        if score > bestScore:
            bestScore = score
            best = (y,x,depth, currGrid, moves)
        if process_time() - start_time > 9*currentTick/tickLength:
            return best

        if currentDepth < depth and len(q) > width:
            q1 = PriorityQueue()
            # q.appendleft()
            for (y,x,depth, currGrid, moves, allPos, lastPutDelay, value) in q:
                q1.put((y,x,depth, currGrid, moves, allPos, lastPutDelay, value), value)
            nq = deque()
            for i in range(width):
                (y, x, depth, currGrid, moves, allPos, lastPutDelay, value) = q1.get()
                nq.appendleft((y,x,depth, currGrid, moves, allPos, lastPutDelay, value))
            q = nq
        currentDepth = depth

        for a,b,d in ((y+1,x," D"),(y-1,x," U"),(y,x+1," R"),(y,x-1," L")):
            if inGrid(a, b) and canBuild(currGrid[a][b]):# and (a, b) not in visited:

                ngrid = []
                for row in currGrid:
                    ngrid.append(row.copy())
                ngrid[a][b] = "#"

                ev = depth
                counter = 0
                for (aa,bb) in ((a-1,b),(a+1,b),(a,b+1),(a,b-1),(a+1,b+1),(a+1,b-1),(a-1,b+1),(a-1,b-1)):
                    if not inGrid(aa, bb) or currGrid[aa][bb] == "#":
                        counter += 1

                if counter in (1,2):
                    ev -= counter*30

                ev -= 20 * lastPutDelay

                q.appendleft((y,x, depth+1, ngrid, moves+[str(y) + " " + str(x) + " B"+d], allPos, 0, ev))

                if (a,b) not in allPos:

                    ngrid2 = []
                    for row in currGrid:
                        ngrid2.append(row.copy())
                    ngrid2[a][b] = "B"
                    ngrid2[y][x] = "."

                    ev = depth - 10

                    for (wy,wx) in waters:
                        ev -= (abs(a-wy) + abs(b-wx))/4

                    q.appendleft((a,b, depth+1, ngrid2, moves+[str(y) + " " + str(x) + " M"+d], allPos|{(a,b)}, lastPutDelay + 1, ev))


def inGrid(row, col):
    return row >= 0 and row < H and col >= 0 and col < W


def canBuild(c):
    return c == '.' or c == '*'


def waterPasses(c):
    return c in ('.', '*', "B","T")


def isolated_sa(r, c, chosen):
    q = deque()
    q.appendleft((r,c))
    visited = {(r,c)}
    counter = 0

    while q:
        (y,x) = q.pop()

        for a, b in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if inGrid(a, b) and (a, b) not in walls and (a, b) not in chosen and (a, b) not in visited:
                if abs(a - r) > M1 or M1 < abs(b - c) or abs(a - r) + abs(b - c) > M2:
                    return -100000

                currVal = grid[a][b]
                if currVal == "T":
                    return -100000
                q.appendleft((a, b))
                visited.add((a, b))
                counter += globalScores[currVal] if currVal != "B" else 1

    return counter


def sa(pos):
    (r,c) = pos
    chosen = set()

    acceptedSpots = []

    for i in range(H):
        for j in range(W):
            if ((m < abs(i-r) < M and 0 <= abs(j-c) < M) or (m < abs(j-c) < M and 0 <= abs(i-r) < M)) and (i,j) not in walls:
                acceptedSpots.append((i,j))#inGrid(aa, bb)
    bestScore = 0
    found = 0
    nbIt = 0
    while found <= 0:#eval : taille zone - nb de caisses
        a, b = random.choice(acceptedSpots)
        if (a,b) not in chosen:
            counter = 0
            for (aa, bb) in ((a - 1, b), (a + 1, b), (a, b + 1), (a, b - 1), (a + 1, b + 1), (a + 1, b - 1), (a - 1, b + 1),(a - 1, b - 1)):
                if (aa, bb) in walls or (aa, bb) in chosen:#not inGrid(aa, bb) or  ne pas compter ça car ne marche pas
                    counter += 1

            if counter < 4 or (nbIt > 100 and counter < 5) or (nbIt > 200 and counter < 6) or (nbIt > 300 and counter < 7) or (nbIt > 400 and counter < 8):
                chosen.add((a,b))

                found = isolated_sa(r, c, chosen)
                bestScore = found - len(chosen)
            else:
                nbIt += 1

    best = chosen.copy()

    while process_time() - start_time < 9.5:
        current = chosen.copy()

        nbMut = random.randint(1,20)
        changed = False
        for i in range(nbMut):
            a, b = random.choice(acceptedSpots)
            if (a, b) not in current:
                counter = 0
                for (aa, bb) in (
                (a - 1, b), (a + 1, b), (a, b + 1), (a, b - 1), (a + 1, b + 1), (a + 1, b - 1), (a - 1, b + 1),
                (a - 1, b - 1)):
                    if (aa, bb) in walls or (aa, bb) in current: 
                        counter += 1

                if counter < 3:
                    current.add((a, b))
                    changed = True
            else:
                current.remove((a, b))
                changed = True

        if changed:

            score = isolated_sa(r,c,current) - len(current)
            if score > bestScore:
                bestScore = score
                best = current
                chosen = current
                print(chosen, file=sys.stderr)


    return best


H = int(input())
start_time = process_time()
W = int(input())
T = int(input())
B = int(input())
S = int(input())
builders = set()
waters = set()
flowers = set()
walls = set()
reachedByWater = {}


M = 12
M1 = 11
M2 = 22
m = 4

M = M*(W+H)//(2*30)
M1 = M2*(W+H)//(2*30)
M2 = M2*(W+H)//(2*30)
m = m*(W+H)//(2*30)

# read grid
grid = [[' ' for x in range(W)] for y in range(H)]
for r in range(H):
    for c in range(W):
        grid[r][c] = input()
        reachedByWater[(r,c)] = 10000
        if grid[r][c] == 'B':
            builders.add((r,c))
        elif grid[r][c] == 'T':
            waters.add((r,c))
        elif grid[r][c] == '*':
            flowers.add((r,c))
        elif grid[r][c] == '#':
            walls.add((r,c))


for water in waters:
    q = deque()
    q.appendleft((water, S-1))
    visited = {water}

    while q:
        ((y,x), depth) = q.pop()
        if depth < reachedByWater[(y,x)]:
            reachedByWater[(y, x)] = depth
        for a,b in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if inGrid(a, b) and waterPasses(grid[a][b]) and (a, b) not in visited:
                q.appendleft(((a,b), depth+1))
                visited.add((a,b))

sortedReachedByWater = list(sorted(reachedByWater.items(), key=lambda t: t[1], reverse=True))

nbT = 0
for a,b in sortedReachedByWater:
    if b < 1000:
        nbT = b
        for (y, x) in builders:
            if abs(y - a[0]) + abs(x - a[1]) > b - 1:
                B -= 1
        break


if H < 15 or W < 15 or (nbT < 30 and B == 3) or (nbT < 35 and B == 2) or B == 1 or nbT < 25:

    allMoves = {}

    currentTick = 0
    tickLength = len(builders)
    for (y, x) in builders:
        currentTick += 1
        sim = beam(y, x, grid)
        if sim:
            (a, b, depth, grid, moves) = sim
            allMoves[(y, x)] = moves.copy()

    turns = S + 20
    print(turns)

    for turn in range(turns):
        moves = []
        for move in allMoves.values():
            if len(move) > turn:
                moves.append(move[turn])

        print(len(moves))
        for s in moves:
            print(s)

else:
    for a,b in sortedReachedByWater:
        if b < 1000:
            res = sa(a)
            break

    movesPerTurn = defaultdict(list)

    def dirPerPos(dy, dx):
        if dy == -1:
            return "D"
        if dy == 1:
            return "U"
        if dx == -1:
            return "R"
        return "L"

    def bfs(y, x, target):
        q = deque()
        q.appendleft((y,x,None))
        visited = {(y,x)}

        while q:
            y,x,first = q.pop()
            if (y,x) == target:
                return first

            for a, b, d in ((y + 1, x, " D"), (y - 1, x, " U"), (y, x + 1, " R"), (y, x - 1, " L")):
                if inGrid(a, b) and canBuild(grid[a][b]) and (a, b) not in visited:
                    q.appendleft((a,b, (a,b,d) if not first else first))
                    visited.add((a,b))


    turn = 0
    while len(res) > 0:
        newBuilders = []
        for (y, x) in builders:
            if len(res) == 0:
                newBuilders.append((y, x))
                continue
            if reachedByWater[(y, x)] <= turn:
                newBuilders.append((y, x))
                continue


            closest = None
            closestDist = sys.maxsize
            for (a, b) in res:
                d = abs(y-a) + abs(x-b)
                if d < closestDist:
                    closestDist = d
                    closest = (a,b)

            if closestDist > reachedByWater[closest] - turn - 1:
                for (a,b) in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if inGrid(a, b) and canBuild(grid[a][b]) and reachedByWater[(a, b)] > turn:
                        d = dirPerPos(y - a, x - b)
                        movesPerTurn[turn].append(str(y) + " " + str(x) + " B " + d)
                        grid[a][b] = "#"
                        if (a,b) in res:
                            res.remove((a,b))
                        newBuilders.append((y, x))
                        break
                continue
            if closestDist > 1:
                rrr = bfs(y,x,closest)
                if rrr:
                    (a, b, d) = rrr
                    if reachedByWater[(a,b)] <= turn:
                        continue
                    movesPerTurn[turn].append(str(y) + " " + str(x) + " M" + d)
                    grid[a][b] = "B"
                    grid[y][x] = "."
                    y,x=a,b
            elif closestDist == 1:
                (a,b) = closest
                if reachedByWater[(a, b)] <= turn:
                    newBuilders.append((a, b))
                    continue
                d = dirPerPos(y - a, x - b)
                movesPerTurn[turn].append(str(y) + " " + str(x) + " B " + d)
                res.remove(closest)
                grid[a][b] = "#"

            else:
                for (a,b,d) in ((y+1,x," D"),(y-1,x, " U"),(y,x+1, " R"),(y,x-1, " L")):
                    if inGrid(a, b) and canBuild(grid[a][b]) and reachedByWater[(a, b)] > turn:
                        movesPerTurn[turn].append(str(y) + " " + str(x) + " M" + d)
                        grid[a][b] = "B"
                        grid[y][x] = "."
                        y, x = a, b
                        break
            newBuilders.append((y,x))
        builders = newBuilders.copy()
        turn += 1
        if turn > nbT:
            break

    if len(movesPerTurn[turn]) > 0:
        turn += 1

    for i in range(4):
        newBuilders = []
        for (y, x) in builders:
            if reachedByWater[(y, x)] > turn:
                for (a,b) in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if inGrid(a,b) and canBuild(grid[a][b]) and reachedByWater[(a,b)] > turn:
                        d = dirPerPos(y - a, x - b)
                        movesPerTurn[turn].append(str(y) + " " + str(x) + " B " + d)
                        grid[a][b] = "#"
                        newBuilders.append((y,x))
                        break
        turn += 1
        builders = newBuilders.copy()

    print(len(movesPerTurn))

    for turn in range(len(movesPerTurn)):
        print(len(movesPerTurn[turn]))
        for s in movesPerTurn[turn]:
            print(s)

sys.stdout.flush()
