import sys
from collections import deque, defaultdict
from time import process_time

def bfs(r,c):
  q = deque()
  q.appendleft((r, c, 0, 0, None, 0))
  visited = {(r, c)}
  finals = set()

  while q:
    (y, x, depth, crossedCoins, first, stayed) = q.pop()
    if depth == len(allLogs) or (len(finals) > 0 and process_time() - start_time > 9.5*(turn+nF/F)/1000):
      break

    if coinsPerFrog[(r, c)] > 30 and r < 4:
      if y == 0:
        finals.add((y, x, depth, crossedCoins, first))
    else:
      if x >= W // 2:
        if rowDir[y] == "<":
          finals.add((y, x, depth, crossedCoins, first))
      else:
        if rowDir[y] == ">":
          finals.add((y, x, depth, crossedCoins, first))

    for (b, a) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
      if (a, b) not in visited:
        visited.add((a, b))
        if (a, b) not in currentFrogsPos and ((a, b) in allLogs[depth] or (a, b) in beach):
          nb = b

          if (a, b) in allLogs[depth]:
            if rowDir[a] == "<":
              nb -= 1
            else:
              nb += 1
          visited.add((a, nb))

          if 0 <= nb < W:
            q.appendleft((a, nb, depth + 1, crossedCoins+1 if depth < len(allCoins) and (a, b) in allCoins[depth] else crossedCoins, (a, b) if not first else first, 0))  

    if stayed < 2 and depth <= 2:
      (a,b) = (y,x)
      nb = b

      if (a, b) in allLogs[depth]:
        if rowDir[a] == "<":
          nb -= 1
        else:
          nb += 1
      if 0 <= nb < W:
        q.appendleft((a, nb, depth + 1, crossedCoins+1 if depth < len(allCoins) and (a, b) in allCoins[depth] else crossedCoins, (a, b) if not first else first, stayed+1)) 

  if finals:
    scores = {}
    for (y, x, depth, crossedCoins, first) in finals:
      score = 4*crossedCoins
      if x >= W // 2 and rowDir[y] == ">":
        score -= 100 * x ** 2
      if x < W // 2 and rowDir[y] == "<":
        score -= 100 * (W - x) ** 2
      if turn < 870 and not coinsPerFrog[(r, c)] > threshold:
        if r != H:
          score += y
      else:
        if r > 0:
          score -= y
      if first not in scores or scores[first] < score:
        scores[first] = score

    return list({a: b for a, b in sorted(scores.items(), key=lambda x: x[1])}.keys())[-1]

  if c >= W // 2:
    if rowDir[r] == "<":
      return (r, c)
  else:
    if rowDir[r] == ">":
      return(r, c)
  return first


H = int(input())
start_time = process_time()
W = int(input())
F = int(input())
KL = int(input())
KW = int(input())
PC = float(input())

threshold = 30*(1 + W-8 + KL-2 + 5-KW)

if (KW == 1 and W > 22) or (KW == 1 and W > 17 and KL > 3) or (KW == 2 and W > 24 and KL > 3):
  threshold = 155 * (1 + W - 8 + KL - 2 + 5 - KW)
coinsPerFrog = defaultdict(int)
 
rowDir=[''] * H;
for r in range(1,H): rowDir[r]=input()[0]

grid = [['' for x in range(W)] for y in range(H)]

for turn in range(1000):
  temp = {}

  frogs = set()
  logs = set()
  coins = set()
  beach = set()
  # beach ('#'), water ('.'), log ('='), frog ('@') or coin ('o').

  for r in range(H):
    for c in range(W):
      grid[r][c] = input()[0]
      if grid[r][c] == '@':
        frogs.add((r,c))
        if r > 0:
          logs.add((r, c))
      if grid[r][c] == '=':
        logs.add((r,c))
      if grid[r][c] == 'o':
        coins.add((r,c))
        logs.add((r, c))
      if grid[r][c] == '#':
        beach.add((r,c))

  elapsedTime=int(input())

  allLogs = [logs]
  nlogs = logs 

  while nlogs:

    nnlogs = set()
    for (y,x) in nlogs:
      if rowDir[y] == "<" and x-1 >= 0:
        nnlogs.add((y, x - 1))
      if rowDir[y] == ">" and x + 1 < H:
        nnlogs.add((y, x + 1))

    allLogs += [nnlogs]
    nlogs = nnlogs

  allCoins = [coins]
  ncoins = coins 

  while ncoins:

    nncoins = set()
    for (y,x) in ncoins:
      if rowDir[y] == "<" and x-1 >= 0:
        nncoins.add((y, x - 1))
      if rowDir[y] == ">" and x + 1 < H:
        nncoins.add((y, x + 1))

    allCoins += [nncoins]
    ncoins = nncoins


  moves=[]
  currentFrogsPos = frogs.copy()
  nF = 0
  for (r,c) in frogs:
    nF += 1
    first = bfs(r,c)

    if first:

      (a,b) = first

      if first in logs:
        if rowDir[a] == "<":
          b -= 1
        else:
          b += 1
      if (a,b) != (r,c):
        if (a, b) in coinsPerFrog:
          temp[(a,b)] = r * (1 if first in coins else 0)
          if (r,c) in coinsPerFrog:
            temp[(a,b)] += coinsPerFrog[(r, c)]
            del coinsPerFrog[(r,c)]
            if a == 0:
              temp[(a, b)] = 0
        else:
          coinsPerFrog[(a,b)] = r * (1 if first in coins else 0)
          if (r,c) in coinsPerFrog:
            coinsPerFrog[(a,b)] += coinsPerFrog[(r, c)]
            del coinsPerFrog[(r,c)]
            if a == 0:
              coinsPerFrog[(a, b)] = 0
      else:
        coinsPerFrog[(a, b)] += r * (1 if first in coins else 0)

      if first == (r+1,c):
        moves.append(str(r) + " " + str(c) + " D")
        currentFrogsPos.remove((r,c))
        currentFrogsPos.add(first)
      if first == (r-1,c):
        moves.append(str(r) + " " + str(c) + " U")
        currentFrogsPos.remove((r,c))
        currentFrogsPos.add(first)
      if first == (r,c+1):
        moves.append(str(r) + " " + str(c) + " R")
        currentFrogsPos.remove((r,c))
        currentFrogsPos.add(first)
      if first == (r,c-1):
        moves.append(str(r) + " " + str(c) + " L")
        currentFrogsPos.remove((r,c))
        currentFrogsPos.add(first)

    else:
      first = (r,c)
      (a,b) = first
      if first in logs:
        if rowDir[r] == "<":
          b -= 1
        else:
          b += 1

        if (r,c) in coinsPerFrog:
          if (a,b) in coinsPerFrog:
            temp[(a,b)] = coinsPerFrog[(r, c)]
          else:
            coinsPerFrog[(a,b)] = coinsPerFrog[(r, c)]
          del coinsPerFrog[(r,c)]


  for (a,b) in temp.items():
    coinsPerFrog[a] = b

  print(len(moves))
  for m in moves: print(m)
  sys.stdout.flush()
