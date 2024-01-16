import math
import random
import sys
from collections import defaultdict, deque
from time import process_time


def getValidMoves(r,c, queens):
  possible = []
  for (dy, dx) in ((-1,1),(1,-1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0),(1,1)):
    y, x = r, c
    while 0 <= y+dy < N and 0 <= x+dx < N and (y+dy, x+dx) not in walls and not any((y+dy, x+dx) in queens[color] for color in range(C)):

      y += dy
      x += dx
      possible.append((y, x))

  return possible

#a, TSTA = sys.argv

t_start = 4
t_final = 100
N = int(input())
start_time = process_time()
C = int(input())

#a, nMut = sys.argv
nMut = 1#int(nMut)
step = 19#int(step)

walls = set()
queens = defaultdict(set)
amountsPerLine = {}
amountsPerCol = {}
amountsPerDiag = {} # x+y
amountsPerInvDiag = {} # (N-x)+y

for i in range(C):
  amountsPerLine[i] = defaultdict(int)
  amountsPerCol[i] = defaultdict(int)
  amountsPerDiag[i] = defaultdict(int)
  amountsPerInvDiag[i] = defaultdict(int)

# read grid
grid = [[-100 for x in range(N)] for y in range(N)]
for r in range(N):
  for c in range(N):
    grid[r][c] = int(input())
    color = grid[r][c] - 1

    if color > -1:
      ##print(color, C, file=sys.stderr)
      queens[color].add((r, c))
      amountsPerLine[color][r] += 1
      amountsPerCol[color][c] += 1
      amountsPerDiag[color][r+c] += 1
      amountsPerInvDiag[color][r+(N-c)] += 1
    if color == -2:
      walls.add((r,c))

