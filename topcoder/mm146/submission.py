import random
import sys
from collections import deque, defaultdict
from time import process_time
import heapq
from typing import List, Tuple
sys.setrecursionlimit(10000000)


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


BIG = 160
INIT = 16
MED = 2
LOW = 1


def closestDistToColor(grid, color, i, j):
  q = deque()
  q.appendleft((i,j,0))
  visited = {(i,j)}

  while q:
    (c, d, depth) = q.pop()
    if grid[c][d] == color and depth > 0:
      return depth
    for e,f in ((c+1,d), (c-1,d), (c,d+1), (c,d-1)):
      if 0 <= e < N and 0 <= f < N and grid[e][f] > 0 and (e,f) not in visited:
        q.appendleft((e,f,depth+1))
        visited.add((e,f))


def mc(remainingTime, grid, nTurns, allConnectedComponents, connectedComponentIndexPerSpot, sizesPerComponent, oldscore, actions):
  global bscore, best#, bcc
  while process_time() - start_time < remainingTime:
    if N > 0:
      x = random.randint(0, N-1)
      y = random.randint(0, N-1)
      while grid[y][x] == 0 or sizesPerComponent[connectedComponentIndexPerSpot[(y,x)]] == K:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)

      a, b = random.choice([(y+1,x), (y-1,x), (y,x+1), (y,x-1)])
      ntr = 0
      nttt = 0
      while a < 0 or b < 0 or a >= N or b >= N or grid[a][b] in (0, grid[y][x]) or sizesPerComponent[connectedComponentIndexPerSpot[(a,b)]] == K:
        ntr += 1
        nttt += 1
        if ntr >= 20:
          ntr = 0
          x = random.randint(0, N - 1)
          y = random.randint(0, N - 1)
          while grid[y][x] == 0 or sizesPerComponent[connectedComponentIndexPerSpot[(y,x)]] == K:
            x = random.randint(0, N - 1)
            y = random.randint(0, N - 1)

        a, b = random.choice([(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])

        if nttt >= 200:
          return

    

    grid[y][x], grid[a][b] = grid[a][b], grid[y][x]

    allConnectedComponents = []
    connectedComponentIndexPerSpot = {}
    sizesPerComponent = {}
    allVisitedSpots = set()

    for r in range(N):
      for c in range(N):
        if (r, c) not in allVisitedSpots and grid[r][c] != 0:
          q = deque()
          visited = {(r, c)}
          q.appendleft((r, c))

          while q:
            yy, xx = q.pop()
            connectedComponentIndexPerSpot[(yy, xx)] = len(allConnectedComponents)
            for (i, j) in ((yy + 1, xx), (yy - 1, xx), (yy, xx + 1), (yy, xx - 1)):
              if (i, j) not in visited and (i, j) not in allVisitedSpots and 0 <= i < N and 0 <= j < N and grid[i][j] == \
                  grid[yy][xx]:
                q.appendleft((i, j))
                visited.add((i, j))

          allVisitedSpots |= visited
          sizesPerComponent[len(allConnectedComponents)] = len(visited)
          allConnectedComponents.append(visited)

    
    actions += [(a,b,y,x)]

    score = P * len([size for size in sizesPerComponent.values() if size == K]) - nTurns

    if score > bscore:
      bscore = score
      best = actions[:]

    
    FACTOR1 = 2.5*N**2
    FACTOR2 = P*nbCasesValides/K
    if nTurns > FACTOR1:
      return
    if nTurns > 0.8*FACTOR2:
      return
    if score > oldscore:
      if nTurns > 0.7 * FACTOR2 or nTurns > 0.9*FACTOR1:
        if random.randint(1, 10) > 3:
          return

      elif nTurns > 0.6 * FACTOR2 or nTurns > 0.8*FACTOR1:
        if random.randint(1, 10) > 6:
          return

      elif nTurns > 0.5 * FACTOR2 or nTurns > 0.7*FACTOR1:
        if random.randint(1, 10) > 8:
          return

      elif nTurns > 0.4 * FACTOR2 or nTurns > 0.6*FACTOR1:
        if random.randint(1, 10) > 9:
          return

      elif nTurns > nTurns > 0.3 * FACTOR2 or nTurns > 0.5*FACTOR1:
        if random.randint(1, 100) > 95:
          return

      elif nTurns > 0.2 * FACTOR2 or nTurns > 0.4*FACTOR1:
        if random.randint(1, 100) > 98:
          return
    oldscore = score
    nTurns += 1


N = int(input())
start_time = process_time()
C = int(input())
K = int(input())
P = int(input())

initcounters = defaultdict(int)
initfree = set()
print(N, file=sys.stderr)
print(C, file=sys.stderr)
print(K, file=sys.stderr)
print(P, file=sys.stderr)

# read grid
initgrid = [[-1 for x in range(N)] for y in range(N)]
for r in range(N):
  for c in range(N):
    initgrid[r][c] = int(input())
    if initgrid[r][c] > 0:
      initcounters[initgrid[r][c]] += 1
      initfree.add((r,c))


best = []
bestGrid = []
bscore = 0
nbRollouts = 0


if K > 5 and C > 6:
  allConnectedComponents = []
  connectedComponentIndexPerSpot = {}
  sizesPerComponent = {}
  allVisitedSpots = set()

  for r in range(N):
    for c in range(N):
      if (r,c) not in allVisitedSpots and initgrid[r][c] != 0:
        q = deque()
        visited = {(r,c)}
        q.appendleft((r,c))

        while q:
          y, x = q.pop()
          connectedComponentIndexPerSpot[(y,x)] = len(allConnectedComponents)
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) not in visited and (a,b) not in allVisitedSpots and 0 <= a < N and 0 <= b < N and initgrid[a][b] == initgrid[y][x]:
              q.appendleft((a, b))
              visited.add((a, b))

        allVisitedSpots |= visited
        sizesPerComponent[len(allConnectedComponents)] = len(visited)
        allConnectedComponents.append(visited)

  nbCasesValides = len(allVisitedSpots)

  iscore = P*len([size for size in sizesPerComponent.values() if size == K])
  bscore = iscore
  while process_time() - start_time < 5:
    nGrid = []
    for line in initgrid:
      nGrid.append(line.copy())

    nallConnectedComponents = []

    for component in allConnectedComponents:
      nallConnectedComponents.append(component.copy())

    nconnectedComponentIndexPerSpot = {}

    for position, component in connectedComponentIndexPerSpot.items():
      nconnectedComponentIndexPerSpot[position] = component

    nsizesPerComponent = {}

    for component, size in sizesPerComponent.items():
      nsizesPerComponent[component] = size

    mc(5, nGrid, 1, nallConnectedComponents, nconnectedComponentIndexPerSpot, nsizesPerComponent, iscore, [])


    nbRollouts += 1