if N > 9 and ( C == 1 or (C == 2 and len(walls) < 0.36*N*N) or (C == 3 and len(walls) < 0.28*N*N) or (C == 4 and len(walls) < 0.24*N*N) or (C == 5 and len(walls) < 0.1*N*N) ):
  initSortedQueens = {}
  moves = []

  for i in range(C):
    initSortedQueens[i] = list(sorted(queens[i], key=lambda x: x[0]+x[1]))

  MMM = sys.maxsize

  while process_time() - start_time < 0.5:

    nQueens = defaultdict(set)
    visited = walls.copy()

    possibilities = []

    for r in range(N):
      for c in range(N):
        if (r,c) not in visited:
          possibilities.append((r,c))

    amountsPerLine = {}
    amountsPerCol = {}
    amountsPerDiag = {}  # x+y
    amountsPerInvDiag = {}  # (N-x)+y

    for i in range(C):
      amountsPerLine[i] = defaultdict(int)
      amountsPerCol[i] = defaultdict(int)
      amountsPerDiag[i] = defaultdict(int)
      amountsPerInvDiag[i] = defaultdict(int)

    for color in range(C):
      while len(nQueens[color]) < len(queens[color]):
        l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and amountsPerLine[color][r] + amountsPerCol[color][c] + amountsPerDiag[color][r+c] + amountsPerInvDiag[color][r+(N-c)] == 0]
        if l:
          (r,c) = random.choice(l)
        else:
          l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and amountsPerLine[color][r] + amountsPerCol[color][c] + amountsPerDiag[color][r+c] + amountsPerInvDiag[color][r+(N-c)] == 1]
          if l:
            (r,c) = random.choice(l)
          else:
            l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and sum([1 for elt in [amountsPerLine[color][r] == 0, amountsPerCol[color][c] == 0, amountsPerDiag[color][r+c] == 0, amountsPerInvDiag[color][r+(N-c)]==0 ] if elt]) == 2 and sum([1 for elt in [amountsPerLine[color][r] == 1, amountsPerCol[color][c] == 1, amountsPerDiag[color][r+c] == 1, amountsPerInvDiag[color][r+(N-c)]==1 ] if elt]) == 2]

            (r,c) = random.choice(l)

        visited.add((r,c))
        nQueens[color].add((r,c))

        amountsPerLine[color][r] += 1
        amountsPerCol[color][c] += 1
        amountsPerDiag[color][r+c] += 1
        amountsPerInvDiag[color][r+(N-c)] += 1

    score = 0

    for color in range(C):

      for r in range(N):
        if amountsPerLine[color][r] > 1:
          score += (amountsPerLine[color][r] - 1) * (amountsPerLine[color][r]) // 2

      for c in range(N):
        if amountsPerCol[color][c] > 1:
          score += (amountsPerCol[color][c] - 1) * (amountsPerCol[color][c]) // 2

      for diag in amountsPerDiag[color]:
        if amountsPerDiag[color][diag] > 1:
          score += (amountsPerDiag[color][diag] - 1) * (amountsPerDiag[color][diag]) // 2

      for diag in amountsPerInvDiag[color]:
        if amountsPerInvDiag[color][diag] > 1:
          score += (amountsPerInvDiag[color][diag] - 1) * (amountsPerInvDiag[color][diag]) // 2


    MMM = min(MMM, score)
  bQueens = defaultdict(set)
  currQueens = defaultdict(set)
  print(MMM, file=sys.stderr, flush=True)
  bestS = sys.maxsize
  currS = sys.maxsize
  maxT = 0
  currT = process_time()
  while currT - start_time + maxT < 9.5:
    try:
      cQueens = {}
      visited = walls.copy()

      amountsPerLine = {}
      amountsPerCol = {}
      amountsPerDiag = {}  # x+y
      amountsPerInvDiag = {}  # (N-x)+y

      for color in range(C):
        amountsPerLine[color] = defaultdict(int)
        amountsPerCol[color] = defaultdict(int)
        amountsPerDiag[color] = defaultdict(int)
        amountsPerInvDiag[color] = defaultdict(int)

        cQueens[color] = set(random.sample(currQueens[color], random.randint(0, len(currQueens[color]))))

        for (r,c) in cQueens[color]:

          visited.add((r, c))

          amountsPerLine[color][r] += 1
          amountsPerCol[color][c] += 1
          amountsPerDiag[color][r + c] += 1
          amountsPerInvDiag[color][r + (N - c)] += 1

      possibilities = []

      for r in range(N):
        for c in range(N):
          if (r,c) not in visited:
            possibilities.append((r,c))


      for color in range(C):
        while len(cQueens[color]) < len(queens[color]):
          l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and amountsPerLine[color][r] + amountsPerCol[color][c] + amountsPerDiag[color][r+c] + amountsPerInvDiag[color][r+(N-c)] == 0]
          if l:
            (r,c) = random.choice(l)
          else:
            l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and amountsPerLine[color][r] + amountsPerCol[color][c] + amountsPerDiag[color][r+c] + amountsPerInvDiag[color][r+(N-c)] == 1]
            if l:
              (r,c) = random.choice(l)
            else:
              l = [(r,c) for (r,c) in possibilities if (r,c) not in visited and sum([1 for elt in [amountsPerLine[color][r] == 0, amountsPerCol[color][c] == 0, amountsPerDiag[color][r+c] == 0, amountsPerInvDiag[color][r+(N-c)]==0 ] if elt]) == 2 and sum([1 for elt in [amountsPerLine[color][r] == 1, amountsPerCol[color][c] == 1, amountsPerDiag[color][r+c] == 1, amountsPerInvDiag[color][r+(N-c)]==1 ] if elt]) == 2]

              (r,c) = random.choice(l)

          visited.add((r,c))
          cQueens[color].add((r,c))

          amountsPerLine[color][r] += 1
          amountsPerCol[color][c] += 1
          amountsPerDiag[color][r+c] += 1
          amountsPerInvDiag[color][r+(N-c)] += 1

      score = 0

      for color in range(C):

        for r in range(N):
          if amountsPerLine[color][r] > 1:
            score += (amountsPerLine[color][r] - 1) * (amountsPerLine[color][r]) // 2

        for c in range(N):
          if amountsPerCol[color][c] > 1:
            score += (amountsPerCol[color][c] - 1) * (amountsPerCol[color][c]) // 2

        for diag in amountsPerDiag[color]:
          if amountsPerDiag[color][diag] > 1:
            score += (amountsPerDiag[color][diag] - 1) * (amountsPerDiag[color][diag]) // 2

        for diag in amountsPerInvDiag[color]:
          if amountsPerInvDiag[color][diag] > 1:
            score += (amountsPerInvDiag[color][diag] - 1) * (amountsPerInvDiag[color][diag]) // 2


      #print(score, process_time() - start_time, file=sys.stderr, flush=True)

      if score > MMM+1:
        continue

      score *= N

      shouldBeInCQueens = set()
      isAlreadyInCQueens = set()
      colorPerPos = {}

      nqueens = defaultdict(set)

      for color in range(C):
        nqueens[color] = queens[color].copy()
        for (r,c) in cQueens[color]:
          shouldBeInCQueens.add((r, c))
          colorPerPos[(r,c)] = color

      tempMoves = []
      while shouldBeInCQueens:# or queens != cQueens:
        # on démarre du coin HG et on reconstruit la grille

        q = deque()
        q.appendleft((0, 0))
        visited = {(0, 0)}
        while q:
          y, x = q.pop()
          if (y, x) in shouldBeInCQueens:
            cy, cx = y,x
            break

          for (a, b) in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if (a, b) not in visited and N > a >= 0 and N > b >= 0:  # and grid[a][b] > 0:
              visited.add((a, b))
              q.appendleft((a, b))

        # ci dessous :
        # d'abord, déplacer la reine qui est placée ici si jamais y'en a une
        # (vers le bas pour pas péter le config actuelle déjà settée en haut)

        if colorPerPos[(cy, cx)] in nqueens[colorPerPos[(cy, cx)]]:
          shouldBeInCQueens.remove((cy, cx))
          isAlreadyInCQueens.add((cy, cx))
          # DONE here if color in queens[colorPerPos[(cy, cx)]]: finaliser et continue

        for color in range(C):
          if (cy, cx) in nqueens[color]:
            #break

            q = deque()
            q.appendleft((cy, cx, [(cy,cx)]))
            visited = {(0, 0)}
            while q:
              y, x, path = q.pop()

              if all((y, x) not in nqueens[col] for col in range(C)):
                break

              for (a, b) in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y - 1, x - 1), (y - 1, x + 1), (y+1, x - 1)):
                if (a, b) not in visited and N > a >= 0 and N > b >= 0 and (a,b) not in walls and not any((a,b) in nqueens[col] for col in range(C)):
                  visited.add((a, b))
                  q.appendleft((a, b, path+[(a,b)]))

            oldDelta = (0,0)
            for elt in range(len(path) - 1):
              (r, c) = path[elt]
              (i, j) = path[elt + 1]
              delta = (r-i, c-j)
              if delta == oldDelta:
                (a,b,c,d) = tempMoves[-1]
                tempMoves[-1] = (a,b,i,j)
              else:
                tempMoves.append((r, c, i, j))
              oldDelta = delta

            nqueens[color].remove(path[0])
            nqueens[color].add(path[-1])
            #colorPerPos[path[-1]] = color
            #del colorPerPos[path[0]]
            break

        # pour partir du point de chute, et pour y aller
        # DONE => FAIRE BOUGER LES REINES EN DIAGO (concerne 2 BFS)

        color = colorPerPos[(cy, cx)] # CONCERNE LA TARGET, PAS LA COULEUR COURANTE
        q = deque()
        q.appendleft((cy, cx, [(cy, cx)]))
        visited = {(cy, cx)}
        #print(queens[color], file=sys.stderr, flush=True)
        while q:
          y, x, path = q.pop()
          #print(y, x, path, file=sys.stderr, flush=True)

          for (a, b) in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1)):
            if (a, b) in nqueens[color] and (a,b) not in isAlreadyInCQueens:  # TODO TROUVER QUOI FAIRE QUAND CA N ARRIVE JAMAIS
              break
            if (a, b) not in visited and N > a >= 0 and N > b >= 0 and (a,b) not in walls and not any((a,b) in nqueens[col] for col in range(C)):

              visited.add((a, b))
              q.appendleft((a, b, path+[(a,b)]))

          if (a, b) in nqueens[color] and (a,b) not in isAlreadyInCQueens:  # TODO TROUVER QUOI FAIRE QUAND CA N ARRIVE JAMAIS
            path.append((a, b))
            #print(path[0], path[-1], file=sys.stderr, flush=True)

            break
        path.reverse()

        oldDelta = (0, 0)
        for elt in range(len(path) - 1):
          (r, c) = path[elt]
          (i, j) = path[elt + 1]
          delta = (r - i, c - j)
          if delta == oldDelta:
            (a, b, c, d) = tempMoves[-1]
            tempMoves[-1] = (a, b, i, j)
          else:
            tempMoves.append((r, c, i, j))
          oldDelta = delta

        #print(path[0] in isAlreadyInCQueens, file=sys.stderr, flush=True) #shouldBeInCQueens

        nqueens[color].remove(path[0])
        nqueens[color].add(path[-1])
        shouldBeInCQueens.remove(path[-1])
        isAlreadyInCQueens.add(path[-1])
        #colorPerPos[path[-1]] = color
        #del colorPerPos[path[0]]
        #print(path[0], path[-1], file=sys.stderr, flush=True) #shouldBeInCQueens
        #print(tempMoves, file=sys.stderr, flush=True) #shouldBeInCQueens
        #print(isAlreadyInCQueens, file=sys.stderr, flush=True) #shouldBeInCQueens

      for (r, c, i, j) in tempMoves:
        score += max(abs(r - i), abs(c - j)) ** 0.5
      nT = process_time()

      if score < currS:
        currS = score
        currQueens = cQueens
        if score < bestS:
          bestS = score
          moves = tempMoves
          bQueens = cQueens.copy()
          print(bestS, file=sys.stderr, flush=True)
          #print(moves, file=sys.stderr, flush=True)
          #print(bestS*N, file=sys.stderr, flush=True)
          #print(cQueens, file=sys.stderr, flush=True)

      else:
        r = random.uniform(0, 1)

        g = nT - start_time

        if g < 1:
          T = t_start * (t_final / t_start)**g
        if g < 2:
          T = t_start * (t_final / t_start)**(g-1)
        if g < 3:
          T = t_start * (t_final / t_start)**(g-2)
        if g < 4:
          T = t_start * (t_final / t_start)**(g-3)
        if g < 5:
          T = t_start * (t_final / t_start)**(g-4)
        if g < 6:
          T = t_start * (t_final / t_start)**(g-5)
        if g < 7:
          T = t_start * (t_final / t_start)**(g-6)
        if g < 8:
          T = t_start * (t_final / t_start)**(g-7)
        if g < 9:
          T = t_start * (t_final / t_start)**(g-8)
        else:
          T = t_start * (t_final / t_start)**(g-9)


        if math.exp((currS - score) / T) > r:
          currS = score
          currQueens = cQueens

      totT = nT - currT
      maxT = max(maxT, totT)
      currT = nT
    except Exception:
      pass
else:

  score = 0

  for color in range(C):

    for r in range(N):
      if amountsPerLine[color][r] > 1:
        score += (amountsPerLine[color][r] - 1) * (amountsPerLine[color][r]) // 2

    for c in range(N):
      if amountsPerCol[color][c] > 1:
        score += (amountsPerCol[color][c] - 1) * (amountsPerCol[color][c]) // 2

    for diag in amountsPerDiag[color]:
      if amountsPerDiag[color][diag] > 1:
        score += (amountsPerDiag[color][diag] - 1) * (amountsPerDiag[color][diag]) // 2

    for diag in amountsPerInvDiag[color]:
      if amountsPerInvDiag[color][diag] > 1:
        score += (amountsPerInvDiag[color][diag] - 1) * (amountsPerInvDiag[color][diag]) // 2

  bestScore = N * score
  moves = []
  maxT = 0
  currT = process_time()
  while currT - start_time + maxT < 9.5:
    cqueens = defaultdict(set)
    camountsPerLine = {}
    camountsPerCol = {}
    camountsPerDiag = {}  # x+y
    camountsPerInvDiag = {}  # (N-x)+y
    cmoves = []
    cpenalty = 0
    cscore = score

    for i in range(C):
      camountsPerLine[i] = amountsPerLine[i].copy()
      camountsPerCol[i] = amountsPerCol[i].copy()
      camountsPerDiag[i] = amountsPerDiag[i].copy()
      camountsPerInvDiag[i] = amountsPerInvDiag[i].copy()
      cqueens[i] = queens[i].copy()

    nbUseless = 0

    remaining = currT - start_time + maxT
    MM = max(30, N * N * step // 10)
    if remaining > 8:
      MM = min(MM, 100)
    MV = random.randint(8, MM)  # 2*N*N*N
    MMV = min(MV, 2 * N * N * N)
    improv = False
    while (nbUseless < 500 and len(cmoves) < MMV) or improv:
      improv = False

      # if process_time() - start_time + maxT > 9.5:
      #  break
      nMutations = random.randint(1, nMut)

      ncqueens = defaultdict(set)
      ncamountsPerLine = {}
      ncamountsPerCol = {}
      ncamountsPerDiag = {}  # x+y
      ncamountsPerInvDiag = {}  # (N-x)+y
      ncmoves = []
      nscore = cscore
      npenalty = cpenalty

      for i in range(C):
        ncamountsPerLine[i] = camountsPerLine[i].copy()
        ncamountsPerCol[i] = camountsPerCol[i].copy()
        ncamountsPerDiag[i] = camountsPerDiag[i].copy()
        ncamountsPerInvDiag[i] = camountsPerInvDiag[i].copy()
        ncqueens[i] = cqueens[i].copy()

      for mutation in range(nMutations):
        valid = []
        # ccc = 0
        while not valid:
          # ccc += 1

          (r, c, color) = random.choice([(r, c, col) for col in range(C) for (r, c) in ncqueens[col]])
          valid = getValidMoves(r, c, ncqueens)
        (i, j) = random.choice(valid)

        ncqueens[color].remove((r, c))
        ncamountsPerLine[color][r] -= 1
        ncamountsPerCol[color][c] -= 1
        ncamountsPerDiag[color][r + c] -= 1
        ncamountsPerInvDiag[color][r + (N - c)] -= 1

        ncqueens[color].add((i, j))
        ncamountsPerLine[color][i] += 1
        ncamountsPerCol[color][j] += 1
        ncamountsPerDiag[color][i + j] += 1
        ncamountsPerInvDiag[color][i + (N - j)] += 1

        ncmoves.append((r, c, i, j))
        npenalty += max(abs(r - i), abs(c - j))**0.5

      nscore = 0

      for color in range(C):

        for y in range(N):
          if ncamountsPerLine[color][y] > 1:
            nscore += (ncamountsPerLine[color][y] - 1) * (ncamountsPerLine[color][y]) // 2

        for x in range(N):
          if ncamountsPerCol[color][x] > 1:
            nscore += (ncamountsPerCol[color][x] - 1) * (ncamountsPerCol[color][x]) // 2

        for diag in ncamountsPerDiag[color]:
          if ncamountsPerDiag[color][diag] > 1:
            nscore += (ncamountsPerDiag[color][diag] - 1) * (ncamountsPerDiag[color][diag]) // 2

        for diag in ncamountsPerInvDiag[color]:
          if ncamountsPerInvDiag[color][diag] > 1:
            nscore += (ncamountsPerInvDiag[color][diag] - 1) * (ncamountsPerInvDiag[color][diag]) // 2

        # if nw < old-3:# or turn > 6:#car je me compte moi meme
        #      break
      # print("a", cscore, nscore, bestScore, file=sys.stderr, flush=True)
      if N * cscore + cpenalty > N * nscore + npenalty:
        # print("b", cscore, nscore, bestScore, file=sys.stderr, flush=True)
        cscore = nscore
        nbUseless = 0
        cpenalty = npenalty

        for move in ncmoves:
          cmoves.append(move)

        camountsPerCol = ncamountsPerCol
        camountsPerLine = ncamountsPerLine
        camountsPerDiag = ncamountsPerDiag
        camountsPerInvDiag = ncamountsPerInvDiag
        cqueens = ncqueens

        if bestScore > N * cscore + cpenalty:
          # print("c", cscore, bestScore, file=sys.stderr, flush=True)
          bestScore = N * cscore + cpenalty
          moves = cmoves.copy()
          improv = True

          # print("cc", moves, file=sys.stderr, flush=True)
      else:
        nbUseless += 1

    nT = process_time()
    totT = nT - currT
    maxT = max(maxT, totT)
    currT = nT

print(len(moves))
for (r,c,i,j) in moves:
    print(str(r)+" "+str(c)+" "+str(i)+" "+str(j))

sys.stdout.flush()