elif K > 2 or C < 4:
  while process_time() - start_time < 5.5:

    grid = []
    for line in initgrid:
      grid.append(line.copy())

    counters = initcounters.copy()
    free = initfree.copy()

    initLen = len(free)

    futurePos = {}

    sortedColors = list(counters.keys()) # ajouter des probas grace a la ligne ci dessus

    while len(free) > 0.15*initLen:
      q = deque()
      q.appendleft((0,0))
      visited = {(0,0)}
      while q:
        y, x = q.pop()
        if (y,x) in free:
          break

        for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
          if (a,b) not in visited and N > a >= 0 and N > b >= 0:# and grid[a][b] > 0:
            visited.add((a,b))
            q.appendleft((a,b))

      random.shuffle(sortedColors)

      for color in sortedColors:
        if counters[color] > 0:
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) in futurePos and futurePos[(a,b)] == color:
              break
          else:
            chosenColor = color
            break


      justPut = set()
      sortedJustPut = []

      q = PriorityQueue()
      q.put((y, x), x + y)
      futurePos[(y, x)] = chosenColor
      justPut.add((y, x))
      sortedJustPut.append((y, x))
      free.remove((y, x))

      while not q.empty() and len(justPut) < K:
        y, x = q.get()

        for (a, b) in ((y, x - 1), (y - 1, x), (y, x + 1), (y + 1, x)):
          if (a, b) in free:# and (a, b) not in justPut:
            for (i, j) in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
              if (i, j) not in justPut and (i, j) in futurePos and futurePos[(i, j)] == chosenColor:
                break
            else:
              if len(justPut) < K:
                q.put((a, b), a + b)
                futurePos[(a, b)] = chosenColor
                counters[chosenColor] -= 1
                free.remove((a, b))
                justPut.add((a, b))


    candidate = []
    settled = set()
    while futurePos:
      #print(len(futurePos), len(free))
      q = deque()
      q.appendleft((0,0))
      visited = {(0,0)}
      while q:
        y, x = q.pop()
        if (y,x) in futurePos:
          break

        for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
          if (a,b) not in visited and N > a >= 0 and N > b >= 0:# and grid[a][b] > 0:
            visited.add((a,b))
            q.appendleft((a,b))

      q = deque()
      q.appendleft((y,x,[(y,x)]))
      visited = {(y,x)}
      settled.add((y,x))

      while q:
        i, j,path = q.pop()
        if grid[i][j] == futurePos[(y,x)]:
          break

        for (a,b) in ((i+1,j), (i-1,j), (i,j+1), (i,j-1)):
          if (a,b) not in visited|settled and N > a >= 0 and N > b >= 0 and grid[a][b] > 0:# and grid[a][b] > 0:
            visited.add((a,b))
            q.appendleft((a,b,[(a,b)]+path))

      for i in range(len(path)-1):
        a,b=path[i]
        c,d=path[i+1]
        candidate.append((a,b,c,d))
        grid[a][b], grid[c][d] = grid[c][d], grid[a][b]
        #print((a,b,c,d), futurePos[(y,x)], file=sys.stderr)
      del futurePos[(y,x)]

    allConnectedComponents = []
    connectedComponentIndexPerSpot = {}
    sizesPerComponent = {}
    allVisitedSpots = set()

    for r in range(N):
      for c in range(N):
        if (r, c) not in allVisitedSpots and grid[r][c] != 0:
          q = deque()
          visited = {(r, c)}
          q.appendleft((r, c))

          while q:
            yy, xx = q.pop()
            connectedComponentIndexPerSpot[(yy, xx)] = len(allConnectedComponents)
            for (i, j) in ((yy + 1, xx), (yy - 1, xx), (yy, xx + 1), (yy, xx - 1)):
              if (i, j) not in visited and (i, j) not in allVisitedSpots and 0 <= i < N and 0 <= j < N and grid[i][j] == \
                  grid[yy][xx]:
                q.appendleft((i, j))
                visited.add((i, j))

          allVisitedSpots |= visited
          sizesPerComponent[len(allConnectedComponents)] = len(visited)
          allConnectedComponents.append(visited)


    score = P * len([size for size in sizesPerComponent.values() if size == K]) - len(candidate)

    if score > bscore:
      bscore = score
      best = candidate[:]
      bestGrid = grid
      print("bscore", bscore, file=sys.stderr)

    nbRollouts += 1

  allConnectedComponents = []
  connectedComponentIndexPerSpot = {}
  sizesPerComponent = {}
  allVisitedSpots = set()
  bestp1 = best[:]
  bscorep1 = bscore

  for r in range(N):
    for c in range(N):
      if (r,c) not in allVisitedSpots and bestGrid[r][c] != 0:
        q = deque()
        visited = {(r,c)}
        q.appendleft((r,c))

        while q:
          y, x = q.pop()
          connectedComponentIndexPerSpot[(y,x)] = len(allConnectedComponents)
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) not in visited and (a,b) not in allVisitedSpots and 0 <= a < N and 0 <= b < N and bestGrid[a][b] == bestGrid[y][x]:
              q.appendleft((a, b))
              visited.add((a, b))

        allVisitedSpots |= visited
        sizesPerComponent[len(allConnectedComponents)] = len(visited)
        allConnectedComponents.append(visited)

  nbCasesValides = len(allVisitedSpots)

  bscore = bscorep1# iscore
  while process_time() - start_time < 7.5:
    nGrid = []
    for line in bestGrid:
      nGrid.append(line.copy())

    nallConnectedComponents = []

    for component in allConnectedComponents:
      nallConnectedComponents.append(component.copy())

    nconnectedComponentIndexPerSpot = {}

    for position, component in connectedComponentIndexPerSpot.items():
      nconnectedComponentIndexPerSpot[position] = component

    nsizesPerComponent = {}

    for component, size in sizesPerComponent.items():
      nsizesPerComponent[component] = size

    mc(7.5, nGrid, len(bestp1), nallConnectedComponents, nconnectedComponentIndexPerSpot, nsizesPerComponent, bscorep1, bestp1[:])


    nbRollouts += 1

else:

  while process_time() - start_time < 5.5:

    grid = []
    for line in initgrid:
      grid.append(line.copy())

    counters = initcounters.copy()
    free = initfree.copy()

    initLen = len(free)

    futurePos = {}
    candidate = []

    sortedColors = list(counters.keys()) # ajouter des probas grace a la ligne ci dessus
    allSettled = set()

    while len(free) > 0.03*initLen:

      q = deque()
      q.appendleft((0,0))
      visited = {(0,0)}
      while q:
        y, x = q.pop()
        if (y,x) in free:
          break

        for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
          if (a,b) not in visited and N > a >= 0 and N > b >= 0:# and grid[a][b] > 0:
            visited.add((a,b))
            q.appendleft((a,b))

      random.shuffle(sortedColors)
      bestPut = None
      bestColor = None
      bestPaths = None
      bestFuturePos = None
      minLength = sys.maxsize
      fy, fx = y, x

      for color in sortedColors:
        if counters[color] > 0: # > K
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) in futurePos and futurePos[(a,b)] == color:
              break
          else:
            chosenColor = color
            nfuturePos = futurePos.copy()

            nGrid = []
            for line in grid:
              nGrid.append(line.copy())

            nbPut = 0
            changed = True


            justPut = set()
            sortedJustPut = []

            q = PriorityQueue()
            q.put((y,x),x+y)
            nfuturePos[(y, x)] = chosenColor
            justPut.add((y, x))
            sortedJustPut.append((y, x))

            while not q.empty() and len(justPut) < K:
              y, x = q.get()

              for (a, b) in ((y, x - 1), (y - 1, x), (y, x + 1), (y + 1, x)):
                if (a,b) in free and (a,b) not in justPut:
                  for (i, j) in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if (i,j) not in justPut and (i, j) in nfuturePos and nfuturePos[(i, j)] == chosenColor:
                      break
                  else:
                    if len(justPut) < K:
                      q.put((a,b), a + b)
                      nfuturePos[(a,b)] = chosenColor
                      justPut.add((a,b))
                      sortedJustPut.append((a,b))
                    #break

            if len(justPut) < K:
              continue
            
            sortedJustPut = list(sorted(sortedJustPut, key=lambda h:h[0]+h[1]))
            settled = set()
            foundPaths = []
            for (y,x) in sortedJustPut:
              q = deque()
              q.appendleft((y,x,[(y,x)]))
              visited = {(y,x)}
              settled.add((y,x))

              while q:
                i, j, path = q.pop()
                if nGrid[i][j] == nfuturePos[(y,x)]:
                  foundPaths.append(path)
                  for i in range(len(path) - 1):
                    a, b = path[i]
                    c, d = path[i + 1]
                    nGrid[a][b], nGrid[c][d] = nGrid[c][d], nGrid[a][b]
                  break

                for (a,b) in ((i+1,j), (i-1,j), (i,j+1), (i,j-1)):
                  if (a,b) not in visited|settled|allSettled and N > a >= 0 and N > b >= 0 and nGrid[a][b] > 0:
                    visited.add((a,b))
                    q.appendleft((a,b,[(a,b)]+path))

            score = sum([len(path) for path in foundPaths])
            if score < minLength:
              minLength = score
              bestPaths = foundPaths
              bestFuturePos = nfuturePos
              bestPut = justPut
              bestColor = chosenColor

      if bestPaths:
        for path in bestPaths:
          for i in range(len(path)-1):
            a,b=path[i]
            c,d=path[i+1]
            candidate.append((a,b,c,d))
            grid[a][b], grid[c][d] = grid[c][d], grid[a][b]
        futurePos = bestFuturePos
        free = free.difference(bestPut)  # settled
        allSettled |= bestPut
        counters[bestColor] -= len(bestPut)
      else:
        free.remove((fy,fx))
        allSettled.add((fy,fx))
        futurePos[(fy,fx)] = grid[fy][fx]
        counters[grid[fy][fx]] -= 1

    allConnectedComponents = []
    connectedComponentIndexPerSpot = {}
    sizesPerComponent = {}
    allVisitedSpots = set()

    for r in range(N):
      for c in range(N):
        if (r, c) not in allVisitedSpots and grid[r][c] != 0:
          q = deque()
          visited = {(r, c)}
          q.appendleft((r, c))

          while q:
            yy, xx = q.pop()
            connectedComponentIndexPerSpot[(yy, xx)] = len(allConnectedComponents)
            for (i, j) in ((yy + 1, xx), (yy - 1, xx), (yy, xx + 1), (yy, xx - 1)):
              if (i, j) not in visited and (i, j) not in allVisitedSpots and 0 <= i < N and 0 <= j < N and grid[i][j] == \
                  grid[yy][xx]:
                q.appendleft((i, j))
                visited.add((i, j))

          allVisitedSpots |= visited
          sizesPerComponent[len(allConnectedComponents)] = len(visited)
          allConnectedComponents.append(visited)


    score = P * len([size for size in sizesPerComponent.values() if size == K]) - len(candidate)

    if score > bscore:
      bscore = score
      best = candidate[:]
      bestGrid = grid
      print("i bscore", bscore, file=sys.stderr)

    nbRollouts += 1

  allConnectedComponents = []
  connectedComponentIndexPerSpot = {}
  sizesPerComponent = {}
  allVisitedSpots = set()
  bestp1 = best[:]
  bscorep1 = bscore

  for r in range(N):
    for c in range(N):
      if (r,c) not in allVisitedSpots and bestGrid[r][c] != 0:
        q = deque()
        visited = {(r,c)}
        q.appendleft((r,c))

        while q:
          y, x = q.pop()
          connectedComponentIndexPerSpot[(y,x)] = len(allConnectedComponents)
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) not in visited and (a,b) not in allVisitedSpots and 0 <= a < N and 0 <= b < N and bestGrid[a][b] == bestGrid[y][x]:
              q.appendleft((a, b))
              visited.add((a, b))

        allVisitedSpots |= visited
        sizesPerComponent[len(allConnectedComponents)] = len(visited)
        allConnectedComponents.append(visited)

  nbCasesValides = len(allVisitedSpots)

  bscore = bscorep1# iscore
  while process_time() - start_time < 7:
    nGrid = []
    for line in bestGrid:
      nGrid.append(line.copy())

    nallConnectedComponents = []

    for component in allConnectedComponents:
      nallConnectedComponents.append(component.copy())

    nconnectedComponentIndexPerSpot = {}

    for position, component in connectedComponentIndexPerSpot.items():
      nconnectedComponentIndexPerSpot[position] = component

    nsizesPerComponent = {}

    for component, size in sizesPerComponent.items():
      nsizesPerComponent[component] = size

    mc(7, nGrid, len(bestp1), nallConnectedComponents, nconnectedComponentIndexPerSpot, nsizesPerComponent, bscorep1, bestp1[:])

    nbRollouts += 1

if False:
  allConnectedComponents = []
  connectedComponentIndexPerSpot = {}
  sizesPerComponent = {}
  allVisitedSpots = set()

  for r in range(N):
    for c in range(N):
      if (r,c) not in allVisitedSpots and initgrid[r][c] != 0:
        q = deque()
        visited = {(r,c)}
        q.appendleft((r,c))

        while q:
          y, x = q.pop()
          connectedComponentIndexPerSpot[(y,x)] = len(allConnectedComponents)
          for (a,b) in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
            if (a,b) not in visited and (a,b) not in allVisitedSpots and 0 <= a < N and 0 <= b < N and initgrid[a][b] == initgrid[y][x]:
              q.appendleft((a, b))
              visited.add((a, b))

        allVisitedSpots |= visited
        sizesPerComponent[len(allConnectedComponents)] = len(visited)
        allConnectedComponents.append(visited)

  nbCasesValides = len(allVisitedSpots)

  iscore = P*len([size for size in sizesPerComponent.values() if size == K])
  bscore = iscore
  while process_time() - start_time < 5:
    nGrid = []
    for line in initgrid:
      nGrid.append(line.copy())

    nallConnectedComponents = []

    for component in allConnectedComponents:
      nallConnectedComponents.append(component.copy())

    nconnectedComponentIndexPerSpot = {}

    for position, component in connectedComponentIndexPerSpot.items():
      nconnectedComponentIndexPerSpot[position] = component

    nsizesPerComponent = {}

    for component, size in sizesPerComponent.items():
      nsizesPerComponent[component] = size

    mc(5, nGrid, 1, nallConnectedComponents, nconnectedComponentIndexPerSpot, nsizesPerComponent, iscore, [])


    nbRollouts += 1


while process_time() - start_time < 9.5:#tuner les limites de temps et le random(50)
  grid = []
  for line in initgrid:
    grid.append(line.copy())

  current = []
  for action in best:
    pr = random.randint(1,100)
    if pr > 1:
      current.append(action)
      a, b, y, x = action
      grid[y][x], grid[a][b] = grid[a][b], grid[y][x]


  allConnectedComponents = []
  connectedComponentIndexPerSpot = {}
  sizesPerComponent = {}
  allVisitedSpots = set()

  for r in range(N):
    for c in range(N):
      if (r, c) not in allVisitedSpots and grid[r][c] != 0:
        q = deque()
        visited = {(r, c)}
        q.appendleft((r, c))

        while q:
          yy, xx = q.pop()
          connectedComponentIndexPerSpot[(yy, xx)] = len(allConnectedComponents)
          for (i, j) in ((yy + 1, xx), (yy - 1, xx), (yy, xx + 1), (yy, xx - 1)):
            if (i, j) not in visited and (i, j) not in allVisitedSpots and 0 <= i < N and 0 <= j < N and grid[i][j] == \
                grid[yy][xx]:
              q.appendleft((i, j))
              visited.add((i, j))

        allVisitedSpots |= visited
        sizesPerComponent[len(allConnectedComponents)] = len(visited)
        allConnectedComponents.append(visited)

  score = P * len([size for size in sizesPerComponent.values() if size == K]) - len(current)

  if score > bscore:
    bscore = score
    best = current[:]
    print("bscore", bscore, file=sys.stderr)
  nbRollouts += 1

print("bscore", bscore, file=sys.stderr)
print("nbRollouts", nbRollouts, file=sys.stderr)
print(len(best))

for action in best:
  print(*action)

sys.stdout.flush()
